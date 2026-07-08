# NICE Multi-label NFR Experiment Report

## Dataset

- Raw file: `data\raw\PROMISE-relabeled-NICE.csv`
- Processed file: `data\processed\nice_multilabel_nfr.csv`
- Requirements used: `381`
- NFR labels: `11`
- Multi-label requirements: `125`
- Label cardinality: `1.3648`
- Task: multi-label NFR subclass classification.

## Label Distribution

| label | count |
| --- | --- |
| usability | 85 |
| security | 75 |
| look_and_feel | 69 |
| performance | 63 |
| operability | 58 |
| availability | 38 |
| maintainability | 34 |
| legal | 31 |
| scalability | 29 |
| portability | 22 |
| fault_tolerance | 16 |

## Overall Results

| model | threshold | micro_f1 | macro_f1 | weighted_f1 | hamming_loss | label_ranking_average_precision |
| --- | --- | --- | --- | --- | --- | --- |
| label_frequency_baseline | 0.0500 | 0.2221 | 0.2166 | 0.2657 | 0.8751 | 0.4183 |
| tfidf_logistic_regression | 0.4500 | 0.6299 | 0.5266 | 0.6071 | 0.0901 | 0.7861 |
| tfidf_linear_svm | 0.4500 | 0.6212 | 0.5205 | 0.5992 | 0.0877 | 0.7843 |
| sentence_bert_logistic_regression | 0.5000 | 0.6667 | 0.6049 | 0.6673 | 0.0901 | 0.8286 |
| quantum_inspired_projection | 0.8500 | 0.6076 | 0.5618 | 0.6049 | 0.0980 | 0.7694 |
| quantum_contrastive_projection | 0.5000 | 0.4907 | 0.3885 | 0.4475 | 0.0870 | 0.6818 |
| hybrid_quantum_svm_fusion | 0.4500 | 0.6284 | 0.5286 | 0.6046 | 0.0870 | 0.7779 |

## Interpretation

- `micro_f1`: global multi-label F1 across all labels.
- `macro_f1`: average F1 across labels; important for rare NFR classes.
- `hamming_loss`: fraction of wrong label decisions; lower is better.
- `label_ranking_average_precision`: whether correct labels are ranked above incorrect labels; higher is better.
- `threshold`: decision cutoff selected on the validation split, then applied to the held-out test split.

## Quantum-inspired Explanation Example

- Text: PME Subsystem shall allow keeping submenus within menus and products within submenus in a managed and persisted order.
- True labels: `look_and_feel, usability`
- Predicted labels: `usability`
- Explanation label: `usability`

| token/phrase | semantic amplitude contribution |
|---|---:|
| and | 0.0394 |
| shall allow | 0.0278 |
| allow | 0.0248 |
| products | 0.0124 |
| within | 0.0061 |
| order | -0.0036 |
| shall | 0.0034 |
| in | -0.0020 |

## Per-label Classification Reports

### label_frequency_baseline

```text
                 precision    recall  f1-score   support

   availability       0.10      1.00      0.19        12
fault_tolerance       0.03      1.00      0.05         3
          legal       0.09      1.00      0.16        10
  look_and_feel       0.19      1.00      0.32        22
maintainability       0.09      1.00      0.16        10
    operability       0.15      1.00      0.26        17
    performance       0.16      1.00      0.27        18
    portability       0.06      1.00      0.11         7
    scalability       0.08      1.00      0.15         9
       security       0.20      1.00      0.33        23
      usability       0.23      1.00      0.38        27

      micro avg       0.12      1.00      0.22       158
      macro avg       0.12      1.00      0.22       158
   weighted avg       0.16      1.00      0.27       158
    samples avg       0.12      1.00      0.22       158

```

### tfidf_logistic_regression

```text
                 precision    recall  f1-score   support

   availability       0.88      0.58      0.70        12
fault_tolerance       0.00      0.00      0.00         3
          legal       0.83      0.50      0.62        10
  look_and_feel       0.68      0.77      0.72        22
maintainability       0.25      0.10      0.14        10
    operability       0.44      0.47      0.46        17
    performance       0.57      0.72      0.63        18
    portability       0.80      0.57      0.67         7
    scalability       1.00      0.22      0.36         9
       security       0.76      0.83      0.79        23
      usability       0.62      0.78      0.69        27

      micro avg       0.65      0.61      0.63       158
      macro avg       0.62      0.50      0.53       158
   weighted avg       0.65      0.61      0.61       158
    samples avg       0.60      0.67      0.61       158

```

### tfidf_linear_svm

```text
                 precision    recall  f1-score   support

   availability       0.73      0.67      0.70        12
fault_tolerance       0.00      0.00      0.00         3
          legal       0.71      0.50      0.59        10
  look_and_feel       0.71      0.68      0.70        22
maintainability       0.50      0.10      0.17        10
    operability       0.47      0.47      0.47        17
    performance       0.65      0.72      0.68        18
    portability       0.80      0.57      0.67         7
    scalability       0.67      0.22      0.33         9
       security       0.80      0.70      0.74        23
      usability       0.66      0.70      0.68        27

      micro avg       0.67      0.58      0.62       158
      macro avg       0.61      0.48      0.52       158
   weighted avg       0.66      0.58      0.60       158
    samples avg       0.60      0.64      0.60       158

```

### sentence_bert_logistic_regression

```text
                 precision    recall  f1-score   support

   availability       0.50      0.58      0.54        12
fault_tolerance       0.17      0.33      0.22         3
          legal       0.60      0.60      0.60        10
  look_and_feel       0.74      0.77      0.76        22
maintainability       0.38      0.30      0.33        10
    operability       0.54      0.76      0.63        17
    performance       0.61      0.78      0.68        18
    portability       0.62      0.71      0.67         7
    scalability       0.58      0.78      0.67         9
       security       0.78      0.91      0.84        23
      usability       0.69      0.74      0.71        27

      micro avg       0.62      0.72      0.67       158
      macro avg       0.56      0.66      0.60       158
   weighted avg       0.63      0.72      0.67       158
    samples avg       0.67      0.78      0.69       158

```

### quantum_inspired_projection

```text
                 precision    recall  f1-score   support

   availability       0.50      0.50      0.50        12
fault_tolerance       0.33      0.33      0.33         3
          legal       0.86      0.60      0.71        10
  look_and_feel       0.74      0.64      0.68        22
maintainability       0.33      0.20      0.25        10
    operability       0.50      0.47      0.48        17
    performance       0.68      0.72      0.70        18
    portability       0.50      0.57      0.53         7
    scalability       0.71      0.56      0.62         9
       security       0.77      0.74      0.76        23
      usability       0.51      0.74      0.61        27

      micro avg       0.61      0.61      0.61       158
      macro avg       0.59      0.55      0.56       158
   weighted avg       0.62      0.61      0.60       158
    samples avg       0.68      0.67      0.65       158

```

### quantum_contrastive_projection

```text
                 precision    recall  f1-score   support

   availability       1.00      0.42      0.59        12
fault_tolerance       0.00      0.00      0.00         3
          legal       1.00      0.50      0.67        10
  look_and_feel       0.50      0.05      0.08        22
maintainability       0.00      0.00      0.00        10
    operability       1.00      0.18      0.30        17
    performance       0.91      0.56      0.69        18
    portability       1.00      0.29      0.44         7
    scalability       1.00      0.11      0.20         9
       security       1.00      0.43      0.61        23
      usability       0.84      0.59      0.70        27

      micro avg       0.91      0.34      0.49       158
      macro avg       0.75      0.28      0.39       158
   weighted avg       0.81      0.34      0.45       158
    samples avg       0.42      0.39      0.40       158

```

### hybrid_quantum_svm_fusion

```text
                 precision    recall  f1-score   support

   availability       0.80      0.67      0.73        12
fault_tolerance       0.00      0.00      0.00         3
          legal       0.83      0.50      0.62        10
  look_and_feel       0.70      0.64      0.67        22
maintainability       0.50      0.10      0.17        10
    operability       0.47      0.47      0.47        17
    performance       0.65      0.72      0.68        18
    portability       0.80      0.57      0.67         7
    scalability       1.00      0.22      0.36         9
       security       0.77      0.74      0.76        23
      usability       0.62      0.78      0.69        27

      micro avg       0.67      0.59      0.63       158
      macro avg       0.65      0.49      0.53       158
   weighted avg       0.68      0.59      0.60       158
    samples avg       0.60      0.65      0.60       158

```
