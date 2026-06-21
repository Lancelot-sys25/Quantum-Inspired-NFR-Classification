# NICE Quantum-inspired Ablation Study

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Labels: `11`
- Folds: `5`
- Each model uses the same train/validation/test fold partitions.
- A global threshold is selected on the validation split by maximizing Macro-F1.

## Ablation Meaning

- `svm_only_sublinear_tfidf`: discriminative SVM component without quantum projection.
- `positive_projection_with_interference`: original centroid projection with label co-occurrence adjustment.
- `contrastive_projection_no_interference`: positive-minus-negative label directions without co-occurrence adjustment.
- `contrastive_projection_with_interference`: contrastive projection with co-occurrence adjustment.
- `hybrid_alpha_*`: score-level fusion between contrastive projection and SVM with different quantum weights.

## Mean Results

| model | micro_f1_mean | micro_f1_std | macro_f1_mean | macro_f1_std | weighted_f1_mean | weighted_f1_std | hamming_loss_mean | hamming_loss_std | label_ranking_average_precision_mean | label_ranking_average_precision_std | threshold_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hybrid_alpha_0_15 | 0.6739 | 0.0432 | 0.6000 | 0.0318 | 0.6582 | 0.0392 | 0.0742 | 0.0099 | 0.8075 | 0.0259 | 0.4900 |
| svm_only_sublinear_tfidf | 0.6713 | 0.0553 | 0.5945 | 0.0409 | 0.6554 | 0.0477 | 0.0843 | 0.0263 | 0.8081 | 0.0291 | 0.4400 |
| hybrid_alpha_0_50 | 0.6501 | 0.0544 | 0.5865 | 0.0443 | 0.6399 | 0.0544 | 0.0818 | 0.0119 | 0.7933 | 0.0374 | 0.5400 |
| hybrid_alpha_0_30 | 0.6442 | 0.0597 | 0.5761 | 0.0470 | 0.6307 | 0.0602 | 0.0759 | 0.0085 | 0.8029 | 0.0294 | 0.5300 |
| contrastive_projection_with_interference | 0.6145 | 0.0493 | 0.5602 | 0.0416 | 0.6093 | 0.0496 | 0.0873 | 0.0116 | 0.7775 | 0.0320 | 0.6400 |
| positive_projection_with_interference | 0.5931 | 0.0166 | 0.5490 | 0.0237 | 0.5936 | 0.0138 | 0.1096 | 0.0213 | 0.7830 | 0.0304 | 0.7800 |
| contrastive_projection_no_interference | 0.5995 | 0.0353 | 0.5445 | 0.0363 | 0.5899 | 0.0376 | 0.0878 | 0.0089 | 0.7783 | 0.0328 | 0.6500 |

## Per-fold Results

| fold | model | threshold | micro_f1 | macro_f1 | weighted_f1 | hamming_loss | label_ranking_average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | svm_only_sublinear_tfidf | 0.4500 | 0.7075 | 0.6131 | 0.6869 | 0.0732 | 0.8220 |
| 1 | positive_projection_with_interference | 0.9500 | 0.6082 | 0.5584 | 0.6071 | 0.0897 | 0.7956 |
| 1 | contrastive_projection_no_interference | 0.6000 | 0.6422 | 0.5876 | 0.6491 | 0.0921 | 0.7911 |
| 1 | contrastive_projection_with_interference | 0.6000 | 0.6368 | 0.5799 | 0.6437 | 0.0956 | 0.7911 |
| 1 | hybrid_alpha_0_15 | 0.4500 | 0.6979 | 0.6278 | 0.6942 | 0.0838 | 0.8122 |
| 1 | hybrid_alpha_0_30 | 0.5000 | 0.6759 | 0.6083 | 0.6740 | 0.0826 | 0.8105 |
| 1 | hybrid_alpha_0_50 | 0.5000 | 0.6888 | 0.6249 | 0.6903 | 0.0885 | 0.7970 |
| 2 | svm_only_sublinear_tfidf | 0.4500 | 0.7300 | 0.6417 | 0.7072 | 0.0646 | 0.8462 |
| 2 | positive_projection_with_interference | 0.5500 | 0.5776 | 0.5248 | 0.5745 | 0.1400 | 0.8280 |
| 2 | contrastive_projection_no_interference | 0.7000 | 0.6228 | 0.5452 | 0.5955 | 0.0754 | 0.8278 |
| 2 | contrastive_projection_with_interference | 0.6500 | 0.6848 | 0.6035 | 0.6754 | 0.0694 | 0.8256 |
| 2 | hybrid_alpha_0_15 | 0.5000 | 0.7302 | 0.6164 | 0.6982 | 0.0610 | 0.8445 |
| 2 | hybrid_alpha_0_30 | 0.5000 | 0.7310 | 0.6344 | 0.7116 | 0.0634 | 0.8446 |
| 2 | hybrid_alpha_0_50 | 0.5500 | 0.7188 | 0.6283 | 0.7022 | 0.0646 | 0.8460 |
| 3 | svm_only_sublinear_tfidf | 0.4500 | 0.6737 | 0.6131 | 0.6591 | 0.0742 | 0.8135 |
| 3 | positive_projection_with_interference | 0.8500 | 0.6030 | 0.5856 | 0.5983 | 0.0945 | 0.7798 |
| 3 | contrastive_projection_no_interference | 0.6500 | 0.6057 | 0.5697 | 0.5901 | 0.0825 | 0.7716 |
| 3 | contrastive_projection_with_interference | 0.6500 | 0.6145 | 0.5809 | 0.6001 | 0.0825 | 0.7700 |
| 3 | hybrid_alpha_0_15 | 0.5000 | 0.6782 | 0.6145 | 0.6626 | 0.0670 | 0.8154 |
| 3 | hybrid_alpha_0_30 | 0.5500 | 0.6258 | 0.5769 | 0.6106 | 0.0730 | 0.8098 |
| 3 | hybrid_alpha_0_50 | 0.5500 | 0.6480 | 0.5971 | 0.6300 | 0.0754 | 0.8085 |
| 4 | svm_only_sublinear_tfidf | 0.4500 | 0.6598 | 0.5618 | 0.6403 | 0.0789 | 0.7738 |
| 4 | positive_projection_with_interference | 0.8500 | 0.6038 | 0.5377 | 0.6038 | 0.1005 | 0.7593 |
| 4 | contrastive_projection_no_interference | 0.6500 | 0.5632 | 0.4957 | 0.5542 | 0.0909 | 0.7572 |
| 4 | contrastive_projection_with_interference | 0.6500 | 0.5682 | 0.4994 | 0.5613 | 0.0909 | 0.7572 |
| 4 | hybrid_alpha_0_15 | 0.5000 | 0.6404 | 0.5476 | 0.6203 | 0.0766 | 0.7851 |
| 4 | hybrid_alpha_0_30 | 0.5500 | 0.6087 | 0.5204 | 0.5907 | 0.0754 | 0.7793 |
| 4 | hybrid_alpha_0_50 | 0.5500 | 0.6044 | 0.5270 | 0.5913 | 0.0861 | 0.7593 |
| 5 | svm_only_sublinear_tfidf | 0.4000 | 0.5856 | 0.5426 | 0.5835 | 0.1304 | 0.7852 |
| 5 | positive_projection_with_interference | 0.7000 | 0.5726 | 0.5385 | 0.5843 | 0.1232 | 0.7522 |
| 5 | contrastive_projection_no_interference | 0.6500 | 0.5638 | 0.5243 | 0.5605 | 0.0981 | 0.7438 |
| 5 | contrastive_projection_with_interference | 0.6500 | 0.5684 | 0.5370 | 0.5659 | 0.0981 | 0.7438 |
| 5 | hybrid_alpha_0_15 | 0.5000 | 0.6230 | 0.5934 | 0.6157 | 0.0825 | 0.7804 |
| 5 | hybrid_alpha_0_30 | 0.5500 | 0.5799 | 0.5403 | 0.5667 | 0.0849 | 0.7703 |
| 5 | hybrid_alpha_0_50 | 0.5500 | 0.5907 | 0.5553 | 0.5857 | 0.0945 | 0.7556 |

## Interpretation

- This ablation is designed to verify whether each proposed component contributes useful signal.
- If `contrastive_projection_with_interference` improves over `positive_projection_with_interference`, contrastive label directions are beneficial.
- If hybrid variants improve over pure projection variants, discriminative calibration is beneficial.
- If increasing `alpha` hurts performance, the quantum component is useful as a calibrated auxiliary signal rather than as the dominant score.
