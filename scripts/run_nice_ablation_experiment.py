import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, hamming_loss, label_ranking_average_precision_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from quantum_re_nfr.quantum_model import (
    HybridQuantumSVMNFRClassifier,
    QuantumInspiredContrastiveNFRClassifier,
    QuantumInspiredNFRClassifier,
)
from run_nice_multilabel_experiment import find_best_threshold, load_nice_dataset, markdown_table, stratify_key


def evaluate_scores(y_true: np.ndarray, y_score: np.ndarray, threshold: float) -> dict:
    y_pred = (y_score >= threshold).astype(int)
    return {
        "micro_f1": f1_score(y_true, y_pred, average="micro", zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "hamming_loss": hamming_loss(y_true, y_pred),
        "label_ranking_average_precision": label_ranking_average_precision_score(y_true, y_score),
    }


def sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -50, 50)
    return 1 / (1 + np.exp(-x))


def model_suite(seed: int) -> dict:
    return {
        "svm_only_sublinear_tfidf": OneVsRestClassifier(
            Pipeline(
                [
                    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
                    ("clf", LinearSVC(class_weight="balanced", dual="auto", random_state=seed)),
                ]
            )
        ),
        "positive_projection_no_interference": QuantumInspiredNFRClassifier(
            random_state=seed,
            interference_weight=0.0,
        ),
        "positive_projection_with_interference": QuantumInspiredNFRClassifier(
            random_state=seed,
            interference_weight=0.15,
        ),
        "contrastive_projection_no_interference": QuantumInspiredContrastiveNFRClassifier(
            random_state=seed,
            interference_weight=0.0,
        ),
        "contrastive_projection_with_interference": QuantumInspiredContrastiveNFRClassifier(
            random_state=seed,
            interference_weight=0.05,
        ),
        "hybrid_alpha_0_15": HybridQuantumSVMNFRClassifier(random_state=seed, quantum_weight=0.15),
        "hybrid_alpha_0_30": HybridQuantumSVMNFRClassifier(random_state=seed, quantum_weight=0.30),
        "hybrid_alpha_0_50": HybridQuantumSVMNFRClassifier(random_state=seed, quantum_weight=0.50),
    }


def fit_model(model, x_train: np.ndarray, y_train: np.ndarray):
    if isinstance(
        model,
        (
            QuantumInspiredNFRClassifier,
            QuantumInspiredContrastiveNFRClassifier,
            HybridQuantumSVMNFRClassifier,
        ),
    ):
        model.fit(list(x_train), y_train)
    else:
        model.fit(x_train, y_train)
    return model


def predict_scores(model, x_values: np.ndarray) -> np.ndarray:
    if isinstance(
        model,
        (
            QuantumInspiredNFRClassifier,
            QuantumInspiredContrastiveNFRClassifier,
            HybridQuantumSVMNFRClassifier,
        ),
    ):
        return model.predict_proba(list(x_values))
    if hasattr(model, "predict_proba"):
        return model.predict_proba(x_values)
    return sigmoid(model.decision_function(x_values))


def summarize(results: pd.DataFrame) -> pd.DataFrame:
    metric_columns = [
        "micro_f1",
        "macro_f1",
        "weighted_f1",
        "hamming_loss",
        "label_ranking_average_precision",
    ]
    rows = []
    for model, group in results.groupby("model"):
        row = {"model": model}
        for metric in metric_columns:
            row[f"{metric}_mean"] = group[metric].mean()
            row[f"{metric}_std"] = group[metric].std(ddof=1)
        row["threshold_mean"] = group["threshold"].mean()
        rows.append(row)
    return pd.DataFrame(rows).sort_values("macro_f1_mean", ascending=False)


def write_report(report_path: Path, raw_path: Path, labels: list[str], fold_results: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# NICE Quantum-inspired Ablation Study",
        "",
        "## Setup",
        "",
        f"- Dataset: `{raw_path}`",
        f"- Labels: `{len(labels)}`",
        f"- Folds: `{fold_results['fold'].nunique()}`",
        "- Each model uses the same train/validation/test fold partitions.",
        "- A global threshold is selected on the validation split by maximizing Macro-F1.",
        "",
        "## Ablation Meaning",
        "",
        "- `svm_only_sublinear_tfidf`: discriminative SVM component without quantum projection.",
        "- `positive_projection_no_interference`: original centroid projection without label co-occurrence adjustment.",
        "- `positive_projection_with_interference`: original centroid projection with label co-occurrence adjustment.",
        "- `contrastive_projection_no_interference`: positive-minus-negative label directions without co-occurrence adjustment.",
        "- `contrastive_projection_with_interference`: contrastive projection with co-occurrence adjustment.",
        "- `hybrid_alpha_*`: score-level fusion between contrastive projection and SVM with different quantum weights.",
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
        "- This ablation is designed to verify whether each proposed component contributes useful signal.",
        "- If `contrastive_projection_with_interference` improves over `positive_projection_with_interference`, contrastive label directions are beneficial.",
        "- If hybrid variants improve over pure projection variants, discriminative calibration is beneficial.",
        "- If increasing `alpha` hurts performance, the quantum component is useful as a calibrated auxiliary signal rather than as the dominant score.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/PROMISE-relabeled-NICE.csv")
    parser.add_argument("--folds", type=int, default=5)
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

    results = []
    splitter = StratifiedKFold(n_splits=args.folds, shuffle=True, random_state=args.seed)
    for fold, (train_all_idx, test_idx) in enumerate(splitter.split(x, keys), start=1):
        train_idx, valid_idx = train_test_split(
            train_all_idx,
            test_size=0.20,
            random_state=args.seed + fold,
            stratify=stratify_key(y[train_all_idx], labels),
        )
        x_train, x_valid, x_test = x[train_idx], x[valid_idx], x[test_idx]
        y_train, y_valid, y_test = y[train_idx], y[valid_idx], y[test_idx]

        for model_name, model in model_suite(args.seed + fold).items():
            fit_model(model, x_train, y_train)
            valid_score = predict_scores(model, x_valid)
            test_score = predict_scores(model, x_test)
            threshold = find_best_threshold(y_valid, valid_score)
            results.append(
                {
                    "fold": fold,
                    "model": model_name,
                    "threshold": threshold,
                    **evaluate_scores(y_test, test_score, threshold),
                }
            )

    fold_results = pd.DataFrame(results)
    summary = summarize(fold_results)

    fold_path = out_dir / "nice_ablation_fold_results.csv"
    summary_path = out_dir / "nice_ablation_summary.csv"
    report_path = out_dir / "nice_ablation_report.md"
    metadata_path = out_dir / "nice_ablation_metadata.json"

    fold_results.to_csv(fold_path, index=False)
    summary.to_csv(summary_path, index=False)
    write_report(report_path, raw_path, labels, fold_results, summary)
    metadata_path.write_text(
        json.dumps(
            {
                "source": str(raw_path),
                "folds": args.folds,
                "seed": args.seed,
                "labels": labels,
                "threshold_selection": "validation macro_f1 grid search from 0.05 to 0.95",
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
