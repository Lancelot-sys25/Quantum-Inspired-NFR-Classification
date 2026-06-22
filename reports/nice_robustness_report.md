# NICE Robustness and Explainability Comparison Report

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Split: same 70/30 train-test seed and internal validation protocol as the single-split experiment.
- Deletion comparison: projection intrinsic contributions versus SVM TF-IDF coefficient contributions.
- Bootstrap: paired bootstrap over held-out test requirements for Macro-F1 differences.

## Deletion Comparison Summary

| explainer | top_k | random_trials | evaluated_label_assignments | mean_base_score | mean_top_deleted_score | mean_random_deleted_score | mean_top_score_drop | mean_random_score_drop | drop_ratio_top_vs_random |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| projection_intrinsic | 3 | 50 | 158 | 0.6577 | 0.5413 | 0.6435 | 0.1165 | 0.0143 | 8.1673 |
| svm_tfidf_coefficients | 3 | 50 | 158 | 0.4925 | 0.4058 | 0.4713 | 0.0867 | 0.0212 | 4.0892 |

## Paired Bootstrap Summary

| comparison | iterations | observed_macro_f1_difference | ci95_low | ci95_high | bootstrap_p_two_sided |
| --- | --- | --- | --- | --- | --- |
| hybrid_quantum_svm_fusion_vs_tfidf_linear_svm | 2000 | 0.0814 | -0.0039 | 0.1541 | 0.0700 |
| hybrid_quantum_svm_fusion_vs_tfidf_logistic_regression | 2000 | 0.0753 | -0.0147 | 0.1533 | 0.1400 |
| hybrid_quantum_svm_fusion_vs_quantum_contrastive_projection | 2000 | 0.0652 | 0.0002 | 0.1163 | 0.0480 |
