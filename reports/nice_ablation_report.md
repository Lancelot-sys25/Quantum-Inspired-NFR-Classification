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
| hybrid_alpha_0_30 | 0.6881 | 0.0325 | 0.6112 | 0.0301 | 0.6700 | 0.0289 | 0.0749 | 0.0076 | 0.8045 | 0.0268 | 0.4500 |
| hybrid_alpha_0_15 | 0.6870 | 0.0315 | 0.6097 | 0.0298 | 0.6690 | 0.0282 | 0.0747 | 0.0072 | 0.8085 | 0.0280 | 0.4500 |
| hybrid_alpha_0_50 | 0.6853 | 0.0394 | 0.6040 | 0.0280 | 0.6641 | 0.0341 | 0.0757 | 0.0090 | 0.8007 | 0.0250 | 0.4500 |
| svm_only_sublinear_tfidf | 0.6713 | 0.0553 | 0.5945 | 0.0409 | 0.6554 | 0.0477 | 0.0843 | 0.0263 | 0.8081 | 0.0291 | 0.4400 |
| positive_projection_with_interference | 0.5931 | 0.0166 | 0.5490 | 0.0237 | 0.5936 | 0.0138 | 0.1096 | 0.0213 | 0.7830 | 0.0304 | 0.7800 |
| contrastive_projection_no_interference | 0.5447 | 0.0420 | 0.5397 | 0.0398 | 0.5777 | 0.0415 | 0.1339 | 0.0100 | 0.7183 | 0.0523 | 0.4500 |
| contrastive_projection_with_interference | 0.4924 | 0.0537 | 0.5144 | 0.0387 | 0.5408 | 0.0468 | 0.1751 | 0.0352 | 0.7185 | 0.0538 | 0.4500 |

## Per-fold Results

| fold | model | threshold | micro_f1 | macro_f1 | weighted_f1 | hamming_loss | label_ranking_average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | svm_only_sublinear_tfidf | 0.4500 | 0.7075 | 0.6131 | 0.6869 | 0.0732 | 0.8220 |
| 1 | positive_projection_with_interference | 0.9500 | 0.6082 | 0.5584 | 0.6071 | 0.0897 | 0.7956 |
| 1 | contrastive_projection_no_interference | 0.4500 | 0.5909 | 0.5954 | 0.6290 | 0.1275 | 0.7800 |
| 1 | contrastive_projection_with_interference | 0.4500 | 0.4969 | 0.5623 | 0.5836 | 0.1913 | 0.7840 |
| 1 | hybrid_alpha_0_15 | 0.4500 | 0.7075 | 0.6131 | 0.6869 | 0.0732 | 0.8223 |
| 1 | hybrid_alpha_0_30 | 0.4500 | 0.7170 | 0.6229 | 0.6958 | 0.0708 | 0.8115 |
| 1 | hybrid_alpha_0_50 | 0.4500 | 0.7333 | 0.6374 | 0.7102 | 0.0661 | 0.8031 |
| 2 | svm_only_sublinear_tfidf | 0.4500 | 0.7300 | 0.6417 | 0.7072 | 0.0646 | 0.8462 |
| 2 | positive_projection_with_interference | 0.5500 | 0.5776 | 0.5248 | 0.5745 | 0.1400 | 0.8280 |
| 2 | contrastive_projection_no_interference | 0.4500 | 0.5854 | 0.5632 | 0.6118 | 0.1220 | 0.7703 |
| 2 | contrastive_projection_with_interference | 0.4500 | 0.5760 | 0.5499 | 0.5965 | 0.1268 | 0.7697 |
| 2 | hybrid_alpha_0_15 | 0.4500 | 0.7300 | 0.6417 | 0.7072 | 0.0646 | 0.8453 |
| 2 | hybrid_alpha_0_30 | 0.4500 | 0.7255 | 0.6392 | 0.7027 | 0.0670 | 0.8425 |
| 2 | hybrid_alpha_0_50 | 0.4500 | 0.7228 | 0.6119 | 0.6909 | 0.0670 | 0.8360 |
| 3 | svm_only_sublinear_tfidf | 0.4500 | 0.6737 | 0.6131 | 0.6591 | 0.0742 | 0.8135 |
| 3 | positive_projection_with_interference | 0.8500 | 0.6030 | 0.5856 | 0.5983 | 0.0945 | 0.7798 |
| 3 | contrastive_projection_no_interference | 0.4500 | 0.4937 | 0.4953 | 0.5280 | 0.1447 | 0.6750 |
| 3 | contrastive_projection_with_interference | 0.4500 | 0.4980 | 0.4931 | 0.5281 | 0.1495 | 0.6758 |
| 3 | hybrid_alpha_0_15 | 0.4500 | 0.6806 | 0.6247 | 0.6654 | 0.0730 | 0.8131 |
| 3 | hybrid_alpha_0_30 | 0.4500 | 0.6842 | 0.6265 | 0.6684 | 0.0718 | 0.8110 |
| 3 | hybrid_alpha_0_50 | 0.4500 | 0.6598 | 0.6061 | 0.6439 | 0.0789 | 0.8100 |
| 4 | svm_only_sublinear_tfidf | 0.4500 | 0.6598 | 0.5618 | 0.6403 | 0.0789 | 0.7738 |
| 4 | positive_projection_with_interference | 0.8500 | 0.6038 | 0.5377 | 0.6038 | 0.1005 | 0.7593 |
| 4 | contrastive_projection_no_interference | 0.4500 | 0.5299 | 0.5154 | 0.5601 | 0.1316 | 0.6889 |
| 4 | contrastive_projection_with_interference | 0.4500 | 0.4525 | 0.4780 | 0.4971 | 0.1998 | 0.6897 |
| 4 | hybrid_alpha_0_15 | 0.4500 | 0.6598 | 0.5618 | 0.6403 | 0.0789 | 0.7760 |
| 4 | hybrid_alpha_0_30 | 0.4500 | 0.6598 | 0.5618 | 0.6403 | 0.0789 | 0.7764 |
| 4 | hybrid_alpha_0_50 | 0.4500 | 0.6598 | 0.5597 | 0.6368 | 0.0789 | 0.7721 |
| 5 | svm_only_sublinear_tfidf | 0.4000 | 0.5856 | 0.5426 | 0.5835 | 0.1304 | 0.7852 |
| 5 | positive_projection_with_interference | 0.7000 | 0.5726 | 0.5385 | 0.5843 | 0.1232 | 0.7522 |
| 5 | contrastive_projection_no_interference | 0.4500 | 0.5238 | 0.5291 | 0.5596 | 0.1435 | 0.6774 |
| 5 | contrastive_projection_with_interference | 0.4500 | 0.4387 | 0.4885 | 0.4990 | 0.2081 | 0.6736 |
| 5 | hybrid_alpha_0_15 | 0.4500 | 0.6569 | 0.6074 | 0.6453 | 0.0837 | 0.7857 |
| 5 | hybrid_alpha_0_30 | 0.4500 | 0.6538 | 0.6057 | 0.6429 | 0.0861 | 0.7812 |
| 5 | hybrid_alpha_0_50 | 0.4500 | 0.6507 | 0.6048 | 0.6384 | 0.0873 | 0.7824 |

## Interpretation

- This ablation is designed to verify whether each proposed component contributes useful signal.
- If `contrastive_projection_with_interference` improves over `positive_projection_with_interference`, contrastive label directions are beneficial.
- If hybrid variants improve over pure projection variants, discriminative calibration is beneficial.
- If increasing `alpha` hurts performance, the quantum component is useful as a calibrated auxiliary signal rather than as the dominant score.
