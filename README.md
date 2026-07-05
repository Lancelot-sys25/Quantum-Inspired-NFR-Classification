# Quantum-Inspired NFR Classification

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5%2B-orange.svg)](https://scikit-learn.org/)
[![Research Artifact](https://img.shields.io/badge/Artifact-Reproducible-green.svg)](#reproducibility)
[![Status](https://img.shields.io/badge/Status-Research%20Prototype-yellow.svg)](#limitations)

This repository provides the reproducibility package for the study:

**Explainable Quantum-Inspired Multi-label Classification of Non-Functional Requirements**

The project investigates whether quantum-inspired semantic projection can support multi-label classification of non-functional requirements (NFRs) while preserving interpretable token-level evidence. Requirements are represented as normalized semantic states, NFR categories are represented as projection directions, label scores are estimated from projection amplitudes, and label co-occurrence is modeled through an interference matrix. The final experimental pipeline also evaluates a hybrid quantum-SVM model that combines the interpretability of projection-based scores with the discriminative strength of a calibrated Linear SVM.

The empirical claim supported by the current artifact is deliberately conservative: the quantum-inspired signal is most effective as an auxiliary interpretable component in a hybrid model, rather than as a stand-alone replacement for strong classical text classifiers.

## Contents

- [Research Objective](#research-objective)
- [Main Contributions](#main-contributions)
- [Methodological Overview](#methodological-overview)
- [Repository Layout](#repository-layout)
- [Datasets](#datasets)
- [Installation](#installation)
- [Reproducibility](#reproducibility)
- [Experimental Results](#experimental-results)
- [Explainability and Robustness](#explainability-and-robustness)
- [Paper and Review Artifact](#paper-and-review-artifact)
- [Limitations](#limitations)
- [Future Work](#future-work)
- [Citation](#citation)

## Research Objective

Requirements Engineering frequently distinguishes between functional requirements and non-functional requirements. NFRs describe quality attributes such as security, usability, performance, availability, maintainability, scalability, and portability. In practical requirement specifications, these concerns are often implicit, ambiguous, and overlapping. Consequently, a single requirement may belong to several NFR categories, making the task naturally multi-label.

This repository addresses the following research questions:

**RQ1.** Can a quantum-inspired semantic projection model classify multi-label NFRs competitively with classical TF-IDF baselines?

**RQ2.** Can projection-based semantic amplitudes provide useful token-level explanations for NFR predictions?

**RQ3.** Are the observed behaviors stable under cross-validation, threshold calibration, ablation, and robustness analysis?

## Main Contributions

This artifact includes:

1. A reproducible Python implementation for multi-label NFR classification.
2. A positive-centroid quantum-inspired projection classifier.
3. A contrastive projection variant based on positive-minus-negative label directions.
4. A rectified contrastive scoring rule that avoids rewarding negative projection evidence.
5. A label-interference mechanism derived from NFR co-occurrence.
6. A hybrid quantum-SVM fusion model with calibrated score-level fusion.
7. Token-level intrinsic explanations based on semantic amplitude contribution.
8. Deletion-based faithfulness evaluation for intrinsic and SVM-based explanations.
9. Cross-validation, per-label threshold calibration, ablation, bootstrap, and robustness reports.
10. LaTeX paper sources and a packaged review artifact.

## Methodological Overview

### Semantic State Representation

Each requirement text is encoded as a TF-IDF vector and L2-normalized:

```text
|r_i> = x_i / ||x_i||_2
```

The normalized vector is interpreted as a semantic state in a high-dimensional lexical space.

### Positive Label Projection

For each NFR label, a normalized positive-class centroid is estimated from training examples. The association between a requirement and a label is computed as a squared projection amplitude:

```text
s_c(r_i) = (<c | r_i>)^2
```

These scores are association scores used for thresholding; they are not mutually exclusive probabilities and are not constrained to sum to one.

### Contrastive Projection

The contrastive label direction is defined as:

```text
|c_delta> = (mu_c_positive - mu_c_negative) / ||mu_c_positive - mu_c_negative||_2
```

Because this direction is signed, a negative projection indicates evidence against the label. The implemented contrastive score therefore uses a rectified squared projection:

```text
s_delta_c(r_i) = max(0, <c_delta | r_i>)^2
```

This correction is important for semantic validity: evidence opposite to a label direction should not become high-confidence evidence for that label after squaring.

### Label Interference

The model estimates a label co-occurrence matrix from the training labels and mixes it with the identity matrix:

```text
M' = (1 - lambda) I + lambda M
```

The adjusted score vector is obtained by applying this label-coupling matrix to the projection scores. This component models the empirical tendency of some NFR categories to co-occur.

### Hybrid Quantum-SVM Fusion

The final hybrid model combines contrastive quantum-inspired scores with calibrated one-vs-rest Linear SVM scores:

```text
h_i = alpha q_i + (1 - alpha) v_i
```

where `q_i` is the quantum-inspired score vector, `v_i` is the SVM score vector, and the final experiments use:

```text
alpha = 0.30
```

## Repository Layout

```text
Quantum-Inspired-NFR-Classification/
  artifacts/
    nfr_eai_fisat_2026_review_artifact.zip
  data/
    raw/
    processed/
    cv/
  docs/
  paper/
    main.tex
    references.bib
    README.md
  reports/
    nice_multilabel_report.md
    nice_cv_report.md
    nice_per_label_threshold_report.md
    nice_ablation_report.md
    nice_explainability_deletion_report.md
    nice_robustness_report.md
    run_all_experiments_summary.md
  scripts/
    run_all_experiments.py
    run_nice_multilabel_experiment.py
    run_nice_cv_experiment.py
    run_nice_per_label_threshold_experiment.py
    run_nice_ablation_experiment.py
    run_nice_robustness_experiment.py
    run_explainability_deletion_test.py
    run_promise_experiment.py
    make_review_artifact.ps1
  src/quantum_re_nfr/
    quantum_model.py
    explainability.py
    metrics.py
    data.py
    config.py
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

Expected input path:

```text
data/raw/PROMISE-relabeled-NICE.csv
```

After filtering requirements with at least one NFR subclass label and removing the empty `Other` label, the main experiment uses:

| Statistic | Value |
| --- | ---: |
| Requirements | 381 |
| NFR labels | 11 |
| Multi-label requirements | 125 |
| Label cardinality | 1.3648 |

The evaluated labels are:

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

### Auxiliary PROMISE-family Datasets

The repository also includes auxiliary single-label NFR subtype experiments on PROMISE-expanded and related datasets. These results are useful as sanity checks, but the NICE dataset is the primary evidence for the multi-label research claim.

## Installation

Clone the repository:

```bash
git clone https://github.com/Lancelot-sys25/Quantum-Inspired-NFR-Classification.git
cd Quantum-Inspired-NFR-Classification
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .[dev]
```

Run the unit test suite:

```bash
python -m pytest tests
```

## Reproducibility

The complete reproducibility runner is:

```bash
python scripts/run_all_experiments.py
```

The latest recorded run completed the following stages successfully:

| Stage | Status |
| --- | --- |
| Unit tests | PASS |
| NICE single split | PASS |
| NICE 5-fold cross-validation | PASS |
| NICE per-label threshold calibration | PASS |
| NICE ablation study | PASS |
| NICE explainability deletion test | PASS |
| PROMISE auxiliary experiment | PASS |

A faster smoke test can be executed with:

```bash
python scripts/run_all_experiments.py --folds 2 --no-sbert --skip-promise --random-trials 5
```

### Individual Experiment Commands

Single train/validation/test split:

```bash
python scripts/run_nice_multilabel_experiment.py
```

Five-fold cross-validation:

```bash
python scripts/run_nice_cv_experiment.py
```

Per-label threshold calibration:

```bash
python scripts/run_nice_per_label_threshold_experiment.py
```

Ablation study:

```bash
python scripts/run_nice_ablation_experiment.py
```

Explainability deletion test:

```bash
python scripts/run_explainability_deletion_test.py
```

Robustness and bootstrap analysis:

```bash
python scripts/run_nice_robustness_experiment.py
```

Auxiliary PROMISE experiment:

```bash
python scripts/run_promise_experiment.py
```

## Experimental Results

### NICE Single Split

| Model | Threshold | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| --- | ---: | ---: | ---: | ---: | ---: |
| TF-IDF Logistic Regression | 0.45 | 0.6299 | 0.5266 | 0.0901 | 0.7861 |
| TF-IDF Linear SVM | 0.45 | 0.6212 | 0.5205 | 0.0877 | 0.7843 |
| Quantum-inspired Projection | 0.85 | 0.6076 | 0.5618 | 0.0980 | 0.7694 |
| Contrastive Quantum Projection | 0.45 | 0.4346 | 0.4460 | 0.2119 | 0.7099 |
| Hybrid Quantum-SVM Fusion | 0.45 | 0.6254 | 0.5276 | 0.0862 | 0.7775 |
| Label-frequency Baseline | 0.05 | 0.2221 | 0.2166 | 0.8751 | 0.4183 |

On this split, the positive projection variant achieves the strongest Macro-F1 among the quantum-inspired stand-alone variants, while the hybrid model obtains the lowest Hamming loss.

### NICE Five-fold Cross-validation

| Model | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| --- | ---: | ---: | ---: | ---: |
| Hybrid Quantum-SVM Fusion | 0.6881 +/- 0.0325 | 0.6112 +/- 0.0301 | 0.0749 +/- 0.0076 | 0.8045 +/- 0.0268 |
| TF-IDF Linear SVM | 0.6821 +/- 0.0405 | 0.6049 +/- 0.0336 | 0.0764 +/- 0.0094 | 0.8056 +/- 0.0262 |
| TF-IDF Logistic Regression | 0.6787 +/- 0.0463 | 0.5977 +/- 0.0229 | 0.0759 +/- 0.0140 | 0.7990 +/- 0.0240 |
| Quantum-inspired Projection | 0.5931 +/- 0.0166 | 0.5490 +/- 0.0237 | 0.1096 +/- 0.0213 | 0.7830 +/- 0.0304 |
| Contrastive Quantum Projection | 0.4924 +/- 0.0537 | 0.5144 +/- 0.0387 | 0.1751 +/- 0.0352 | 0.7185 +/- 0.0538 |
| Label-frequency Baseline | 0.2328 +/- 0.0034 | 0.2083 +/- 0.0032 | 0.7927 +/- 0.0019 | 0.4059 +/- 0.0110 |

The hybrid model achieves the highest Micro-F1 and Macro-F1 among the evaluated non-embedding models. The difference relative to TF-IDF Linear SVM is small, which motivates the statistical and robustness analyses below.

### Per-label Threshold Calibration

| Model | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| --- | ---: | ---: | ---: | ---: |
| Hybrid Quantum-SVM Fusion | 0.6230 +/- 0.0747 | 0.5850 +/- 0.0250 | 0.1031 +/- 0.0496 | 0.8045 +/- 0.0268 |
| TF-IDF Linear SVM | 0.6085 +/- 0.0588 | 0.5640 +/- 0.0309 | 0.1057 +/- 0.0378 | 0.8056 +/- 0.0262 |
| TF-IDF Logistic Regression | 0.6219 +/- 0.0588 | 0.5629 +/- 0.0532 | 0.0967 +/- 0.0195 | 0.7990 +/- 0.0240 |

Per-label thresholding is included because NFR labels are imbalanced and rare labels may require different decision thresholds from frequent labels.

### Ablation Study

| Variant | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| --- | ---: | ---: | ---: | ---: |
| Hybrid alpha = 0.30 | 0.6881 | 0.6112 | 0.0749 | 0.8045 |
| Hybrid alpha = 0.15 | 0.6870 | 0.6097 | 0.0747 | 0.8085 |
| Hybrid alpha = 0.50 | 0.6853 | 0.6040 | 0.0757 | 0.8007 |
| SVM-only sublinear TF-IDF | 0.6713 | 0.5945 | 0.0843 | 0.8081 |
| Positive projection with interference | 0.5931 | 0.5490 | 0.1096 | 0.7830 |
| Contrastive projection without interference | 0.5447 | 0.5397 | 0.1339 | 0.7183 |
| Contrastive projection with interference | 0.4924 | 0.5144 | 0.1751 | 0.7185 |

The ablation shows that hybrid fusion is the most useful component in the current implementation. The rectified contrastive projection is semantically preferable to squaring signed negative evidence, but its pure projection performance remains weaker than the positive-centroid projection on this dataset.

## Explainability and Robustness

### Deletion-based Explanation Faithfulness

The intrinsic projection explanation was evaluated by deleting the top-3 explanatory terms and comparing the score reduction with random deletion.

| Explainer | Top-k | Assignments | Mean Top Drop | Mean Random Drop | Drop Ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Contrastive projection intrinsic | 3 | 158 | 0.0305 | 0.0059 | 5.1366 |
| SVM TF-IDF coefficients | 3 | 158 | 0.0867 | 0.0212 | 4.0892 |

The intrinsic projection explanations pass a basic faithfulness test: deleting high-contribution terms reduces model scores substantially more than deleting random nonzero terms.

### Paired Bootstrap Analysis

| Comparison | Observed Macro-F1 Difference | 95% CI | Two-sided p |
| --- | ---: | --- | ---: |
| Hybrid vs. TF-IDF Linear SVM | 0.0071 | [-0.0094, 0.0229] | 0.407 |
| Hybrid vs. TF-IDF Logistic Regression | 0.0010 | [-0.0217, 0.0223] | 0.982 |
| Hybrid vs. Contrastive Projection | 0.0816 | [0.0330, 0.1250] | 0.000 |

The bootstrap analysis supports a cautious interpretation. The hybrid model is clearly stronger than the pure contrastive projection, but its advantage over strong TF-IDF baselines is small and not statistically decisive in the current sample.

## Paper and Review Artifact

Paper source files:

```text
paper/main.tex
paper/references.bib
```

Recommended compiler:

```text
pdfLaTeX
```

Packaged review artifact:

```text
artifacts/nfr_eai_fisat_2026_review_artifact.zip
```

The review artifact can be regenerated with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/make_review_artifact.ps1
```

## Limitations

The current study has several threats to validity:

1. **Dataset size:** NICE contains only a few hundred usable multi-label NFR instances after filtering.
2. **Label imbalance:** Several NFR categories have limited support, which affects threshold stability and fold-level variance.
3. **Baseline scope:** The implemented baselines include TF-IDF Logistic Regression, TF-IDF Linear SVM, Sentence-BERT records in the paper, and auxiliary classical experiments; fine-tuned BERT, RoBERTa, NoRBERT, ML-kNN, and classifier chains remain future work.
4. **Representation simplicity:** The quantum-inspired models currently use TF-IDF semantic states rather than contextual neural representations.
5. **Statistical power:** Five-fold cross-validation and bootstrap estimates are informative but not sufficient for strong superiority claims.
6. **Explanation evaluation:** Deletion tests measure model faithfulness, not human interpretability or expert rationale agreement.

## Future Work

The most important extensions are:

- integrate contextual embeddings into the projection space;
- compare with fine-tuned BERT, RoBERTa, DistilBERT, NoRBERT, and small language models;
- add ML-kNN, classifier chains, and calibrated binary relevance baselines;
- evaluate explanation usefulness with human annotators;
- construct cross-dataset validation protocols with compatible NFR label mappings;
- expand statistical analysis using repeated cross-validation and approximate randomization.

## Citation

If this artifact is used in academic work, please cite it as:

```bibtex
@misc{quantum_nfr_2026,
  title        = {Explainable Quantum-Inspired Multi-label Classification of Non-Functional Requirements},
  year         = {2026},
  howpublished = {\url{https://github.com/Lancelot-sys25/Quantum-Inspired-NFR-Classification}},
  note         = {Research artifact and reproducibility package}
}
```

## References

- Cleland-Huang, J., Settimi, R., Zou, X., and Solc, P. (2007). Automated classification of non-functional requirements. *Requirements Engineering*, 12(2), 103-120.
- Rejithkumar, G., and Anish, P. R. (2025). NICE: Non-Functional Requirements Identification, Classification, and Explanation Dataset. Zenodo. [https://doi.org/10.5281/zenodo.14590935](https://doi.org/10.5281/zenodo.14590935)
- Rejithkumar, G., and Anish, P. R. (2025). NICE: Non-Functional Requirements Identification, Classification, and Explanation Using Small Language Models. Zenodo. [https://doi.org/10.5281/zenodo.14709254](https://doi.org/10.5281/zenodo.14709254)
- Mitrevski, A. (2019). Software Requirements Classification Using Machine Learning Algorithms on the PROMISE_exp Dataset. [https://github.com/AleksandarMitrevski/se-requirements-classification](https://github.com/AleksandarMitrevski/se-requirements-classification)

## License

No explicit license file is currently included. Before public reuse, redistribution, or archival publication, add an appropriate open-source license and verify the redistribution terms of all external datasets.
