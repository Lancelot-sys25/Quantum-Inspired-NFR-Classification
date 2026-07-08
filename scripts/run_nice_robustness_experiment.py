import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from quantum_re_nfr.quantum_model import HybridQuantumSVMNFRClassifier, QuantumInspiredContrastiveNFRClassifier
from run_nice_multilabel_experiment import (
    evaluate_scores,
    find_best_threshold,
    load_nice_dataset,
    markdown_table,
    stratify_key,
)


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def model_scores(model, x_valid: np.ndarray, x_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if hasattr(model, "predict_proba"):
        return model.predict_proba(x_valid), model.predict_proba(x_test)
    return sigmoid(model.decision_function(x_valid)), sigmoid(model.decision_function(x_test))


def normalized_states(model: QuantumInspiredContrastiveNFRClassifier, texts: np.ndarray) -> np.ndarray:
    vectors = model.vectorizer.transform(list(texts)).toarray()
    return model._normalize_states(vectors)


def projection_label_score(model: QuantumInspiredContrastiveNFRClassifier, state: np.ndarray, label_index: int) -> float:
    amplitude = float(state @ model.label_basis_[label_index])
    rectified_projection = max(0.0, amplitude) ** 2
    raw = model.score_scale * rectified_projection + float(model.label_bias_[label_index])
    return float(model._sigmoid(raw))


def mask_and_renormalize(state: np.ndarray, indices: np.ndarray) -> np.ndarray:
    masked = state.copy()
    masked[indices] = 0.0
    norm = np.linalg.norm(masked)
    return masked / norm if norm else masked


def keep_only_and_renormalize(state: np.ndarray, indices: np.ndarray) -> np.ndarray:
    masked = np.zeros_like(state)
    masked[indices] = state[indices]
    norm = np.linalg.norm(masked)
    return masked / norm if norm else masked


def deletion_comparison(
    projection_model: QuantumInspiredContrastiveNFRClassifier,
    svm_model: OneVsRestClassifier,
    x_test: np.ndarray,
    y_test: np.ndarray,
    labels: list[str],
    top_k: int,
    random_trials: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    states = normalized_states(projection_model, x_test)
    feature_names = np.array(projection_model.vectorizer.get_feature_names_out())
    svm_vectorizers = [estimator.named_steps["tfidf"] for estimator in svm_model.estimators_]
    svm_classifiers = [estimator.named_steps["clf"] for estimator in svm_model.estimators_]
    rows = []

    for sample_index, state in enumerate(states):
        active_projection_features = np.flatnonzero(state)
        if len(active_projection_features) == 0:
            continue

        for label_index, label in enumerate(labels):
            if y_test[sample_index, label_index] != 1:
                continue

            contribution = state * projection_model.label_basis_[label_index]
            ranked = np.argsort(np.abs(contribution))[::-1]
            top_indices = np.array([idx for idx in ranked if state[idx] != 0][:top_k])
            if len(top_indices) == 0:
                continue

            base_score = projection_label_score(projection_model, state, label_index)
            top_score = projection_label_score(
                projection_model,
                mask_and_renormalize(state, top_indices),
                label_index,
            )
            random_k = min(len(top_indices), len(active_projection_features))
            random_scores = []
            for _ in range(random_trials):
                random_indices = rng.choice(active_projection_features, size=random_k, replace=False)
                random_scores.append(
                    projection_label_score(
                        projection_model,
                        mask_and_renormalize(state, random_indices),
                        label_index,
                    )
                )

            # ERASER Sufficiency for projection
            sufficiency_score = projection_label_score(
                projection_model,
                keep_only_and_renormalize(state, top_indices),
                label_index,
            )
            random_sufficiency_scores = []
            for _ in range(random_trials):
                random_indices = rng.choice(active_projection_features, size=random_k, replace=False)
                random_sufficiency_scores.append(
                    projection_label_score(
                        projection_model,
                        keep_only_and_renormalize(state, random_indices),
                        label_index,
                    )
                )
            random_sufficiency_score = float(np.mean(random_sufficiency_scores))

            rows.append(
                {
                    "sample_index": sample_index,
                    "label": label,
                    "explainer": "contrastive_projection_intrinsic",
                    "base_score": base_score,
                    "top_deleted_score": top_score,
                    "random_deleted_score": float(np.mean(random_scores)),
                    "comprehensiveness": base_score - top_score,
                    "random_comprehensiveness": base_score - float(np.mean(random_scores)),
                    "sufficiency": base_score - sufficiency_score,
                    "random_sufficiency": base_score - random_sufficiency_score,
                    "top_terms": ", ".join(feature_names[top_indices]),
                }
            )

            vectorizer = svm_vectorizers[label_index]
            classifier = svm_classifiers[label_index]
            vector = vectorizer.transform([x_test[sample_index]])
            active_svm_features = vector.nonzero()[1]
            if len(active_svm_features) == 0:
                continue
            scores = np.asarray(vector.multiply(classifier.coef_).toarray()).ravel()
            svm_ranked = np.argsort(np.abs(scores))[::-1]
            svm_top_indices = np.array([idx for idx in svm_ranked if vector[0, idx] != 0][:top_k])
            if len(svm_top_indices) == 0:
                continue

            base_decision = float(classifier.decision_function(vector)[0])
            base_svm_score = float(sigmoid(np.array(base_decision)))
            top_vector = vector.copy().tolil()
            top_vector[0, svm_top_indices] = 0
            top_vector = top_vector.tocsr()
            top_svm_score = float(sigmoid(np.array(classifier.decision_function(top_vector)[0])))
            random_svm_scores = []
            svm_random_k = min(len(svm_top_indices), len(active_svm_features))
            for _ in range(random_trials):
                random_indices = rng.choice(active_svm_features, size=svm_random_k, replace=False)
                random_vector = vector.copy().tolil()
                random_vector[0, random_indices] = 0
                random_vector = random_vector.tocsr()
                random_svm_scores.append(float(sigmoid(np.array(classifier.decision_function(random_vector)[0]))))

            # ERASER Sufficiency for SVM
            sufficiency_vector = vector.copy().tolil()
            active_set = set(active_svm_features)
            top_set = set(svm_top_indices)
            for idx in active_set - top_set:
                sufficiency_vector[0, idx] = 0
            sufficiency_vector = sufficiency_vector.tocsr()
            sufficiency_svm_score = float(sigmoid(np.array(classifier.decision_function(sufficiency_vector)[0])))

            random_svm_sufficiency_scores = []
            for _ in range(random_trials):
                random_indices = rng.choice(active_svm_features, size=svm_random_k, replace=False)
                random_sufficiency_vector = vector.copy().tolil()
                for idx in active_set - set(random_indices):
                    random_sufficiency_vector[0, idx] = 0
                random_sufficiency_vector = random_sufficiency_vector.tocsr()
                random_svm_sufficiency_scores.append(
                    float(sigmoid(np.array(classifier.decision_function(random_sufficiency_vector)[0])))
                )
            random_svm_sufficiency_score = float(np.mean(random_svm_sufficiency_scores))

            svm_feature_names = np.array(vectorizer.get_feature_names_out())
            rows.append(
                {
                    "sample_index": sample_index,
                    "label": label,
                    "explainer": "svm_tfidf_coefficients",
                    "base_score": base_svm_score,
                    "top_deleted_score": top_svm_score,
                    "random_deleted_score": float(np.mean(random_svm_scores)),
                    "comprehensiveness": base_svm_score - top_svm_score,
                    "random_comprehensiveness": base_svm_score - float(np.mean(random_svm_scores)),
                    "sufficiency": base_svm_score - sufficiency_svm_score,
                    "random_sufficiency": base_svm_score - random_svm_sufficiency_score,
                    "top_terms": ", ".join(svm_feature_names[svm_top_indices]),
                }
            )

    detail = pd.DataFrame(rows)
    summary = (
        detail.groupby("explainer")
        .agg(
            evaluated_label_assignments=("comprehensiveness", "count"),
            mean_base_score=("base_score", "mean"),
            mean_top_deleted_score=("top_deleted_score", "mean"),
            mean_random_deleted_score=("random_deleted_score", "mean"),
            mean_comprehensiveness=("comprehensiveness", "mean"),
            mean_random_comprehensiveness=("random_comprehensiveness", "mean"),
            mean_sufficiency=("sufficiency", "mean"),
            mean_random_sufficiency=("random_sufficiency", "mean"),
        )
        .reset_index()
    )
    summary["comprehensiveness_ratio"] = summary["mean_comprehensiveness"] / summary["mean_random_comprehensiveness"]
    summary["sufficiency_ratio"] = summary["mean_sufficiency"] / summary["mean_random_sufficiency"]
    summary.insert(1, "top_k", top_k)
    summary.insert(2, "random_trials", random_trials)
    return detail, summary


def paired_bootstrap(
    y_true: np.ndarray,
    model_scores_by_name: dict[str, np.ndarray],
    thresholds_by_name: dict[str, float],
    reference: str,
    comparisons: list[str],
    iterations: int,
    seed: int,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    n = len(y_true)

    reference_pred = (model_scores_by_name[reference] >= thresholds_by_name[reference]).astype(int)
    reference_macro = f1_score(y_true, reference_pred, average="macro", zero_division=0)

    for model_name in comparisons:
        if model_name not in model_scores_by_name:
            continue
        comparison_pred = (model_scores_by_name[model_name] >= thresholds_by_name[model_name]).astype(int)
        comparison_macro = f1_score(y_true, comparison_pred, average="macro", zero_division=0)
        observed_diff = reference_macro - comparison_macro
        diffs = []
        for _ in range(iterations):
            indices = rng.integers(0, n, size=n)
            reference_sample = f1_score(
                y_true[indices],
                reference_pred[indices],
                average="macro",
                zero_division=0,
            )
            comparison_sample = f1_score(
                y_true[indices],
                comparison_pred[indices],
                average="macro",
                zero_division=0,
            )
            diffs.append(reference_sample - comparison_sample)
        diffs = np.array(diffs)
        rows.append(
            {
                "comparison": f"{reference}_vs_{model_name}",
                "iterations": iterations,
                "observed_macro_f1_difference": observed_diff,
                "ci95_low": float(np.quantile(diffs, 0.025)),
                "ci95_high": float(np.quantile(diffs, 0.975)),
                "bootstrap_p_two_sided": float(2 * min(np.mean(diffs <= 0), np.mean(diffs >= 0))),
            }
        )
    return pd.DataFrame(rows)


def write_report(
    report_path: Path,
    raw_path: Path,
    deletion_summary: pd.DataFrame,
    bootstrap: pd.DataFrame,
) -> None:
    lines = [
        "# NICE Robustness and Explainability Comparison Report",
        "",
        "## Setup",
        "",
        f"- Dataset: `{raw_path}`",
        "- Split: same 70/30 train-test seed and internal validation protocol as the single-split experiment.",
        "- Deletion comparison: contrastive projection intrinsic contributions versus SVM TF-IDF coefficient contributions.",
        "- Bootstrap: paired bootstrap over held-out test requirements for Macro-F1 differences.",
        "",
        "## Deletion Comparison Summary",
        "",
        markdown_table(deletion_summary, float_digits=4),
        "",
        "## Paired Bootstrap Summary",
        "",
        markdown_table(bootstrap, float_digits=4),
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
    parser.add_argument("--bootstrap-iterations", type=int, default=2000)
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
    train_idx, valid_idx = train_test_split(
        train_idx,
        test_size=0.20,
        random_state=args.seed,
        stratify=stratify_key(y[train_idx], labels),
    )

    x_train, x_valid, x_test = x[train_idx], x[valid_idx], x[test_idx]
    y_train, y_valid, y_test = y[train_idx], y[valid_idx], y[test_idx]

    svm_model = OneVsRestClassifier(
        Pipeline(
            [
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
                ("clf", LinearSVC(class_weight="balanced", dual="auto", random_state=args.seed)),
            ]
        )
    )
    logistic_model = OneVsRestClassifier(
        Pipeline(
            [
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
                ("clf", LogisticRegression(max_iter=3000, class_weight="balanced")),
            ]
        )
    )
    projection_model = QuantumInspiredContrastiveNFRClassifier(random_state=args.seed)
    hybrid_model = HybridQuantumSVMNFRClassifier(random_state=args.seed, quantum_weight=0.30)

    models = {
        "tfidf_logistic_regression": logistic_model,
        "tfidf_linear_svm": svm_model,
        "quantum_contrastive_projection": projection_model,
        "hybrid_quantum_svm_fusion": hybrid_model,
    }

    scores_by_name = {}
    thresholds_by_name = {}
    metrics_rows = []
    for model_name, model in models.items():
        if model_name.startswith("quantum") or model_name.startswith("hybrid"):
            model.fit(list(x_train), y_train)
            valid_score = model.predict_proba(list(x_valid))
            test_score = model.predict_proba(list(x_test))
        else:
            model.fit(x_train, y_train)
            valid_score, test_score = model_scores(model, x_valid, x_test)
        threshold = find_best_threshold(y_valid, valid_score)
        scores_by_name[model_name] = test_score
        thresholds_by_name[model_name] = threshold
        metrics_rows.append({"model": model_name, "threshold": threshold, **evaluate_scores(y_test, test_score, threshold)})

    deletion_detail, deletion_summary = deletion_comparison(
        projection_model=projection_model,
        svm_model=svm_model,
        x_test=x_test,
        y_test=y_test,
        labels=labels,
        top_k=args.top_k,
        random_trials=args.random_trials,
        seed=args.seed,
    )
    bootstrap = paired_bootstrap(
        y_true=y_test,
        model_scores_by_name=scores_by_name,
        thresholds_by_name=thresholds_by_name,
        reference="hybrid_quantum_svm_fusion",
        comparisons=["tfidf_linear_svm", "tfidf_logistic_regression", "quantum_contrastive_projection"],
        iterations=args.bootstrap_iterations,
        seed=args.seed,
    )

    deletion_detail.to_csv(out_dir / "nice_deletion_comparison_detail.csv", index=False)
    deletion_summary.to_csv(out_dir / "nice_deletion_comparison_summary.csv", index=False)
    bootstrap.to_csv(out_dir / "nice_paired_bootstrap_summary.csv", index=False)
    pd.DataFrame(metrics_rows).to_csv(out_dir / "nice_robustness_split_metrics.csv", index=False)
    write_report(out_dir / "nice_robustness_report.md", raw_path, deletion_summary, bootstrap)
    (out_dir / "nice_robustness_metadata.json").write_text(
        json.dumps(
            {
                "source": str(raw_path),
                "test_size": args.test_size,
                "seed": args.seed,
                "top_k": args.top_k,
                "random_trials": args.random_trials,
                "bootstrap_iterations": args.bootstrap_iterations,
                "labels": labels,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Deletion comparison")
    print(deletion_summary.to_string(index=False))
    print()
    print("Paired bootstrap")
    print(bootstrap.to_string(index=False))


if __name__ == "__main__":
    main()
