import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    classification_report,
    f1_score,
    hamming_loss,
    label_ranking_average_precision_score,
)
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression

from quantum_re_nfr.baselines import (
    SentenceBertLogisticRegressionClassifier,
    sentence_transformers_available,
)
from quantum_re_nfr.explainability import top_feature_contributions
from quantum_re_nfr.quantum_model import (
    HybridQuantumSVMNFRClassifier,
    QuantumInspiredContrastiveNFRClassifier,
    QuantumInspiredNFRClassifier,
)


LABEL_COLUMNS = {
    "Availability (A)": "availability",
    "Fault Tolerance (FT)": "fault_tolerance",
    "Legal (L)": "legal",
    "Look & Feel (LF)": "look_and_feel",
    "Maintainability (MN)": "maintainability",
    "Operability (O)": "operability",
    "Performance (PE)": "performance",
    "Portability (PO)": "portability",
    "Scalability (SC)": "scalability",
    "Security (SE)": "security",
    "Usability (US)": "usability",
    "Other (OT)": "other",
}


def clean_requirement(text: str) -> str:
    text = str(text).strip()
    if len(text) >= 2 and text[0] == "'" and text[-1] == "'":
        text = text[1:-1]
    return " ".join(text.split())


def load_nice_dataset(path: Path) -> tuple[pd.DataFrame, list[str]]:
    data = pd.read_csv(path)
    missing = {"RequirementText", *LABEL_COLUMNS.keys()} - set(data.columns)
    if missing:
        raise ValueError(f"Missing expected NICE columns: {sorted(missing)}")

    data = data.rename(columns=LABEL_COLUMNS)
    labels = list(LABEL_COLUMNS.values())
    data["text"] = data["RequirementText"].map(clean_requirement)
    data[labels] = data[labels].fillna(0).astype(int)

    # Keep rows that have at least one NFR subclass label.
    data = data[data[labels].sum(axis=1) > 0].reset_index(drop=True)
    labels = [label for label in labels if data[label].sum() > 0]
    data.insert(0, "sample_id", [f"NICE_{i + 1:04d}" for i in range(len(data))])
    return data[["sample_id", "ProjectID", "text", *labels]], labels


def stratify_key(y: np.ndarray, labels: list[str]) -> list[str]:
    keys = []
    for row in y:
        active = [labels[i] for i, value in enumerate(row) if value == 1]
        keys.append("+".join(active) if active else "none")
    counts = pd.Series(keys).value_counts()
    return [key if counts[key] >= 2 else "rare_combo" for key in keys]


def evaluate_scores(y_true: np.ndarray, y_score: np.ndarray, threshold: float = 0.5) -> dict:
    y_pred = (y_score >= threshold).astype(int)
    return {
        "micro_f1": f1_score(y_true, y_pred, average="micro", zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "hamming_loss": hamming_loss(y_true, y_pred),
        "label_ranking_average_precision": label_ranking_average_precision_score(y_true, y_score),
    }


def find_best_threshold(y_true: np.ndarray, y_score: np.ndarray, metric: str = "macro_f1") -> float:
    best_threshold = 0.5
    best_score = -1.0
    for threshold in np.arange(0.05, 0.96, 0.05):
        scores = evaluate_scores(y_true, y_score, float(threshold))
        if scores[metric] > best_score:
            best_score = scores[metric]
            best_threshold = float(threshold)
    return best_threshold


def dummy_scores(train_y: np.ndarray, test_size: int) -> np.ndarray:
    frequency = train_y.mean(axis=0)
    return np.tile(frequency, (test_size, 1))


def markdown_table(frame: pd.DataFrame, float_digits: int | None = None) -> str:
    headers = list(frame.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in frame.iterrows():
        cells = []
        for col in headers:
            value = row[col]
            if isinstance(value, float) and float_digits is not None:
                cells.append(f"{value:.{float_digits}f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_report(
    report_path: Path,
    raw_path: Path,
    processed_path: Path,
    data: pd.DataFrame,
    labels: list[str],
    metrics: list[dict],
    per_label_reports: dict[str, str],
    example: dict,
) -> None:
    metrics_frame = pd.DataFrame(metrics)
    label_counts = (
        pd.DataFrame({"label": labels, "count": data[labels].sum(axis=0).astype(int).to_list()})
        .sort_values("count", ascending=False)
        .reset_index(drop=True)
    )
    label_cardinality = float(data[labels].sum(axis=1).mean())
    multilabel_rows = int((data[labels].sum(axis=1) > 1).sum())

    lines = [
        "# NICE Multi-label NFR Experiment Report",
        "",
        "## Dataset",
        "",
        f"- Raw file: `{raw_path}`",
        f"- Processed file: `{processed_path}`",
        f"- Requirements used: `{len(data)}`",
        f"- NFR labels: `{len(labels)}`",
        f"- Multi-label requirements: `{multilabel_rows}`",
        f"- Label cardinality: `{label_cardinality:.4f}`",
        "- Task: multi-label NFR subclass classification.",
        "",
        "## Label Distribution",
        "",
        markdown_table(label_counts),
        "",
        "## Overall Results",
        "",
        markdown_table(metrics_frame, float_digits=4),
        "",
        "## Interpretation",
        "",
        "- `micro_f1`: global multi-label F1 across all labels.",
        "- `macro_f1`: average F1 across labels; important for rare NFR classes.",
        "- `hamming_loss`: fraction of wrong label decisions; lower is better.",
        "- `label_ranking_average_precision`: whether correct labels are ranked above incorrect labels; higher is better.",
        "- `threshold`: decision cutoff selected on the validation split, then applied to the held-out test split.",
        "",
        "## Quantum-inspired Explanation Example",
        "",
        f"- Text: {example['text']}",
        f"- True labels: `{', '.join(example['true_labels'])}`",
        f"- Predicted labels: `{', '.join(example['predicted_labels'])}`",
        f"- Explanation label: `{example['explanation_label']}`",
        "",
        "| token/phrase | semantic amplitude contribution |",
        "|---|---:|",
    ]
    for term, score in example["contributions"]:
        lines.append(f"| {term} | {score:.4f} |")

    lines.extend(["", "## Per-label Classification Reports", ""])
    for model_name, report in per_label_reports.items():
        lines.extend([f"### {model_name}", "", "```text", report, "```", ""])

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/PROMISE-relabeled-NICE.csv")
    parser.add_argument("--test-size", type=float, default=0.30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--out-dir", default="reports")
    parser.add_argument("--no-sbert", action="store_true", help="Skip the optional Sentence-BERT baseline.")
    args = parser.parse_args()

    raw_path = Path(args.data)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    data, labels = load_nice_dataset(raw_path)
    processed_path = Path("data/processed/nice_multilabel_nfr.csv")
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(processed_path, index=False)

    x = data["text"].to_numpy()
    y = data[labels].to_numpy(dtype=int)
    train_idx, test_idx = train_test_split(
        np.arange(len(data)),
        test_size=args.test_size,
        random_state=args.seed,
        stratify=stratify_key(y, labels),
    )

    train_idx, valid_idx = train_test_split(
        train_idx,
        test_size=0.20,
        random_state=args.seed,
        stratify=stratify_key(y[train_idx], labels),
    )

    x_train, x_valid, x_test = x[train_idx], x[valid_idx], x[test_idx]
    y_train, y_valid, y_test = y[train_idx], y[valid_idx], y[test_idx]

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
    }
    if not args.no_sbert and sentence_transformers_available():
        models["sentence_bert_logistic_regression"] = SentenceBertLogisticRegressionClassifier(random_state=args.seed)
    elif not args.no_sbert:
        print("Skipping Sentence-BERT baseline because sentence-transformers is not installed.")

    metrics = []
    per_label_reports = {}

    valid_score = dummy_scores(y_train, len(x_valid))
    threshold = find_best_threshold(y_valid, valid_score)
    y_score = dummy_scores(y_train, len(x_test))
    row = {
        "model": "label_frequency_baseline",
        "threshold": threshold,
        **evaluate_scores(y_test, y_score, threshold),
    }
    metrics.append(row)
    per_label_reports["label_frequency_baseline"] = classification_report(
        y_test,
        (y_score >= threshold).astype(int),
        target_names=labels,
        zero_division=0,
    )

    for model_name, model in models.items():
        if isinstance(model, SentenceBertLogisticRegressionClassifier):
            model.fit(list(x_train), y_train)
        else:
            model.fit(x_train, y_train)
        if hasattr(model, "predict_proba"):
            if isinstance(model, SentenceBertLogisticRegressionClassifier):
                valid_score = model.predict_proba(list(x_valid))
                y_score = model.predict_proba(list(x_test))
            else:
                valid_score = model.predict_proba(x_valid)
                y_score = model.predict_proba(x_test)
        else:
            valid_decision = model.decision_function(x_valid)
            valid_score = 1 / (1 + np.exp(-valid_decision))
            decision = model.decision_function(x_test)
            y_score = 1 / (1 + np.exp(-decision))
        threshold = find_best_threshold(y_valid, valid_score)
        metrics.append({"model": model_name, "threshold": threshold, **evaluate_scores(y_test, y_score, threshold)})
        per_label_reports[model_name] = classification_report(
            y_test,
            (y_score >= threshold).astype(int),
            target_names=labels,
            zero_division=0,
        )

    quantum_models = {
        "quantum_inspired_projection": QuantumInspiredNFRClassifier(threshold=args.threshold, random_state=args.seed),
        "quantum_contrastive_projection": QuantumInspiredContrastiveNFRClassifier(
            threshold=args.threshold,
            random_state=args.seed,
        ),
        "hybrid_quantum_svm_fusion": HybridQuantumSVMNFRClassifier(
            threshold=args.threshold,
            random_state=args.seed,
            quantum_weight=0.15,
        ),
    }
    quantum_model = None
    quantum_score = None
    quantum_pred = None
    for model_name, candidate in quantum_models.items():
        candidate.fit(list(x_train), y_train)
        valid_score = candidate.predict_proba(list(x_valid))
        threshold = find_best_threshold(y_valid, valid_score)
        y_score = candidate.predict_proba(list(x_test))
        y_pred = (y_score >= threshold).astype(int)
        metrics.append(
            {
                "model": model_name,
                "threshold": threshold,
                **evaluate_scores(y_test, y_score, threshold),
            }
        )
        per_label_reports[model_name] = classification_report(
            y_test,
            y_pred,
            target_names=labels,
            zero_division=0,
        )
        if model_name == "quantum_contrastive_projection":
            quantum_model = candidate
            quantum_score = y_score
            quantum_pred = y_pred

    example_index = next(
        (i for i in range(len(x_test)) if y_test[i].sum() > 1 and quantum_pred[i].sum() > 0),
        0,
    )
    if quantum_pred[example_index].sum() > 0:
        explanation_label_index = int(np.argmax(quantum_score[example_index]))
    else:
        explanation_label_index = int(np.argmax(y_test[example_index]))
    example = {
        "text": x_test[example_index],
        "true_labels": [labels[i] for i, value in enumerate(y_test[example_index]) if value == 1],
        "predicted_labels": [labels[i] for i, value in enumerate(quantum_pred[example_index]) if value == 1],
        "explanation_label": labels[explanation_label_index],
        "contributions": top_feature_contributions(
            quantum_model,
            x_test[example_index],
            explanation_label_index,
            top_k=10,
        ),
    }

    metrics_path = out_dir / "nice_multilabel_metrics.csv"
    report_path = out_dir / "nice_multilabel_report.md"
    metadata_path = out_dir / "nice_multilabel_metadata.json"

    pd.DataFrame(metrics).to_csv(metrics_path, index=False)
    write_report(report_path, raw_path, processed_path, data, labels, metrics, per_label_reports, example)
    metadata_path.write_text(
        json.dumps(
            {
                "source": str(raw_path),
                "processed": str(processed_path),
                "rows": int(len(data)),
                "labels": labels,
                "test_size": args.test_size,
                "default_threshold": args.threshold,
                "threshold_selection": "validation macro_f1 grid search from 0.05 to 0.95",
                "seed": args.seed,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote processed data: {processed_path}")
    print(f"Wrote metrics: {metrics_path}")
    print(f"Wrote report: {report_path}")
    print(pd.DataFrame(metrics).to_string(index=False))


if __name__ == "__main__":
    main()
