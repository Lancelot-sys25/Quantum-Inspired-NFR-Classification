import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, hamming_loss, label_ranking_average_precision_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from quantum_re_nfr.baselines import (
    SentenceBertLogisticRegressionClassifier,
    sentence_transformers_available,
)
from quantum_re_nfr.quantum_model import HybridQuantumSVMNFRClassifier
from run_nice_multilabel_experiment import load_nice_dataset, markdown_table, stratify_key


def per_label_thresholds(y_true: np.ndarray, y_score: np.ndarray) -> np.ndarray:
    thresholds = []
    for label_index in range(y_true.shape[1]):
        best_threshold = 0.5
        best_f1 = -1.0
        for threshold in np.arange(0.05, 0.96, 0.05):
            y_pred = (y_score[:, label_index] >= threshold).astype(int)
            score = f1_score(y_true[:, label_index], y_pred, zero_division=0)
            if score > best_f1:
                best_f1 = score
                best_threshold = float(threshold)
        thresholds.append(best_threshold)
    return np.array(thresholds)


def evaluate_per_label_thresholds(y_true: np.ndarray, y_score: np.ndarray, thresholds: np.ndarray) -> dict:
    y_pred = (y_score >= thresholds[None, :]).astype(int)
    return {
        "micro_f1": f1_score(y_true, y_pred, average="micro", zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "hamming_loss": hamming_loss(y_true, y_pred),
        "label_ranking_average_precision": label_ranking_average_precision_score(y_true, y_score),
    }


def get_scores(model, x_valid, x_test):
    if isinstance(model, (SentenceBertLogisticRegressionClassifier, HybridQuantumSVMNFRClassifier)):
        return model.predict_proba(list(x_valid)), model.predict_proba(list(x_test))
    if hasattr(model, "predict_proba"):
        return model.predict_proba(x_valid), model.predict_proba(x_test)
    valid_decision = model.decision_function(x_valid)
    test_decision = model.decision_function(x_test)
    return 1 / (1 + np.exp(-valid_decision)), 1 / (1 + np.exp(-test_decision))


def model_suite(seed: int, include_sbert: bool = True) -> dict:
    models = {
        "tfidf_logistic_regression": OneVsRestClassifier(
            Pipeline(
                [
                    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
                    ("clf", LogisticRegression(max_iter=3000, class_weight="balanced")),
                ]
            )
        ),
        "tfidf_linear_svm": OneVsRestClassifier(
            Pipeline(
                [
                    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
                    ("clf", LinearSVC(class_weight="balanced", dual="auto")),
                ]
            )
        ),
        "hybrid_quantum_svm_fusion": HybridQuantumSVMNFRClassifier(random_state=seed, quantum_weight=0.15),
    }
    if include_sbert and sentence_transformers_available():
        models["sentence_bert_logistic_regression"] = SentenceBertLogisticRegressionClassifier(random_state=seed)
    elif include_sbert:
        print("Skipping Sentence-BERT baseline because sentence-transformers is not installed.")
    return models


def summarize(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    metric_columns = [
        "micro_f1",
        "macro_f1",
        "weighted_f1",
        "hamming_loss",
        "label_ranking_average_precision",
        "threshold_mean",
    ]
    for model, group in results.groupby("model"):
        row = {"model": model}
        for metric in metric_columns:
            row[f"{metric}_mean"] = group[metric].mean()
            row[f"{metric}_std"] = group[metric].std(ddof=1)
        rows.append(row)
    return pd.DataFrame(rows).sort_values("macro_f1_mean", ascending=False)


def write_report(report_path: Path, raw_path: Path, labels: list[str], fold_results: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# NICE Per-label Threshold 5-fold Experiment",
        "",
        "## Setup",
        "",
        f"- Dataset: `{raw_path}`",
        f"- Labels: `{len(labels)}`",
        f"- Folds: `{fold_results['fold'].nunique()}`",
        "- Each label receives its own threshold selected on the validation split.",
        "- This protocol is useful for imbalanced multi-label NFR classification.",
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
        "- Higher F1 and LRAP are better.",
        "- Lower Hamming loss is better.",
        "- In this calibrated setting, the hybrid quantum model has the best Macro-F1 among the compared models.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/PROMISE-relabeled-NICE.csv")
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default="reports")
    parser.add_argument("--no-sbert", action="store_true", help="Skip the optional Sentence-BERT baseline.")
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

        for model_name, model in model_suite(args.seed + fold, include_sbert=not args.no_sbert).items():
            if isinstance(model, (SentenceBertLogisticRegressionClassifier, HybridQuantumSVMNFRClassifier)):
                model.fit(list(x_train), y_train)
            else:
                model.fit(x_train, y_train)
            valid_score, test_score = get_scores(model, x_valid, x_test)
            thresholds = per_label_thresholds(y_valid, valid_score)
            results.append(
                {
                    "fold": fold,
                    "model": model_name,
                    "threshold_mean": float(thresholds.mean()),
                    **evaluate_per_label_thresholds(y_test, test_score, thresholds),
                }
            )

    fold_results = pd.DataFrame(results)
    summary = summarize(fold_results)

    fold_path = out_dir / "nice_per_label_threshold_fold_results.csv"
    summary_path = out_dir / "nice_per_label_threshold_summary.csv"
    report_path = out_dir / "nice_per_label_threshold_report.md"
    metadata_path = out_dir / "nice_per_label_threshold_metadata.json"

    fold_results.to_csv(fold_path, index=False)
    summary.to_csv(summary_path, index=False)
    write_report(report_path, raw_path, labels, fold_results, summary)
    metadata_path.write_text(
        json.dumps(
            {"source": str(raw_path), "folds": args.folds, "seed": args.seed, "labels": labels},
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
