# NICE Fine-tuned Transformer Baseline

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Transformer: `distilbert-base-uncased`
- Labels: `11`
- Folds: `5`
- Epochs per fold: `2`
- Batch size: `16`
- Max sequence length: `128`
- Learning rate: `5e-05`
- Loss: BCEWithLogitsLoss; positive weights: `True`.
- Calibration: `per_label` thresholds selected on validation data.

## Mean Results

| model | micro_f1_mean | micro_f1_std | macro_f1_mean | macro_f1_std | weighted_f1_mean | weighted_f1_std | hamming_loss_mean | hamming_loss_std | label_ranking_average_precision_mean | label_ranking_average_precision_std | threshold_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| finetuned_distilbert_base_uncased | 0.5420 | 0.0569 | 0.5333 | 0.0591 | 0.5727 | 0.0467 | 0.1402 | 0.0361 | 0.7105 | 0.0516 | 0.5582 |

## Per-fold Results

| fold | model | threshold | micro_f1 | macro_f1 | weighted_f1 | hamming_loss | label_ranking_average_precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | finetuned_distilbert_base_uncased | 0.5545 | 0.4825 | 0.4839 | 0.5204 | 0.1924 | 0.6888 |
| 2 | finetuned_distilbert_base_uncased | 0.5682 | 0.6161 | 0.5813 | 0.6312 | 0.1029 | 0.6888 |
| 3 | finetuned_distilbert_base_uncased | 0.5545 | 0.5259 | 0.4775 | 0.5461 | 0.1423 | 0.7915 |
| 4 | finetuned_distilbert_base_uncased | 0.5318 | 0.5000 | 0.5145 | 0.5542 | 0.1531 | 0.6569 |
| 5 | finetuned_distilbert_base_uncased | 0.5818 | 0.5856 | 0.6091 | 0.6115 | 0.1100 | 0.7266 |

## Interpretation

- This is a fine-tuned transformer baseline, not a frozen embedding baseline.
- Because NICE has only 381 usable requirements and rare label combinations, these fold-level estimates should be interpreted cautiously.
- The result is intended to bound performance against a task-adapted neural baseline, not to tune for state-of-the-art performance.
