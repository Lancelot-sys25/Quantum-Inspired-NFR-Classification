from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import nct, rankdata, t, ttest_rel, wilcoxon


def paired_t_power(n: int, effect_size: float, alpha: float = 0.05) -> float:
    """Power of an idealized two-sided paired t-test for Cohen's d_z."""
    degrees_of_freedom = n - 1
    critical_value = t.ppf(1 - alpha / 2, degrees_of_freedom)
    noncentrality = abs(effect_size) * math.sqrt(n)
    return float(
        nct.sf(critical_value, degrees_of_freedom, noncentrality)
        + nct.cdf(-critical_value, degrees_of_freedom, noncentrality)
    )


def minimum_pairs_for_power(
    effect_size: float,
    alpha: float = 0.05,
    target_power: float = 0.80,
    maximum_n: int = 10_000,
) -> tuple[int, float]:
    for n in range(2, maximum_n + 1):
        power = paired_t_power(n, effect_size, alpha)
        if power >= target_power:
            return n, power
    raise RuntimeError(f"Target power was not reached by n={maximum_n}.")


def rank_biserial_from_differences(differences: np.ndarray) -> float:
    nonzero = differences[differences != 0]
    if len(nonzero) == 0:
        return 0.0
    ranks = rankdata(np.abs(nonzero))
    positive = ranks[nonzero > 0].sum()
    negative = ranks[nonzero < 0].sum()
    return float((positive - negative) / (positive + negative))


def model_values(frame: pd.DataFrame, model: str) -> np.ndarray:
    rows = frame.loc[frame["model"] == model].sort_values("fold")
    if rows.empty:
        raise ValueError(f"Model not found: {model}")
    if rows["fold"].duplicated().any():
        raise ValueError(f"Duplicate folds for model: {model}")
    return rows["macro_f1"].to_numpy(dtype=float)


def comparison_row(
    name: str,
    left: np.ndarray,
    right: np.ndarray,
) -> dict[str, float | int | str]:
    if len(left) != len(right):
        raise ValueError(f"Unpaired input lengths for {name}: {len(left)} and {len(right)}")
    differences = left - right
    standard_deviation = float(differences.std(ddof=1))
    effect_size = float(differences.mean() / standard_deviation) if standard_deviation else 0.0
    return {
        "name": name,
        "n": len(differences),
        "mean_diff": float(differences.mean()),
        "std_diff": standard_deviation,
        "dz": effect_size,
        "rbc": rank_biserial_from_differences(differences),
        "w_p": float(wilcoxon(differences, alternative="two-sided").pvalue),
        "t_p": float(ttest_rel(left, right).pvalue),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cv-results", default="reports/nice_cv_fold_results.csv")
    parser.add_argument("--ablation-results", default="reports/nice_ablation_fold_results.csv")
    parser.add_argument("--out-dir", default="reports")
    parser.add_argument("--power-effect-size", type=float, default=0.5)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--target-power", type=float, default=0.80)
    args = parser.parse_args()

    cv = pd.read_csv(args.cv_results)
    ablation = pd.read_csv(args.ablation_results)

    comparisons = [
        (
            "Hybrid vs TF-IDF Linear SVM (main text)",
            model_values(cv, "hybrid_quantum_svm_fusion"),
            model_values(cv, "tfidf_linear_svm"),
        ),
        (
            "Hybrid vs TF-IDF Logistic Regression (main text)",
            model_values(cv, "hybrid_quantum_svm_fusion"),
            model_values(cv, "tfidf_logistic_regression"),
        ),
        (
            "Hybrid vs Sentence-BERT (main text)",
            model_values(cv, "hybrid_quantum_svm_fusion"),
            model_values(cv, "sentence_bert_logistic_regression"),
        ),
        (
            "ISOLATED QUANTUM CONTRIBUTION: Hybrid a=0.30 vs SVM-only (same TF-IDF backbone)",
            model_values(ablation, "hybrid_alpha_0_30"),
            model_values(ablation, "svm_only_sublinear_tfidf"),
        ),
        (
            "Hybrid vs pure Quantum Contrastive Projection (value of fusion)",
            model_values(ablation, "hybrid_alpha_0_30"),
            model_values(ablation, "contrastive_projection_with_interference"),
        ),
        (
            "Pure Quantum Contrastive Projection vs TF-IDF Linear SVM (quantum alone)",
            model_values(cv, "quantum_contrastive_projection"),
            model_values(cv, "tfidf_linear_svm"),
        ),
        (
            "Pure Quantum Positive Projection vs TF-IDF Linear SVM (quantum alone)",
            model_values(cv, "quantum_inspired_projection"),
            model_values(cv, "tfidf_linear_svm"),
        ),
        (
            "Interference effect on Positive Projection",
            model_values(ablation, "positive_projection_with_interference"),
            model_values(ablation, "positive_projection_no_interference"),
        ),
        (
            "Interference effect on Contrastive Projection",
            model_values(ablation, "contrastive_projection_with_interference"),
            model_values(ablation, "contrastive_projection_no_interference"),
        ),
    ]
    effect_sizes = pd.DataFrame(comparison_row(name, left, right) for name, left, right in comparisons)

    required_pairs, achieved_power = minimum_pairs_for_power(
        args.power_effect_size,
        alpha=args.alpha,
        target_power=args.target_power,
    )
    power_summary = pd.DataFrame(
        [
            {
                "test": "two-sided paired t-test",
                "effect_size_dz": args.power_effect_size,
                "alpha": args.alpha,
                "target_power": args.target_power,
                "minimum_independent_pairs": required_pairs,
                "achieved_power": achieved_power,
            }
        ]
    )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    effect_path = out_dir / "quantum_contribution_effect_sizes.csv"
    power_path = out_dir / "power_analysis.csv"
    effect_sizes.to_csv(effect_path, index=False)
    power_summary.to_csv(power_path, index=False)

    print(effect_sizes.to_string(index=False))
    print()
    print(power_summary.to_string(index=False))
    print(
        "\nCaution: the power calculation assumes independent paired observations; "
        "cross-validation folds from one dataset are dependent."
    )
    print(f"\nWrote: {effect_path}")
    print(f"Wrote: {power_path}")


if __name__ == "__main__":
    main()
