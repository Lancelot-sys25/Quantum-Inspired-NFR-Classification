import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from quantum_re_nfr.quantum_model import QuantumInspiredContrastiveNFRClassifier
from run_nice_multilabel_experiment import load_nice_dataset, markdown_table, stratify_key


def normalized_states(model: QuantumInspiredContrastiveNFRClassifier, texts: np.ndarray) -> np.ndarray:
    vectors = model.vectorizer.transform(list(texts)).toarray()
    return model._normalize_states(vectors)


def label_score(model: QuantumInspiredContrastiveNFRClassifier, state: np.ndarray, label_index: int) -> float:
    amplitude = float(state @ model.label_basis_[label_index])
    rectified_projection = max(0.0, amplitude) ** 2
    raw = model.score_scale * rectified_projection + float(model.label_bias_[label_index])
    return float(model._sigmoid(raw))


def mask_and_renormalize(state: np.ndarray, indices: np.ndarray) -> np.ndarray:
    masked = state.copy()
    masked[indices] = 0.0
    norm = np.linalg.norm(masked)
    return masked / norm if norm else masked


def deletion_test(
    model: QuantumInspiredContrastiveNFRClassifier,
    x_test: np.ndarray,
    y_test: np.ndarray,
    labels: list[str],
    top_k: int,
    random_trials: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    states = normalized_states(model, x_test)
    feature_names = np.array(model.vectorizer.get_feature_names_out())
    rows = []

    for sample_index, state in enumerate(states):
        active_features = np.flatnonzero(state)
        if len(active_features) == 0:
            continue
        for label_index, label in enumerate(labels):
            if y_test[sample_index, label_index] != 1:
                continue

            contribution = state * model.label_basis_[label_index]
            ranked = np.argsort(np.abs(contribution))[::-1]
            top_indices = np.array([idx for idx in ranked if state[idx] != 0][:top_k])
            if len(top_indices) == 0:
                continue

            base_score = label_score(model, state, label_index)
            top_score = label_score(model, mask_and_renormalize(state, top_indices), label_index)
            random_scores = []
            random_k = min(len(top_indices), len(active_features))
            for _ in range(random_trials):
                random_indices = rng.choice(active_features, size=random_k, replace=False)
                random_scores.append(label_score(model, mask_and_renormalize(state, random_indices), label_index))

            rows.append(
                {
                    "sample_index": sample_index,
                    "label": label,
                    "base_score": base_score,
                    "top_deleted_score": top_score,
                    "random_deleted_score": float(np.mean(random_scores)),
                    "top_score_drop": base_score - top_score,
                    "random_score_drop": base_score - float(np.mean(random_scores)),
                    "top_terms": ", ".join(feature_names[top_indices]),
                }
            )

    detail = pd.DataFrame(rows)
    mean_top_drop = detail["top_score_drop"].mean()
    mean_random_drop = detail["random_score_drop"].mean()
    summary = pd.DataFrame(
        [
            {
                "evaluated_label_assignments": int(len(detail)),
                "top_k": top_k,
                "random_trials": random_trials,
                "mean_base_score": detail["base_score"].mean(),
                "mean_top_deleted_score": detail["top_deleted_score"].mean(),
                "mean_random_deleted_score": detail["random_deleted_score"].mean(),
                "mean_top_score_drop": mean_top_drop,
                "mean_random_score_drop": mean_random_drop,
                "drop_ratio_top_vs_random": mean_top_drop / mean_random_drop if mean_random_drop else np.nan,
            }
        ]
    )
    return detail, summary


def write_report(report_path: Path, raw_path: Path, detail: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# NICE Explainability Deletion-test Report",
        "",
        "## Setup",
        "",
        f"- Dataset: `{raw_path}`",
        "- Model: contrastive quantum-inspired projection",
        "- Evaluation: compare score drop after deleting top contribution terms with deleting random nonzero terms.",
        "",
        "## Summary",
        "",
        markdown_table(summary, float_digits=4),
        "",
        "## Example Rows",
        "",
        markdown_table(detail.head(20), float_digits=4),
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/PROMISE-relabeled-NICE.csv")
    parser.add_argument("--test-size", type=float, default=0.30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--random-trials", type=int, default=50)
    parser.add_argument("--out-dir", default="reports")
    args = parser.parse_args()

    raw_path = Path(args.data)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    data, labels = load_nice_dataset(raw_path)
    x = data["text"].to_numpy()
    y = data[labels].to_numpy(dtype=int)
    train_idx, test_idx = train_test_split(
        np.arange(len(data)),
        test_size=args.test_size,
        random_state=args.seed,
        stratify=stratify_key(y, labels),
    )
    x_train, x_test = x[train_idx], x[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    model = QuantumInspiredContrastiveNFRClassifier(random_state=args.seed)
    model.fit(list(x_train), y_train)
    detail, summary = deletion_test(
        model=model,
        x_test=x_test,
        y_test=y_test,
        labels=labels,
        top_k=args.top_k,
        random_trials=args.random_trials,
        seed=args.seed,
    )

    detail_path = out_dir / "nice_explainability_deletion_detail.csv"
    summary_path = out_dir / "nice_explainability_deletion_summary.csv"
    report_path = out_dir / "nice_explainability_deletion_report.md"
    metadata_path = out_dir / "nice_explainability_deletion_metadata.json"

    detail.to_csv(detail_path, index=False)
    summary.to_csv(summary_path, index=False)
    write_report(report_path, raw_path, detail, summary)
    metadata_path.write_text(
        json.dumps(
            {
                "source": str(raw_path),
                "model": "quantum_contrastive_projection",
                "test_size": args.test_size,
                "seed": args.seed,
                "top_k": args.top_k,
                "random_trials": args.random_trials,
                "labels": labels,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote detail: {detail_path}")
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote report: {report_path}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
