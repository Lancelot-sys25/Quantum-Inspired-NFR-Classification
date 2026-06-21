# NICE Multi-label Cross-validation Report

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Labels: `11`
- Folds: `5`
- Threshold is selected on an internal validation split inside each training fold.

## Mean Results

| model | micro_f1_mean | micro_f1_std | macro_f1_mean | macro_f1_std | weighted_f1_mean | weighted_f1_std | hamming_loss_mean | hamming_loss_std | label_ranking_average_precision_mean | label_ranking_average_precision_std | threshold_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sentence_bert_logistic_regression | 0.6493 | 0.0357 | 0.6121 | 0.0450 | 0.6526 | 0.0354 | 0.0919 | 0.0200 | 0.8361 | 0.0225 | 0.5400 |
| tfidf_linear_svm | 0.6821 | 0.0405 | 0.6049 | 0.0336 | 0.6650 | 0.0353 | 0.0764 | 0.0094 | 0.8056 | 0.0262 | 0.4500 |
| hybrid_quantum_svm_fusion | 0.6739 | 0.0432 | 0.6000 | 0.0318 | 0.6582 | 0.0392 | 0.0742 | 0.0099 | 0.8075 | 0.0259 | 0.4900 |
| tfidf_logistic_regression | 0.6787 | 0.0463 | 0.5977 | 0.0229 | 0.6590 | 0.0367 | 0.0759 | 0.0140 | 0.7990 | 0.0240 | 0.4700 |
| quantum_contrastive_projection | 0.6145 | 0.0493 | 0.5602 | 0.0416 | 0.6093 | 0.0496 | 0.0873 | 0.0116 | 0.7775 | 0.0320 | 0.6400 |
| quantum_inspired_projection | 0.5931 | 0.0166 | 0.5490 | 0.0237 | 0.5936 | 0.0138 | 0.1096 | 0.0213 | 0.7830 | 0.0304 | 0.7800 |
| label_frequency_baseline | 0.2328 | 0.0034 | 0.2083 | 0.0032 | 0.2594 | 0.0053 | 0.7927 | 0.0019 | 0.4059 | 0.0110 | 0.0500 |

## Per-fold Results

| fold | model | threshold | micro_f1 | macro_f1 | weighted_f1 | hamming_loss | label_ranking_average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | label_frequency_baseline | 0.0500 | 0.2369 | 0.2125 | 0.2597 | 0.7910 | 0.4038 |
| 1 | tfidf_logistic_regression | 0.4500 | 0.7196 | 0.6217 | 0.6958 | 0.0708 | 0.7987 |
| 1 | tfidf_linear_svm | 0.4500 | 0.7136 | 0.6169 | 0.6923 | 0.0720 | 0.8055 |
| 1 | quantum_inspired_projection | 0.9500 | 0.6082 | 0.5584 | 0.6071 | 0.0897 | 0.7956 |
| 1 | quantum_contrastive_projection | 0.6000 | 0.6368 | 0.5799 | 0.6437 | 0.0956 | 0.7911 |
| 1 | hybrid_quantum_svm_fusion | 0.4500 | 0.6979 | 0.6278 | 0.6942 | 0.0838 | 0.8122 |
| 1 | sentence_bert_logistic_regression | 0.6000 | 0.6869 | 0.6414 | 0.6858 | 0.0732 | 0.8296 |
| 2 | label_frequency_baseline | 0.0500 | 0.2358 | 0.2109 | 0.2638 | 0.7907 | 0.4137 |
| 2 | tfidf_logistic_regression | 0.5000 | 0.7363 | 0.6202 | 0.7000 | 0.0574 | 0.8368 |
| 2 | tfidf_linear_svm | 0.4500 | 0.7337 | 0.6422 | 0.7100 | 0.0634 | 0.8460 |
| 2 | quantum_inspired_projection | 0.5500 | 0.5776 | 0.5248 | 0.5745 | 0.1400 | 0.8280 |
| 2 | quantum_contrastive_projection | 0.6500 | 0.6848 | 0.6035 | 0.6754 | 0.0694 | 0.8256 |
| 2 | hybrid_quantum_svm_fusion | 0.5000 | 0.7302 | 0.6164 | 0.6982 | 0.0610 | 0.8445 |
| 2 | sentence_bert_logistic_regression | 0.5000 | 0.6667 | 0.6352 | 0.6726 | 0.0921 | 0.8331 |
| 3 | label_frequency_baseline | 0.0500 | 0.2300 | 0.2051 | 0.2628 | 0.7931 | 0.3948 |
| 3 | tfidf_logistic_regression | 0.5000 | 0.6347 | 0.5770 | 0.6200 | 0.0730 | 0.8028 |
| 3 | tfidf_linear_svm | 0.4500 | 0.6702 | 0.6099 | 0.6554 | 0.0754 | 0.8118 |
| 3 | quantum_inspired_projection | 0.8500 | 0.6030 | 0.5856 | 0.5983 | 0.0945 | 0.7798 |
| 3 | quantum_contrastive_projection | 0.6500 | 0.6145 | 0.5809 | 0.6001 | 0.0825 | 0.7700 |
| 3 | hybrid_quantum_svm_fusion | 0.5000 | 0.6782 | 0.6145 | 0.6626 | 0.0670 | 0.8154 |
| 3 | sentence_bert_logistic_regression | 0.5500 | 0.6701 | 0.6379 | 0.6727 | 0.0778 | 0.8613 |
| 4 | label_frequency_baseline | 0.0500 | 0.2317 | 0.2071 | 0.2605 | 0.7931 | 0.4205 |
| 4 | tfidf_logistic_regression | 0.4500 | 0.6602 | 0.5736 | 0.6462 | 0.0837 | 0.7780 |
| 4 | tfidf_linear_svm | 0.4500 | 0.6359 | 0.5506 | 0.6247 | 0.0849 | 0.7805 |
| 4 | quantum_inspired_projection | 0.8500 | 0.6038 | 0.5377 | 0.6038 | 0.1005 | 0.7593 |
| 4 | quantum_contrastive_projection | 0.6500 | 0.5682 | 0.4994 | 0.5613 | 0.0909 | 0.7572 |
| 4 | hybrid_quantum_svm_fusion | 0.5000 | 0.6404 | 0.5476 | 0.6203 | 0.0766 | 0.7851 |
| 4 | sentence_bert_logistic_regression | 0.6000 | 0.6051 | 0.5345 | 0.6013 | 0.0921 | 0.8035 |
| 5 | label_frequency_baseline | 0.0500 | 0.2294 | 0.2060 | 0.2504 | 0.7955 | 0.3967 |
| 5 | tfidf_logistic_regression | 0.4500 | 0.6425 | 0.5961 | 0.6331 | 0.0945 | 0.7785 |
| 5 | tfidf_linear_svm | 0.4500 | 0.6571 | 0.6049 | 0.6426 | 0.0861 | 0.7844 |
| 5 | quantum_inspired_projection | 0.7000 | 0.5726 | 0.5385 | 0.5843 | 0.1232 | 0.7522 |
| 5 | quantum_contrastive_projection | 0.6500 | 0.5684 | 0.5370 | 0.5659 | 0.0981 | 0.7438 |
| 5 | hybrid_quantum_svm_fusion | 0.5000 | 0.6230 | 0.5934 | 0.6157 | 0.0825 | 0.7804 |
| 5 | sentence_bert_logistic_regression | 0.4500 | 0.6176 | 0.6115 | 0.6305 | 0.1244 | 0.8529 |

## Paired Statistical Tests

| comparison | folds | wilcoxon_statistic | p_value | mean_macro_f1_difference |
| --- | --- | --- | --- | --- |
| hybrid_quantum_svm_fusion_vs_tfidf_linear_svm | 5 | 5.0000 | 0.6250 | -0.0049 |
| hybrid_quantum_svm_fusion_vs_tfidf_logistic_regression | 5 | 7.0000 | 1.0000 | 0.0022 |
| hybrid_quantum_svm_fusion_vs_sentence_bert_logistic_regression | 5 | 1.0000 | 0.1250 | -0.0122 |

## Reading the Results

- Higher `micro_f1`, `macro_f1`, `weighted_f1`, and `label_ranking_average_precision` are better.
- Lower `hamming_loss` is better.
- `macro_f1` is the most important score here because the NFR labels are imbalanced.
