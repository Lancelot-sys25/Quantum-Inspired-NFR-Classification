# NICE Quantum-inspired Ablation Study

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Labels: `11`
- Folds: `5`
- Each model uses the same train/validation/test fold partitions.
- A global threshold is selected on the validation split by maximizing Macro-F1.

## Ablation Meaning

- `svm_only_sublinear_tfidf`: discriminative SVM component without quantum projection.
- `positive_projection_no_interference`: original centroid projection without label co-occurrence adjustment.
- `positive_projection_with_interference`: original centroid projection with label co-occurrence adjustment.
- `contrastive_projection_no_interference`: positive-minus-negative label directions without co-occurrence adjustment.
- `contrastive_projection_with_interference`: contrastive projection with co-occurrence adjustment.
- `hybrid_alpha_*`: score-level fusion between contrastive projection and SVM with different quantum weights.

## Mean Results

| model | micro_f1_mean | micro_f1_std | macro_f1_mean | macro_f1_std | weighted_f1_mean | weighted_f1_std | hamming_loss_mean | hamming_loss_std | label_ranking_average_precision_mean | label_ranking_average_precision_std | threshold_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hybrid_alpha_0_15 | 0.6860 | 0.0312 | 0.6091 | 0.0293 | 0.6679 | 0.0278 | 0.0756 | 0.0072 | 0.8085 | 0.0280 | 0.4500 |
| hybrid_alpha_0_30 | 0.6839 | 0.0331 | 0.6084 | 0.0294 | 0.6658 | 0.0298 | 0.0768 | 0.0074 | 0.8040 | 0.0266 | 0.4500 |
| hybrid_alpha_0_50 | 0.6814 | 0.0404 | 0.6054 | 0.0299 | 0.6623 | 0.0349 | 0.0795 | 0.0113 | 0.8012 | 0.0232 | 0.4500 |
| svm_only_sublinear_tfidf | 0.6713 | 0.0553 | 0.5945 | 0.0409 | 0.6554 | 0.0477 | 0.0843 | 0.0263 | 0.8081 | 0.0291 | 0.4400 |
| positive_projection_no_interference | 0.5948 | 0.0238 | 0.5526 | 0.0285 | 0.5952 | 0.0189 | 0.1108 | 0.0233 | 0.7839 | 0.0309 | 0.7400 |
| positive_projection_with_interference | 0.5931 | 0.0166 | 0.5490 | 0.0237 | 0.5936 | 0.0138 | 0.1096 | 0.0213 | 0.7830 | 0.0304 | 0.7800 |
| contrastive_projection_no_interference | 0.5447 | 0.0420 | 0.5397 | 0.0398 | 0.5777 | 0.0415 | 0.1339 | 0.0100 | 0.7183 | 0.0523 | 0.4500 |
| contrastive_projection_with_interference | 0.4300 | 0.0783 | 0.4118 | 0.0275 | 0.4240 | 0.0424 | 0.2074 | 0.1634 | 0.6968 | 0.0503 | 0.4800 |

## Per-fold Results

| fold | model | threshold | micro_f1 | macro_f1 | weighted_f1 | hamming_loss | label_ranking_average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | svm_only_sublinear_tfidf | 0.4500 | 0.7075 | 0.6131 | 0.6869 | 0.0732 | 0.8220 |
| 1 | positive_projection_no_interference | 0.9000 | 0.6231 | 0.5872 | 0.6196 | 0.0885 | 0.7992 |
| 1 | positive_projection_with_interference | 0.9500 | 0.6082 | 0.5584 | 0.6071 | 0.0897 | 0.7956 |
| 1 | contrastive_projection_no_interference | 0.4500 | 0.5909 | 0.5954 | 0.6290 | 0.1275 | 0.7800 |
| 1 | contrastive_projection_with_interference | 0.4500 | 0.3614 | 0.4266 | 0.4125 | 0.3672 | 0.7468 |
| 1 | hybrid_alpha_0_15 | 0.4500 | 0.7103 | 0.6146 | 0.6890 | 0.0732 | 0.8223 |
| 1 | hybrid_alpha_0_30 | 0.4500 | 0.7136 | 0.6201 | 0.6929 | 0.0720 | 0.8093 |
| 1 | hybrid_alpha_0_50 | 0.4500 | 0.7281 | 0.6334 | 0.7030 | 0.0697 | 0.8110 |
| 2 | svm_only_sublinear_tfidf | 0.4500 | 0.7300 | 0.6417 | 0.7072 | 0.0646 | 0.8462 |
| 2 | positive_projection_no_interference | 0.5500 | 0.5830 | 0.5253 | 0.5817 | 0.1352 | 0.8267 |
| 2 | positive_projection_with_interference | 0.5500 | 0.5776 | 0.5248 | 0.5745 | 0.1400 | 0.8280 |
| 2 | contrastive_projection_no_interference | 0.4500 | 0.5854 | 0.5632 | 0.6118 | 0.1220 | 0.7703 |
| 2 | contrastive_projection_with_interference | 0.4500 | 0.3320 | 0.3956 | 0.3571 | 0.4043 | 0.7510 |
| 2 | hybrid_alpha_0_15 | 0.4500 | 0.7255 | 0.6392 | 0.7027 | 0.0670 | 0.8453 |
| 2 | hybrid_alpha_0_30 | 0.4500 | 0.7255 | 0.6392 | 0.7027 | 0.0670 | 0.8426 |
| 2 | hybrid_alpha_0_50 | 0.4500 | 0.7184 | 0.6335 | 0.6968 | 0.0694 | 0.8340 |
| 3 | svm_only_sublinear_tfidf | 0.4500 | 0.6737 | 0.6131 | 0.6591 | 0.0742 | 0.8135 |
| 3 | positive_projection_no_interference | 0.7500 | 0.5972 | 0.5754 | 0.5934 | 0.1017 | 0.7850 |
| 3 | positive_projection_with_interference | 0.8500 | 0.6030 | 0.5856 | 0.5983 | 0.0945 | 0.7798 |
| 3 | contrastive_projection_no_interference | 0.4500 | 0.4937 | 0.4953 | 0.5280 | 0.1447 | 0.6750 |
| 3 | contrastive_projection_with_interference | 0.5000 | 0.4928 | 0.4173 | 0.4442 | 0.0837 | 0.6461 |
| 3 | hybrid_alpha_0_15 | 0.4500 | 0.6806 | 0.6247 | 0.6654 | 0.0730 | 0.8131 |
| 3 | hybrid_alpha_0_30 | 0.4500 | 0.6667 | 0.6160 | 0.6508 | 0.0789 | 0.8103 |
| 3 | hybrid_alpha_0_50 | 0.4500 | 0.6601 | 0.6039 | 0.6425 | 0.0825 | 0.8014 |
| 4 | svm_only_sublinear_tfidf | 0.4500 | 0.6598 | 0.5618 | 0.6403 | 0.0789 | 0.7738 |
| 4 | positive_projection_no_interference | 0.9000 | 0.6091 | 0.5505 | 0.6079 | 0.0921 | 0.7573 |
| 4 | positive_projection_with_interference | 0.8500 | 0.6038 | 0.5377 | 0.6038 | 0.1005 | 0.7593 |
| 4 | contrastive_projection_no_interference | 0.4500 | 0.5299 | 0.5154 | 0.5601 | 0.1316 | 0.6889 |
| 4 | contrastive_projection_with_interference | 0.5000 | 0.4604 | 0.3742 | 0.4377 | 0.0897 | 0.6888 |
| 4 | hybrid_alpha_0_15 | 0.4500 | 0.6598 | 0.5618 | 0.6403 | 0.0789 | 0.7760 |
| 4 | hybrid_alpha_0_30 | 0.4500 | 0.6564 | 0.5603 | 0.6374 | 0.0801 | 0.7759 |
| 4 | hybrid_alpha_0_50 | 0.4500 | 0.6667 | 0.5619 | 0.6421 | 0.0789 | 0.7745 |
| 5 | svm_only_sublinear_tfidf | 0.4000 | 0.5856 | 0.5426 | 0.5835 | 0.1304 | 0.7852 |
| 5 | positive_projection_no_interference | 0.6000 | 0.5615 | 0.5249 | 0.5732 | 0.1364 | 0.7514 |
| 5 | positive_projection_with_interference | 0.7000 | 0.5726 | 0.5385 | 0.5843 | 0.1232 | 0.7522 |
| 5 | contrastive_projection_no_interference | 0.4500 | 0.5238 | 0.5291 | 0.5596 | 0.1435 | 0.6774 |
| 5 | contrastive_projection_with_interference | 0.5000 | 0.5032 | 0.4451 | 0.4685 | 0.0921 | 0.6514 |
| 5 | hybrid_alpha_0_15 | 0.4500 | 0.6538 | 0.6051 | 0.6420 | 0.0861 | 0.7857 |
| 5 | hybrid_alpha_0_30 | 0.4500 | 0.6571 | 0.6066 | 0.6453 | 0.0861 | 0.7818 |
| 5 | hybrid_alpha_0_50 | 0.4500 | 0.6335 | 0.5945 | 0.6273 | 0.0969 | 0.7850 |

## Interpretation

- This ablation is designed to verify whether each proposed component contributes useful signal.
- If `contrastive_projection_with_interference` improves over `positive_projection_with_interference`, contrastive label directions are beneficial.
- If hybrid variants improve over pure projection variants, discriminative calibration is beneficial.
- If increasing `alpha` hurts performance, the quantum component is useful as a calibrated auxiliary signal rather than as the dominant score.
