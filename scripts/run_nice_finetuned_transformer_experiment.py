import argparse
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import f1_score, hamming_loss, label_ranking_average_precision_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from run_nice_multilabel_experiment import find_best_threshold, load_nice_dataset, markdown_table, stratify_key
from run_nice_per_label_threshold_experiment import evaluate_per_label_thresholds, per_label_thresholds


class TextMultiLabelDataset(Dataset):
    def __init__(self, texts: np.ndarray, labels: np.ndarray, tokenizer, max_length: int):
        self.texts = list(texts)
        self.labels = labels.astype(np.float32)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, index: int) -> dict:
        encoded = self.tokenizer(
            self.texts[index],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )
        return {
            "input_ids": encoded["input_ids"].squeeze(0),
            "attention_mask": encoded["attention_mask"].squeeze(0),
            "labels": torch.tensor(self.labels[index], dtype=torch.float32),
        }


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(False)


def evaluate_scores(y_true: np.ndarray, y_score: np.ndarray, threshold: float) -> dict:
    y_pred = (y_score >= threshold).astype(int)
    return {
        "micro_f1": f1_score(y_true, y_pred, average="micro", zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "hamming_loss": hamming_loss(y_true, y_pred),
        "label_ranking_average_precision": label_ranking_average_precision_score(y_true, y_score),
    }


def make_loader(
    texts: np.ndarray,
    labels: np.ndarray,
    tokenizer,
    max_length: int,
    batch_size: int,
    shuffle: bool,
) -> DataLoader:
    dataset = TextMultiLabelDataset(texts, labels, tokenizer, max_length)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def predict_scores(model, loader: DataLoader, device: torch.device) -> np.ndarray:
    model.eval()
    scores = []
    with torch.no_grad():
        for batch in loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            logits = model(input_ids=input_ids, attention_mask=attention_mask).logits
            scores.append(torch.sigmoid(logits).cpu().numpy())
    return np.vstack(scores)


def train_one_fold(
    model_name: str,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_valid: np.ndarray,
    y_valid: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    fold_seed: int,
    labels: list[str],
    epochs: int,
    batch_size: int,
    max_length: int,
    learning_rate: float,
    use_pos_weight: bool,
    calibration: str,
    device: torch.device,
) -> tuple[dict, dict]:
    set_seed(fold_seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(labels),
        problem_type="multi_label_classification",
    ).to(device)

    train_loader = make_loader(x_train, y_train, tokenizer, max_length, batch_size, shuffle=True)
    valid_loader = make_loader(x_valid, y_valid, tokenizer, max_length, batch_size, shuffle=False)
    test_loader = make_loader(x_test, y_test, tokenizer, max_length, batch_size, shuffle=False)

    pos_weight = None
    if use_pos_weight:
        pos = y_train.sum(axis=0)
        neg = len(y_train) - pos
        pos_weight = np.divide(neg, np.maximum(pos, 1), dtype=np.float64)
        pos_weight = np.clip(pos_weight, 1.0, 20.0)
        criterion = torch.nn.BCEWithLogitsLoss(pos_weight=torch.tensor(pos_weight, dtype=torch.float32).to(device))
    else:
        criterion = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    epoch_losses = []
    for _ in range(epochs):
        model.train()
        losses = []
        for batch in train_loader:
            optimizer.zero_grad(set_to_none=True)
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            batch_labels = batch["labels"].to(device)
            logits = model(input_ids=input_ids, attention_mask=attention_mask).logits
            loss = criterion(logits, batch_labels)
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        epoch_losses.append(float(np.mean(losses)))

    valid_score = predict_scores(model, valid_loader, device)
    test_score = predict_scores(model, test_loader, device)
    if calibration == "per_label":
        thresholds = per_label_thresholds(y_valid, valid_score)
        metrics = {"threshold": float(thresholds.mean()), **evaluate_per_label_thresholds(y_test, test_score, thresholds)}
        threshold_detail = thresholds.tolist()
    else:
        threshold = find_best_threshold(y_valid, valid_score)
        metrics = {"threshold": threshold, **evaluate_scores(y_test, test_score, threshold)}
        threshold_detail = threshold
    diagnostics = {
        "epoch_losses": epoch_losses,
        "pos_weight": pos_weight.tolist() if pos_weight is not None else None,
        "threshold_detail": threshold_detail,
    }
    return metrics, diagnostics


def summarize(fold_results: pd.DataFrame) -> pd.DataFrame:
    metric_columns = [
        "micro_f1",
        "macro_f1",
        "weighted_f1",
        "hamming_loss",
        "label_ranking_average_precision",
    ]
    row = {"model": fold_results["model"].iloc[0]}
    for metric in metric_columns:
        row[f"{metric}_mean"] = fold_results[metric].mean()
        row[f"{metric}_std"] = fold_results[metric].std(ddof=1)
    row["threshold_mean"] = fold_results["threshold"].mean()
    return pd.DataFrame([row])


def write_report(
    report_path: Path,
    raw_path: Path,
    model_name: str,
    labels: list[str],
    fold_results: pd.DataFrame,
    summary: pd.DataFrame,
    args: argparse.Namespace,
) -> None:
    lines = [
        "# NICE Fine-tuned Transformer Baseline",
        "",
        "## Setup",
        "",
        f"- Dataset: `{raw_path}`",
        f"- Transformer: `{model_name}`",
        f"- Labels: `{len(labels)}`",
        f"- Folds: `{fold_results['fold'].nunique()}`",
        f"- Epochs per fold: `{args.epochs}`",
        f"- Batch size: `{args.batch_size}`",
        f"- Max sequence length: `{args.max_length}`",
        f"- Learning rate: `{args.learning_rate}`",
        f"- Loss: BCEWithLogitsLoss; positive weights: `{args.use_pos_weight}`.",
        f"- Calibration: `{args.calibration}` thresholds selected on validation data.",
        "",
        "## Mean Results",
        "",
        markdown_table(summary, float_digits=4),
        "",
        "## Per-fold Results",
        "",
        markdown_table(fold_results, float_digits=4),
        "",
        "## Interpretation",
        "",
        "- This is a fine-tuned transformer baseline, not a frozen embedding baseline.",
        "- Because NICE has only 381 usable requirements and rare label combinations, these fold-level estimates should be interpreted cautiously.",
        "- The result is intended to bound performance against a task-adapted neural baseline, not to tune for state-of-the-art performance.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/PROMISE-relabeled-NICE.csv")
    parser.add_argument("--model-name", default="distilbert-base-uncased")
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--use-pos-weight", action="store_true")
    parser.add_argument("--calibration", choices=["global", "per_label"], default="per_label")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default="reports")
    args = parser.parse_args()

    raw_path = Path(args.data)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    data, labels = load_nice_dataset(raw_path)
    x = data["text"].to_numpy()
    y = data[labels].to_numpy(dtype=int)
    keys = stratify_key(y, labels)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    fold_rows = []
    diagnostics = {}
    splitter = StratifiedKFold(n_splits=args.folds, shuffle=True, random_state=args.seed)
    for fold, (train_all_idx, test_idx) in enumerate(splitter.split(x, keys), start=1):
        train_idx, valid_idx = train_test_split(
            train_all_idx,
            test_size=0.20,
            random_state=args.seed + fold,
            stratify=stratify_key(y[train_all_idx], labels),
        )
        metrics, fold_diagnostics = train_one_fold(
            model_name=args.model_name,
            x_train=x[train_idx],
            y_train=y[train_idx],
            x_valid=x[valid_idx],
            y_valid=y[valid_idx],
            x_test=x[test_idx],
            y_test=y[test_idx],
            fold_seed=args.seed + fold,
            labels=labels,
            epochs=args.epochs,
            batch_size=args.batch_size,
            max_length=args.max_length,
            learning_rate=args.learning_rate,
            use_pos_weight=args.use_pos_weight,
            calibration=args.calibration,
            device=device,
        )
        fold_rows.append(
            {
                "fold": fold,
                "model": f"finetuned_{args.model_name.replace('/', '_').replace('-', '_')}",
                **metrics,
            }
        )
        diagnostics[str(fold)] = fold_diagnostics
        print(f"Fold {fold}: macro_f1={metrics['macro_f1']:.4f}, threshold={metrics['threshold']:.2f}")

    fold_results = pd.DataFrame(fold_rows)
    summary = summarize(fold_results)

    safe_model_name = args.model_name.replace("/", "_").replace("-", "_")
    fold_path = out_dir / f"nice_finetuned_transformer_{safe_model_name}_fold_results.csv"
    summary_path = out_dir / f"nice_finetuned_transformer_{safe_model_name}_summary.csv"
    report_path = out_dir / f"nice_finetuned_transformer_{safe_model_name}_report.md"
    metadata_path = out_dir / f"nice_finetuned_transformer_{safe_model_name}_metadata.json"

    fold_results.to_csv(fold_path, index=False)
    summary.to_csv(summary_path, index=False)
    write_report(report_path, raw_path, args.model_name, labels, fold_results, summary, args)
    metadata_path.write_text(
        json.dumps(
            {
                "source": str(raw_path),
                "model_name": args.model_name,
                "folds": args.folds,
                "epochs": args.epochs,
                "batch_size": args.batch_size,
                "max_length": args.max_length,
                "learning_rate": args.learning_rate,
                "use_pos_weight": args.use_pos_weight,
                "calibration": args.calibration,
                "seed": args.seed,
                "device": str(device),
                "labels": labels,
                "diagnostics": diagnostics,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote fold results: {fold_path}")
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote report: {report_path}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
