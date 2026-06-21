# Explainable Quantum-Inspired Multi-label Classification of Non-Functional Requirements

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5%2B-orange.svg)](https://scikit-learn.org/)
[![Research](https://img.shields.io/badge/Project-Research-green.svg)](#research-context)
[![Status](https://img.shields.io/badge/Status-Prototype-yellow.svg)](#limitations-and-threats-to-validity)

This repository contains the source code, experiment scripts, reports, and paper materials for a research project on **Explainable Quantum-Inspired Multi-label Classification of Non-Functional Requirements (NFRs)**.

Non-functional requirements often overlap across quality attributes such as security, performance, usability, availability, maintainability, scalability, and portability. A single requirement may express more than one quality concern, making NFR classification a natural **multi-label text classification** problem. This project investigates whether a quantum-inspired semantic projection model can provide competitive classification performance while preserving interpretable token-level explanations.

> This is a research prototype. The current evidence supports a careful claim: quantum-inspired semantic projection provides an interpretable signal, and a calibrated hybrid quantum-SVM model can be competitive with strong TF-IDF baselines on multi-label NFR classification.

## Table of Contents

- [Research Context](#research-context)
- [Research Questions](#research-questions)
- [Main Contributions](#main-contributions)
- [Method Overview](#method-overview)
- [Repository Structure](#repository-structure)
- [Datasets](#datasets)
- [Installation](#installation)
- [Reproducing Experiments](#reproducing-experiments)
- [Experimental Results](#experimental-results)
- [Explainability](#explainability)
- [Paper Materials](#paper-materials)
- [Limitations and Threats to Validity](#limitations-and-threats-to-validity)
- [Roadmap for International Publication](#roadmap-for-international-publication)
- [Citation](#citation)
- [References](#references)

## Research Context

Requirements Engineering (RE) is a core software engineering activity because requirement quality affects architecture, implementation, testing, and maintenance. Non-functional requirements are particularly challenging because they are often:

- ambiguous and context-dependent;
- expressed implicitly in natural language;
- unevenly distributed across quality categories;
- overlapping across multiple labels.

For example, the requirement:

> "The disputes system must be accessible by both internal and external users."

may relate to availability, security, and operability depending on the intended system context. This makes strict single-label classification insufficient for many realistic RE scenarios.

This project studies an explainable quantum-inspired formulation in which:

- a requirement is represented as a normalized semantic state;
- an NFR label is represented as a projection direction;
- label scores are computed through projection amplitudes;
- token-level semantic amplitude contributions are used as explanations.

The approach is **quantum-inspired**, not quantum-hardware-based. It runs on classical computers and borrows mathematical intuitions from vector states, projection, probability amplitude, and label interference.

## Research Questions

This project is guided by three research questions:

**RQ1.** Can a quantum-inspired semantic projection model classify multi-label NFRs competitively compared with classical TF-IDF baselines?

**RQ2.** Can the model provide useful explainability through token-level semantic amplitude contributions?

**RQ3.** Is the observed improvement stable under cross-validation rather than only under a single train/test split?

## Main Contributions

This repository provides:

1. A reproducible Python pipeline for NFR classification experiments.
2. A quantum-inspired projection model for multi-label NFR classification.
3. A contrastive quantum-inspired projection variant using positive-minus-negative semantic label directions.
4. A hybrid quantum-SVM fusion model that combines interpretable projection scores with discriminative Linear SVM scores.
5. Token-level explanation utilities based on semantic amplitude contribution.
6. Empirical comparison against TF-IDF Logistic Regression, TF-IDF Linear SVM, and a label-frequency baseline.
7. Experiment reports for both single-split and 5-fold cross-validation protocols.

## Method Overview

### 1. Requirement Representation

Each requirement text is converted into a TF-IDF vector:

```text
x_i in R^d
```

The vector is L2-normalized and interpreted as a semantic state:

```text
|r_i> = x_i / ||x_i||
```

### 2. Label Projection

For each NFR label, the model estimates a label basis vector from the centroid of positive training examples. The association between a requirement and a label is computed as a squared projection amplitude:

```text
p(c | r_i) = (<c | r_i>)^2
```

### 3. Contrastive Projection

The contrastive variant learns each label direction from the difference between positive and negative centroids:

```text
|c_delta> = (mu_c_positive - mu_c_negative) / ||mu_c_positive - mu_c_negative||
```

This improves discrimination because the label direction captures what separates examples containing the label from examples not containing it.

### 4. Label Interference

The model estimates a simple label co-occurrence matrix from the training labels. Co-occurring labels can amplify one another through an interference adjustment.

### 5. Hybrid Quantum-SVM Fusion

The hybrid model combines contrastive quantum-inspired scores with one-vs-rest Linear SVM scores:

```text
h_i = alpha * q_i + (1 - alpha) * v_i
```

where:

- `q_i` is the contrastive quantum-inspired score vector;
- `v_i` is the calibrated Linear SVM score vector;
- `alpha = 0.15` is the quantum fusion weight used in the final experiments.

## Repository Structure

```text
NCKH-SWR/
  data/
    raw/                         # External raw datasets are expected here
    processed/                   # Processed datasets generated by scripts
    cv/                          # Cross-validation splits and summaries
  docs/                          # Research proposal, experiment plan, paper outline
  paper/
    main.tex                     # IEEE-style paper source
    references.bib               # Bibliography
    README.md                    # Paper build notes
  reports/                       # Experiment outputs and metric summaries
  scripts/
    run_all_experiments.py
    run_nice_ablation_experiment.py
    run_nice_multilabel_experiment.py
    run_nice_cv_experiment.py
    run_nice_per_label_threshold_experiment.py
    run_promise_experiment.py
    run_quantum_inspired.py
    run_baseline.py
    prepare_dataset.py
    create_cv_dataset.py
  src/quantum_re_nfr/
    quantum_model.py             # Quantum-inspired and hybrid classifiers
    explainability.py            # Token-level contribution utilities
    metrics.py                   # Metric helpers
    data.py                      # Dataset loading helpers
    config.py                    # Project configuration
  tests/
    test_metrics.py
  pyproject.toml
  requirements.txt
  README.md
```

## Datasets

### NICE Multi-label NFR Dataset

The main experiment uses the NICE dataset:

- **Dataset:** NICE: Non-Functional Requirements Identification, Classification, and Explanation Dataset
- **Source:** Zenodo
- **DOI:** [10.5281/zenodo.14590935](https://doi.org/10.5281/zenodo.14590935)

After filtering rows with at least one NFR subclass label and removing the empty `Other` label, the experiment uses:

| Statistic | Value |
| --- | ---: |
| Requirements used | 381 |
| NFR labels | 11 |
| Multi-label requirements | 125 |
| Label cardinality | 1.3648 |

The labels are:

```text
availability
fault_tolerance
legal
look_and_feel
maintainability
operability
performance
portability
scalability
security
usability
```

Expected raw file location:

```text
data/raw/PROMISE-relabeled-NICE.csv
```

### PROMISE-expanded Dataset

The secondary experiment uses PROMISE-expanded as an auxiliary single-label NFR subtype classification task. It is not the main evidence for the multi-label research claim, but it provides a sanity check for the quantum-inspired projection prototype.

Expected raw file location:

```text
data/raw/PROMISE_exp.arff
```

## Installation

### Requirements

- Python 3.10 or later
- pip
- Recommended: virtual environment

### Setup

```bash
git clone https://github.com/Lancelot-sys25/NCKH-SWR.git
cd NCKH-SWR

python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .[dev]
```

Run tests:

```bash
python -m pytest tests
```

## Reproducing Experiments

### 1. NICE Single Train/Validation/Test Split

```bash
python scripts/run_nice_multilabel_experiment.py
```

Outputs:

```text
data/processed/nice_multilabel_nfr.csv
reports/nice_multilabel_report.md
reports/nice_multilabel_metrics.csv
reports/nice_multilabel_metadata.json
```

### 2. NICE 5-Fold Cross-validation

```bash
python scripts/run_nice_cv_experiment.py
```

Outputs:

```text
reports/nice_cv_report.md
reports/nice_cv_summary.csv
reports/nice_cv_fold_results.csv
reports/nice_cv_metadata.json
```

### 3. NICE 5-Fold Cross-validation with Per-label Thresholds

```bash
python scripts/run_nice_per_label_threshold_experiment.py
```

Outputs:

```text
reports/nice_per_label_threshold_report.md
reports/nice_per_label_threshold_summary.csv
reports/nice_per_label_threshold_fold_results.csv
reports/nice_per_label_threshold_metadata.json
```

### 4. NICE Ablation Study

```bash
python scripts/run_nice_ablation_experiment.py
```

Outputs:

```text
reports/nice_ablation_report.md
reports/nice_ablation_summary.csv
reports/nice_ablation_fold_results.csv
reports/nice_ablation_metadata.json
```

The ablation study tests whether the proposed components are aligned with the research claim:

- original positive-centroid projection;
- contrastive projection without label interference;
- contrastive projection with label interference;
- SVM-only discriminative baseline;
- hybrid quantum-SVM fusion with different quantum weights.

### 5. Explainability Deletion Test

```bash
python scripts/run_explainability_deletion_test.py
```

Outputs:

```text
reports/nice_explainability_deletion_report.md
reports/nice_explainability_deletion_summary.csv
reports/nice_explainability_deletion_detail.csv
reports/nice_explainability_deletion_metadata.json
```

### 6. PROMISE-expanded Auxiliary Experiment

```bash
python scripts/run_promise_experiment.py
```

Outputs:

```text
data/processed/promise_exp_nfr_11class.csv
reports/promise_exp_report.md
reports/promise_exp_metrics.csv
reports/promise_exp_metadata.json
```

### 7. Run the Main Reproducibility Pipeline

```bash
python scripts/run_all_experiments.py
```

For a faster smoke test without optional Sentence-BERT:

```bash
python scripts/run_all_experiments.py --folds 2 --no-sbert --skip-promise --random-trials 5
```

## Experimental Results

### NICE Single Split

| Model | Threshold | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| --- | ---: | ---: | ---: | ---: | ---: |
| Label-frequency baseline | 0.05 | 0.2221 | 0.2166 | 0.8751 | 0.4183 |
| TF-IDF Logistic Regression | 0.45 | 0.6299 | 0.5266 | 0.0901 | 0.7861 |
| TF-IDF Linear SVM | 0.45 | 0.6212 | 0.5205 | 0.0877 | 0.7843 |
| Quantum-inspired Projection | 0.85 | 0.6076 | 0.5618 | 0.0980 | 0.7694 |
| Contrastive Quantum Projection | 0.60 | 0.5848 | 0.5367 | 0.1123 | 0.7600 |
| Hybrid Quantum-SVM Fusion | 0.45 | 0.6347 | 0.6019 | 0.0964 | 0.7847 |

In this single split, the hybrid quantum-SVM fusion model obtains the highest Micro-F1, Macro-F1, and LRAP. The original quantum-inspired projection also improves over TF-IDF Logistic Regression and TF-IDF Linear SVM on Macro-F1. However, single-split results should be interpreted cautiously.

### NICE 5-Fold Cross-validation

| Model | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| --- | ---: | ---: | ---: | ---: |
| TF-IDF Linear SVM | 0.6821 | 0.6049 | 0.0764 | 0.8056 |
| Hybrid Quantum-SVM Fusion | 0.6739 | 0.6000 | 0.0742 | 0.8075 |
| TF-IDF Logistic Regression | 0.6787 | 0.5977 | 0.0759 | 0.7990 |
| Contrastive Quantum Projection | 0.6145 | 0.5602 | 0.0873 | 0.7775 |
| Quantum-inspired Projection | 0.5931 | 0.5490 | 0.1096 | 0.7830 |
| Label-frequency baseline | 0.2328 | 0.2083 | 0.7927 | 0.4059 |

Under standard 5-fold cross-validation with a global threshold, TF-IDF Linear SVM obtains the highest Macro-F1. The hybrid quantum-SVM model remains competitive, improves over the pure quantum-inspired variants, and obtains the best Hamming loss and LRAP.

### NICE 5-Fold Cross-validation with Per-label Threshold Calibration

| Model | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| --- | ---: | ---: | ---: | ---: |
| Hybrid Quantum-SVM Fusion | 0.6138 | 0.5775 | 0.1010 | 0.8075 |
| TF-IDF Linear SVM | 0.6085 | 0.5640 | 0.1057 | 0.8056 |
| TF-IDF Logistic Regression | 0.6219 | 0.5629 | 0.0967 | 0.7990 |

With per-label threshold calibration, the hybrid quantum-SVM model obtains the best Macro-F1 and LRAP. This setting is important because the NICE labels are imbalanced and rare labels may require different decision thresholds from frequent labels.

### NICE Ablation Study

| Variant | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| --- | ---: | ---: | ---: | ---: |
| Hybrid Quantum-SVM, alpha = 0.15 | 0.6739 | 0.6000 | 0.0742 | 0.8075 |
| SVM-only sublinear TF-IDF | 0.6713 | 0.5945 | 0.0843 | 0.8081 |
| Hybrid Quantum-SVM, alpha = 0.50 | 0.6501 | 0.5865 | 0.0818 | 0.7933 |
| Hybrid Quantum-SVM, alpha = 0.30 | 0.6442 | 0.5761 | 0.0759 | 0.8029 |
| Contrastive projection with interference | 0.6145 | 0.5602 | 0.0873 | 0.7775 |
| Positive projection with interference | 0.5931 | 0.5490 | 0.1096 | 0.7830 |
| Contrastive projection without interference | 0.5995 | 0.5445 | 0.0878 | 0.7783 |

The ablation supports the current research claim: contrastive projection is more useful than the original positive-centroid projection, and the quantum-inspired signal is most effective as a light-weight calibrated component in the hybrid model.

### PROMISE-expanded Auxiliary Result

| Model | Accuracy | Macro-F1 | Micro-F1 | Weighted-F1 |
| --- | ---: | ---: | ---: | ---: |
| Majority baseline | 0.2405 | 0.0353 | 0.2405 | 0.0933 |
| TF-IDF Logistic Regression | 0.6899 | 0.6344 | 0.6899 | 0.6783 |
| Quantum-inspired Projection | 0.7025 | 0.6748 | 0.7025 | 0.6967 |

This auxiliary result suggests that the projection model can be competitive in a single-label NFR subtype setting. It should not be treated as the main evidence for the multi-label research claim.

## Explainability

The project includes token-level explanation utilities based on semantic amplitude contribution. For a predicted label, the explanation function reports the tokens or n-grams with the largest contribution to the corresponding label direction.

Example output format:

| Token/Phrase | Semantic Amplitude Contribution |
| --- | ---: |
| accessible by | 0.0183 |
| accessible | 0.0183 |
| external | 0.0182 |
| internal | 0.0114 |

This explanation mechanism is lightweight and directly tied to the projection model. Future work should evaluate explanation quality through human annotation, rationale overlap, or deletion-based faithfulness tests.

## Paper Materials

The paper source is available in:

```text
paper/main.tex
paper/references.bib
```

The current paper draft uses IEEE-style formatting and reports:

- research motivation;
- related work;
- quantum-inspired method;
- experimental setup;
- single-split results;
- 5-fold cross-validation;
- per-label threshold calibration;
- limitations and threats to validity;
- recommendations for international submission.

## Limitations and Threats to Validity

The current project has several limitations:

1. **Dataset size:** NICE contains only a few hundred NFR-labeled requirements after filtering.
2. **Label imbalance:** Some labels, such as fault tolerance, have very limited support.
3. **Rare label combinations:** Some multi-label combinations are too rare for stable stratified cross-validation.
4. **Baseline scope:** Current implemented baselines include TF-IDF Logistic Regression and Linear SVM, but not yet BERT, RoBERTa, or small language model baselines.
5. **Model simplicity:** Current quantum-inspired models use TF-IDF semantic states rather than contextual embeddings.
6. **Threshold sensitivity:** Multi-label classification performance depends strongly on threshold selection.
7. **Explainability evaluation:** Token-level explanations are generated, but they have not yet been evaluated through human agreement or faithfulness metrics.

## Roadmap for International Publication

To strengthen the project for submission to an international software engineering, requirements engineering, or applied AI venue, the following extensions are recommended:

- Add stronger neural baselines: BERT, RoBERTa, DistilBERT, Sentence-BERT embeddings, and small language models.
- Add classical multi-label baselines: ML-kNN, classifier chains, binary relevance with calibrated classifiers.
- Perform ablation studies:
  - positive-centroid projection only;
  - contrastive projection only;
  - projection without interference;
  - SVM only;
  - hybrid fusion with different `alpha` values;
  - global threshold versus per-label threshold.
- Add statistical significance tests over fold-level scores:
  - Wilcoxon signed-rank test;
  - paired bootstrap;
  - approximate randomization.
- Evaluate explanation quality:
  - human relevance judgments;
  - rationale overlap;
  - deletion tests;
  - comparison with TF-IDF/SVM feature weights.
- Evaluate cross-dataset generalization if compatible label mappings can be constructed.

## Research Readiness Checklist

- [x] TF-IDF Logistic Regression and Linear SVM baselines
- [x] Sentence-BERT embedding baseline
- [x] Quantum-inspired positive projection
- [x] Contrastive quantum-inspired projection
- [x] Hybrid quantum-SVM fusion
- [x] Cross-validation and per-label threshold calibration
- [x] Wilcoxon signed-rank tests over fold-level Macro-F1
- [x] Deletion-based explanation faithfulness test
- [x] Ablation study for projection, interference, and fusion weight
- [x] Reproducibility runner for the main experiment pipeline
- [ ] Fine-tuned BERT/RoBERTa/NoRBERT baselines
- [ ] Human evaluation of explanation usefulness
- [ ] Cross-dataset validation

## Development Notes

### Run the Test Suite

```bash
python -m pytest tests
```

### Code Style

The codebase is intentionally lightweight and based on:

- `numpy`
- `pandas`
- `scikit-learn`
- `scipy`

The main model implementation is located in:

```text
src/quantum_re_nfr/quantum_model.py
```

## Citation

If you use this repository, please cite the project as:

```bibtex
@misc{nguyen2026quantum_nfr,
  author       = {Nguyen Hoang Phuc and Le Doan Gia Hung},
  title        = {Explainable Quantum-Inspired Multi-label Classification of Non-Functional Requirements},
  year         = {2026},
  howpublished = {\url{https://github.com/Lancelot-sys25/NCKH-SWR}},
  note         = {Research prototype and reproducibility package}
}
```

## References

- Cleland-Huang, J., Settimi, R., Zou, X., and Solc, P. (2007). Automated classification of non-functional requirements. *Requirements Engineering*, 12(2), 103-120. [https://doi.org/10.1007/s00766-007-0045-1](https://doi.org/10.1007/s00766-007-0045-1)
- Rejithkumar, G., and Anish, P. R. (2025). NICE: Non-Functional Requirements Identification, Classification, and Explanation Dataset. Zenodo. [https://doi.org/10.5281/zenodo.14590935](https://doi.org/10.5281/zenodo.14590935)
- Rejithkumar, G., and Anish, P. R. (2025). NICE: Non-Functional Requirements Identification, Classification, and Explanation Using Small Language Models. Zenodo. [https://doi.org/10.5281/zenodo.14709254](https://doi.org/10.5281/zenodo.14709254)
- Mitrevski, A. (2019). Software Requirements Classification Using Machine Learning Algorithms on the PROMISE_exp Dataset. [https://github.com/AleksandarMitrevski/se-requirements-classification](https://github.com/AleksandarMitrevski/se-requirements-classification)

## License

No explicit license file is currently included. Before public reuse, distribution, or publication, add a suitable open-source license and verify the licenses of all external datasets.
