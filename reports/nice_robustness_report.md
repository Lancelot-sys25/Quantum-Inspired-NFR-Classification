# NICE Robustness and Explainability Comparison Report

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Split: same 70/30 train-test seed and internal validation protocol as the single-split experiment.
- Deletion comparison: contrastive projection intrinsic contributions versus SVM TF-IDF coefficient contributions.
- Bootstrap: paired bootstrap over held-out test requirements for Macro-F1 differences.

## Deletion Comparison Summary

| explainer | top_k | random_trials | evaluated_label_assignments | mean_base_score | mean_top_deleted_score | mean_random_deleted_score | mean_comprehensiveness | mean_random_comprehensiveness | mean_sufficiency | mean_random_sufficiency | comprehensiveness_ratio | sufficiency_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contrastive_projection_intrinsic | 3 | 50 | 158 | 0.4786 | 0.4481 | 0.4727 | 0.0305 | 0.0059 | -0.0395 | 0.0337 | 5.2085 | -1.1721 |
| svm_tfidf_coefficients | 3 | 50 | 158 | 0.4925 | 0.4058 | 0.4709 | 0.0867 | 0.0216 | 0.0484 | 0.1141 | 4.0142 | 0.4240 |

## Paired Bootstrap Summary

| comparison | iterations | observed_macro_f1_difference | ci95_low | ci95_high | bootstrap_p_two_sided |
| --- | --- | --- | --- | --- | --- |
| hybrid_quantum_svm_fusion_vs_tfidf_linear_svm | 2000 | 0.0081 | -0.0100 | 0.0263 | 0.3760 |
| hybrid_quantum_svm_fusion_vs_tfidf_logistic_regression | 2000 | 0.0020 | -0.0205 | 0.0227 | 0.9180 |
| hybrid_quantum_svm_fusion_vs_quantum_contrastive_projection | 2000 | 0.1401 | 0.0741 | 0.2127 | 0.0000 |
