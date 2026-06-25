# NICE Multi-label Cross-validation Report

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Labels: `11`
- Folds: `5`
- Threshold is selected on an internal validation split inside each training fold.

## Mean Results

| model | micro_f1_mean | micro_f1_std | macro_f1_mean | macro_f1_std | weighted_f1_mean | weighted_f1_std | hamming_loss_mean | hamming_loss_std | label_ranking_average_precision_mean | label_ranking_average_precision_std | threshold_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hybrid_quantum_svm_fusion | 0.6881 | 0.0325 | 0.6112 | 0.0301 | 0.6700 | 0.0289 | 0.0749 | 0.0076 | 0.8045 | 0.0268 | 0.4500 |
| tfidf_linear_svm | 0.6821 | 0.0405 | 0.6049 | 0.0336 | 0.6650 | 0.0353 | 0.0764 | 0.0094 | 0.8056 | 0.0262 | 0.4500 |
| tfidf_logistic_regression | 0.6787 | 0.0463 | 0.5977 | 0.0229 | 0.6590 | 0.0367 | 0.0759 | 0.0140 | 0.7990 | 0.0240 | 0.4700 |
| quantum_inspired_projection | 0.5931 | 0.0166 | 0.5490 | 0.0237 | 0.5936 | 0.0138 | 0.1096 | 0.0213 | 0.7830 | 0.0304 | 0.7800 |
| quantum_contrastive_projection | 0.4924 | 0.0537 | 0.5144 | 0.0387 | 0.5408 | 0.0468 | 0.1751 | 0.0352 | 0.7185 | 0.0538 | 0.4500 |
| label_frequency_baseline | 0.2328 | 0.0034 | 0.2083 | 0.0032 | 0.2594 | 0.0053 | 0.7927 | 0.0019 | 0.4059 | 0.0110 | 0.0500 |

## Per-fold Results

| fold | model | threshold | micro_f1 | macro_f1 | weighted_f1 | hamming_loss | label_ranking_average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | label_frequency_baseline | 0.0500 | 0.2369 | 0.2125 | 0.2597 | 0.7910 | 0.4038 |
| 1 | tfidf_logistic_regression | 0.4500 | 0.7196 | 0.6217 | 0.6958 | 0.0708 | 0.7987 |
| 1 | tfidf_linear_svm | 0.4500 | 0.7136 | 0.6169 | 0.6923 | 0.0720 | 0.8055 |
| 1 | quantum_inspired_projection | 0.9500 | 0.6082 | 0.5584 | 0.6071 | 0.0897 | 0.7956 |
| 1 | quantum_contrastive_projection | 0.4500 | 0.4969 | 0.5623 | 0.5836 | 0.1913 | 0.7840 |
| 1 | hybrid_quantum_svm_fusion | 0.4500 | 0.7170 | 0.6229 | 0.6958 | 0.0708 | 0.8115 |
| 2 | label_frequency_baseline | 0.0500 | 0.2358 | 0.2109 | 0.2638 | 0.7907 | 0.4137 |
| 2 | tfidf_logistic_regression | 0.5000 | 0.7363 | 0.6202 | 0.7000 | 0.0574 | 0.8368 |
| 2 | tfidf_linear_svm | 0.4500 | 0.7337 | 0.6422 | 0.7100 | 0.0634 | 0.8460 |
| 2 | quantum_inspired_projection | 0.5500 | 0.5776 | 0.5248 | 0.5745 | 0.1400 | 0.8280 |
| 2 | quantum_contrastive_projection | 0.4500 | 0.5760 | 0.5499 | 0.5965 | 0.1268 | 0.7697 |
| 2 | hybrid_quantum_svm_fusion | 0.4500 | 0.7255 | 0.6392 | 0.7027 | 0.0670 | 0.8425 |
| 3 | label_frequency_baseline | 0.0500 | 0.2300 | 0.2051 | 0.2628 | 0.7931 | 0.3948 |
| 3 | tfidf_logistic_regression | 0.5000 | 0.6347 | 0.5770 | 0.6200 | 0.0730 | 0.8028 |
| 3 | tfidf_linear_svm | 0.4500 | 0.6702 | 0.6099 | 0.6554 | 0.0754 | 0.8118 |
| 3 | quantum_inspired_projection | 0.8500 | 0.6030 | 0.5856 | 0.5983 | 0.0945 | 0.7798 |
| 3 | quantum_contrastive_projection | 0.4500 | 0.4980 | 0.4931 | 0.5281 | 0.1495 | 0.6758 |
| 3 | hybrid_quantum_svm_fusion | 0.4500 | 0.6842 | 0.6265 | 0.6684 | 0.0718 | 0.8110 |
| 4 | label_frequency_baseline | 0.0500 | 0.2317 | 0.2071 | 0.2605 | 0.7931 | 0.4205 |
| 4 | tfidf_logistic_regression | 0.4500 | 0.6602 | 0.5736 | 0.6462 | 0.0837 | 0.7780 |
| 4 | tfidf_linear_svm | 0.4500 | 0.6359 | 0.5506 | 0.6247 | 0.0849 | 0.7805 |
| 4 | quantum_inspired_projection | 0.8500 | 0.6038 | 0.5377 | 0.6038 | 0.1005 | 0.7593 |
| 4 | quantum_contrastive_projection | 0.4500 | 0.4525 | 0.4780 | 0.4971 | 0.1998 | 0.6897 |
| 4 | hybrid_quantum_svm_fusion | 0.4500 | 0.6598 | 0.5618 | 0.6403 | 0.0789 | 0.7764 |
| 5 | label_frequency_baseline | 0.0500 | 0.2294 | 0.2060 | 0.2504 | 0.7955 | 0.3967 |
| 5 | tfidf_logistic_regression | 0.4500 | 0.6425 | 0.5961 | 0.6331 | 0.0945 | 0.7785 |
| 5 | tfidf_linear_svm | 0.4500 | 0.6571 | 0.6049 | 0.6426 | 0.0861 | 0.7844 |
| 5 | quantum_inspired_projection | 0.7000 | 0.5726 | 0.5385 | 0.5843 | 0.1232 | 0.7522 |
| 5 | quantum_contrastive_projection | 0.4500 | 0.4387 | 0.4885 | 0.4990 | 0.2081 | 0.6736 |
| 5 | hybrid_quantum_svm_fusion | 0.4500 | 0.6538 | 0.6057 | 0.6429 | 0.0861 | 0.7812 |

## Paired Statistical Tests

| comparison | folds | wilcoxon_statistic | p_value | mean_macro_f1_difference |
| --- | --- | --- | --- | --- |
| hybrid_quantum_svm_fusion_vs_tfidf_linear_svm | 5 | 2.0000 | 0.1875 | 0.0063 |
| hybrid_quantum_svm_fusion_vs_tfidf_logistic_regression | 5 | 3.0000 | 0.3125 | 0.0135 |

## Reading the Results

- Higher `micro_f1`, `macro_f1`, `weighted_f1`, and `label_ranking_average_precision` are better.
- Lower `hamming_loss` is better.
- `macro_f1` is the most important score here because the NFR labels are imbalanced.
