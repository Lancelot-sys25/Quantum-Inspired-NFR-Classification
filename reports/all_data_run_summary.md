# All Runnable Data Experiments Summary

This summary records the datasets found in the `data` folder and the experiments that were successfully run.

## Main Multi-label Dataset

### NICE

Input:

```text
data/raw/PROMISE-relabeled-NICE.csv
```

Task:

```text
Multi-label NFR classification
```

Rows used:

```text
381 requirements, 11 NFR labels, 125 multi-label requirements
```

Reports:

```text
reports/nice_multilabel_report.md
reports/nice_cv_report.md
```

Single split results:

| model | threshold | micro_f1 | macro_f1 | hamming_loss | LRAP |
| --- | ---: | ---: | ---: | ---: | ---: |
| label_frequency_baseline | 0.05 | 0.2221 | 0.2166 | 0.8751 | 0.4183 |
| tfidf_logistic_regression | 0.45 | 0.6299 | 0.5266 | 0.0901 | 0.7861 |
| tfidf_linear_svm | 0.45 | 0.6212 | 0.5205 | 0.0877 | 0.7843 |
| quantum_inspired_projection | 0.85 | 0.6076 | 0.5618 | 0.0980 | 0.7694 |
| quantum_contrastive_projection | 0.45 | 0.4346 | 0.4460 | 0.2119 | 0.7099 |
| hybrid_quantum_svm_fusion | 0.45 | 0.6254 | 0.5276 | 0.0862 | 0.7775 |

5-fold cross-validation mean results:

| model | micro_f1_mean | macro_f1_mean | hamming_loss_mean | LRAP_mean |
| --- | ---: | ---: | ---: | ---: |
| hybrid_quantum_svm_fusion | 0.6881 | 0.6112 | 0.0749 | 0.8045 |
| tfidf_linear_svm | 0.6821 | 0.6049 | 0.0764 | 0.8056 |
| tfidf_logistic_regression | 0.6787 | 0.5977 | 0.0759 | 0.7990 |
| quantum_inspired_projection | 0.5931 | 0.5490 | 0.1096 | 0.7830 |
| quantum_contrastive_projection | 0.4924 | 0.5144 | 0.1751 | 0.7185 |
| label_frequency_baseline | 0.2328 | 0.2083 | 0.7927 | 0.4059 |

Interpretation:

```text
NICE is the most relevant dataset for the research topic because it is multi-label.
The positive projection model is strongest among pure quantum-inspired variants on the single split, while the hybrid quantum + SVM fusion model is strongest among the no-SBERT models in standard 5-fold cross-validation.
The rectified contrastive projection avoids rewarding negative evidence, but the pure contrastive variant needs further refinement.
```

### NICE 5-fold with per-label threshold calibration

Report:

```text
reports/nice_per_label_threshold_report.md
```

| model | micro_f1_mean | macro_f1_mean | hamming_loss_mean | LRAP_mean |
| --- | ---: | ---: | ---: | ---: |
| hybrid_quantum_svm_fusion | 0.6230 | 0.5850 | 0.1031 | 0.8045 |
| tfidf_linear_svm | 0.6085 | 0.5640 | 0.1057 | 0.8056 |
| tfidf_logistic_regression | 0.6219 | 0.5629 | 0.0967 | 0.7990 |

Interpretation:

```text
When every model uses per-label threshold calibration, the hybrid quantum model achieves the best Macro-F1 among the no-SBERT models.
This setting is relevant because multi-label NFR classes are imbalanced and each label can require a different decision threshold.
```

## Single-label NFR Subtype Datasets

These datasets are useful as additional evidence, but they are not the main multi-label experiment.

### PROMISE_exp

Input:

```text
data/raw/PROMISE_exp.arff
```

Rows parsed:

```text
969 total, 525 NFR rows used
```

Report:

```text
reports/promise_exp_report.md
```

| model | accuracy | macro_f1 | micro_f1 | weighted_f1 |
| --- | ---: | ---: | ---: | ---: |
| majority_baseline | 0.2405 | 0.0353 | 0.2405 | 0.0933 |
| tfidf_logistic_regression | 0.6899 | 0.6344 | 0.6899 | 0.6783 |
| quantum_inspired_projection | 0.7025 | 0.6748 | 0.7025 | 0.6967 |

### Promise+

Input:

```text
data/raw/Promise+.arff
```

Rows parsed:

```text
2708 total, 894 NFR rows used
```

Report:

```text
reports/promise_plus_report.md
```

| model | accuracy | macro_f1 | micro_f1 | weighted_f1 |
| --- | ---: | ---: | ---: | ---: |
| majority_baseline | 0.2193 | 0.0327 | 0.2193 | 0.0789 |
| tfidf_logistic_regression | 0.7100 | 0.6744 | 0.7100 | 0.7067 |
| quantum_inspired_projection | 0.6914 | 0.6821 | 0.6914 | 0.6927 |

### tera-PROMISE NFR

Input:

```text
data/raw/data/se-requirements-classification/0-datasets/tera-PROMISE NFR/nfr.arff
```

Rows parsed:

```text
625 total, NFR-only subset used
```

Report:

```text
reports/tera_promise_nfr_report.md
```

| model | accuracy | macro_f1 | micro_f1 | weighted_f1 |
| --- | ---: | ---: | ---: | ---: |
| majority_baseline | 0.1802 | 0.0305 | 0.1802 | 0.0550 |
| tfidf_logistic_regression | 0.7297 | 0.6998 | 0.7297 | 0.7277 |
| quantum_inspired_projection | 0.7207 | 0.6886 | 0.7207 | 0.7160 |

## Metadata / Not Directly Runnable as NFR Classification

### Software Type List

Input:

```text
data/raw/Lista dos tipos de software.xlsx
```

Content:

```text
43 rows, 2 columns: Project ID and Software Class
```

Interpretation:

```text
This is metadata mapping projects to software classes. It does not contain requirement text and NFR labels, so it is not directly runnable as a classification dataset.
```

## Skipped Files

Some files inside:

```text
data/raw/data/se-requirements-classification
```

are original repository scripts, vectorized feature matrices, image resources, trace files, or model result text files. They are useful for reference but were not run as primary datasets for this project.
