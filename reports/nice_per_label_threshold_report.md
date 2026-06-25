# NICE Per-label Threshold 5-fold Experiment

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Labels: `11`
- Folds: `5`
- Each label receives its own threshold selected on the validation split.
- This protocol is useful for imbalanced multi-label NFR classification.

## Mean Results

| model | micro_f1_mean | micro_f1_std | macro_f1_mean | macro_f1_std | weighted_f1_mean | weighted_f1_std | hamming_loss_mean | hamming_loss_std | label_ranking_average_precision_mean | label_ranking_average_precision_std | threshold_mean_mean | threshold_mean_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hybrid_quantum_svm_fusion | 0.6230 | 0.0747 | 0.5850 | 0.0250 | 0.6450 | 0.0325 | 0.1031 | 0.0496 | 0.8045 | 0.0268 | 0.4418 | 0.0325 |
| tfidf_linear_svm | 0.6085 | 0.0588 | 0.5640 | 0.0309 | 0.6361 | 0.0354 | 0.1057 | 0.0378 | 0.8056 | 0.0262 | 0.4491 | 0.0270 |
| tfidf_logistic_regression | 0.6219 | 0.0588 | 0.5629 | 0.0532 | 0.6257 | 0.0512 | 0.0967 | 0.0195 | 0.7990 | 0.0240 | 0.4455 | 0.0234 |

## Per-fold Results

| fold | model | threshold_mean | micro_f1 | macro_f1 | weighted_f1 | hamming_loss | label_ranking_average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | tfidf_logistic_regression | 0.4409 | 0.6754 | 0.6166 | 0.6700 | 0.0874 | 0.7987 |
| 1 | tfidf_linear_svm | 0.4409 | 0.6637 | 0.6006 | 0.6641 | 0.0897 | 0.8055 |
| 1 | hybrid_quantum_svm_fusion | 0.4500 | 0.6789 | 0.6155 | 0.6748 | 0.0826 | 0.8115 |
| 2 | tfidf_logistic_regression | 0.4182 | 0.6638 | 0.6220 | 0.6845 | 0.0933 | 0.8368 |
| 2 | tfidf_linear_svm | 0.4227 | 0.5347 | 0.5693 | 0.6731 | 0.1603 | 0.8460 |
| 2 | hybrid_quantum_svm_fusion | 0.3864 | 0.5077 | 0.5795 | 0.6583 | 0.1902 | 0.8425 |
| 3 | tfidf_logistic_regression | 0.4818 | 0.6286 | 0.5349 | 0.6039 | 0.0778 | 0.8028 |
| 3 | tfidf_linear_svm | 0.4591 | 0.6557 | 0.5729 | 0.6456 | 0.0754 | 0.8118 |
| 3 | hybrid_quantum_svm_fusion | 0.4500 | 0.6839 | 0.6063 | 0.6681 | 0.0730 | 0.8110 |
| 4 | tfidf_logistic_regression | 0.4500 | 0.6154 | 0.5381 | 0.6101 | 0.0957 | 0.7780 |
| 4 | tfidf_linear_svm | 0.4909 | 0.6310 | 0.5154 | 0.5979 | 0.0742 | 0.7805 |
| 4 | hybrid_quantum_svm_fusion | 0.4727 | 0.6554 | 0.5618 | 0.6264 | 0.0730 | 0.7764 |
| 5 | tfidf_logistic_regression | 0.4364 | 0.5263 | 0.5031 | 0.5599 | 0.1292 | 0.7785 |
| 5 | tfidf_linear_svm | 0.4318 | 0.5574 | 0.5618 | 0.5997 | 0.1292 | 0.7844 |
| 5 | hybrid_quantum_svm_fusion | 0.4500 | 0.5888 | 0.5617 | 0.5972 | 0.0969 | 0.7812 |

## Interpretation

- Higher F1 and LRAP are better.
- Lower Hamming loss is better.
- In this calibrated setting, the hybrid quantum model has the best Macro-F1 among the compared models.
