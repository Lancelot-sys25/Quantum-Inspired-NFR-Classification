# Explainable Quantum-Inspired Multi-label Classification of Non-Functional Requirements

This repository contains the official implementation, dataset acquisition and
processing scripts, evaluation reports, and LaTeX manuscript for the paper:
**"Explainable Quantum-Inspired Multi-label Classification of Non-Functional
Requirements"** submitted to EAI FISAT 2026.

---

## Overview

Non-Functional Requirements (NFR) classification is a critical phase in software engineering that ensures software quality attributes (such as Security, Usability, Reliability, and Performance) are systematically addressed. Since real-world requirements often exhibit overlapping characteristics (e.g., a requirement touching both usability and security), this task is inherently multi-label.

This project introduces a **Quantum-Inspired Classifier** built upon semantic vector projections within a Hilbert space. By mapping text requirements to quantum states and utilizing positive and contrastive projection operators, the model achieves:
1. **Calibrated Multi-label Classification:** Custom thresholding is applied per NFR category to address class imbalance.
2. **Intrinsic Explainability:** Token-level semantic projection scores act as high-faithfulness explanations without requiring post-hoc explanation models (such as LIME or SHAP).
3. **Low Computational Footprint:** Unlike heavy deep learning baselines, our model is highly lightweight, requiring no GPU acceleration or large pretrained checkpoints for execution.

---

## Repository Structure

```directory
├── data/
│   ├── raw/                 # Original requirements files (NICE and PROMISE_exp)
│   └── processed/           # Filtered/derived datasets used by the scripts
├── docs/                    # Reproducibility checklists and documentation
├── paper/                   # LaTeX manuscript files (main.tex, references.bib, style classes)
├── reports/                 # Auto-generated experiment reports and raw metric outputs
├── scripts/                 # Executable scripts for running training, ablation, and evaluation
├── src/
│   └── quantum_re_nfr/      # Core package containing model definitions, metrics, and data loaders
├── tests/                   # Unit tests verifying package correctness
├── requirements.txt         # Package dependencies
└── pyproject.toml           # Python package configuration
```

---

## Installation & Setup

Ensure you have Python 3.10+ (Python 3.11.9 recommended) installed on your system.

1. **Obtain the repository:**
   ```bash
   # Clone or extract this repository, then:
   cd Quantum-Inspired-NFR-Classification
   ```

2. **Set up a virtual environment:**
   * **Windows:**
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * **Linux/macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Download and verify the exact datasets used in the experiments:**
   ```bash
   python scripts/download_datasets.py
   ```
   The script downloads NICE from its CC BY 4.0 Zenodo record and PROMISE_exp
   from its public source repository, verifies their SHA-256 digests, and
   writes them to `data/raw/`. See `data/README.md` for attribution and source
   links.

For bit-level reproduction of the submitted tables, use the pinned environment:
```bash
pip install -r requirements-lock.txt
pip install -e .
```

The optional Sentence-BERT baseline downloads
`sentence-transformers/all-MiniLM-L6-v2` on its first run. If the first run is
interrupted by a network error, run the pipeline again after the model is cached,
or pre-cache it with:
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

---

## Running Experiments

After running `python scripts/download_datasets.py`, reproduce the findings
reported in the paper with the scripts below:

### 1. Run the Entire Pipeline
To run preprocessing, baseline training (including TF-IDF and SBERT), quantum model training, and generate the summary reports, run:
```bash
python scripts/run_all_experiments.py
```
The summary report will be generated at `reports/run_all_experiments_summary.md`.
The fine-tuned DistilBERT baseline is CPU-intensive and can be included with:
```bash
python scripts/run_all_experiments.py --include-finetuned-transformer
```

### 2. Ablation Studies (Noise & Projector Configurations)
To analyze the impact of the quantum interference matrix (noise coupling) and test projection combinations:
```bash
python scripts/run_nice_ablation_experiment.py
```
This produces tabular reports at `reports/nice_ablation_summary.csv` and details how turning off the noise parameters affects the system.

### 3. Explainability & Faithfulness Evaluation (ERASER Framework)
To verify the faithfulness of the token-level explanations against classical baselines using **Comprehensiveness** and **Sufficiency** metrics:
```bash
python scripts/run_nice_robustness_experiment.py
```
This produces the deletion test report at `reports/nice_explainability_deletion_report.md`.

### 4. Cross-Dataset Generalizability Validation
To test generalizability, we validate the model's performance on the single-label `PROMISE-expanded` dataset:
```bash
python scripts/run_promise_experiment.py
```
The dataset downloader places the verified source file at
`data/raw/PROMISE_exp.arff`.

### 5. Fine-tuned Transformer Baseline
To run the task-adapted DistilBERT baseline reported in the paper:
```bash
python scripts/run_nice_finetuned_transformer_experiment.py --model-name distilbert-base-uncased --folds 5 --epochs 2 --batch-size 16 --learning-rate 5e-5 --use-pos-weight --calibration per_label
```

The reported DistilBERT result uses per-label threshold calibration only; no
global-threshold DistilBERT result is available. Reproduce the paired effect
sizes and the idealized power calculation with:

```bash
python scripts/reproduce_statistical_analysis.py
```

---

## Experimental Results

Below is a summary of the empirical findings obtained during our evaluation:

### Classification Performance (Global-threshold 5-Fold CV on NICE)

| Classifier | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| :--- | :---: | :---: | :---: | :---: |
| Label Frequency Baseline | 0.2328 | 0.2083 | 0.7927 | 0.4059 |
| TF-IDF Logistic Regression | 0.6787 | 0.5977 | **0.0759** | 0.7990 |
| TF-IDF Linear SVM | 0.6821 | 0.6049 | 0.0764 | 0.8056 |
| **Hybrid (Quantum + SVM)** | **0.6839** | 0.6084 | 0.0768 | 0.8040 |
| *Sentence-BERT (Dense Embedding)* | *0.6493* | **0.6121** | *0.0919* | **0.8361** |

*Note: Sentence-BERT has the highest Macro-F1 and LRAP. The Hybrid model is the
strongest non-embedding model by Macro-F1, but its gain over TF-IDF baselines is
small and not statistically significant at the current dataset size.*

### Classification Performance (Per-label-threshold 5-Fold CV on NICE)

| Classifier | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| :--- | :---: | :---: | :---: | :---: |
| TF-IDF Logistic Regression | 0.6219 | 0.5629 | 0.0967 | 0.7990 |
| TF-IDF Linear SVM | 0.6085 | 0.5640 | 0.1057 | 0.8056 |
| **Hybrid (Quantum + SVM)** | 0.6178 | 0.5854 | 0.1027 | 0.8040 |
| *Sentence-BERT (Dense Embedding)* | **0.6386** | **0.5990** | **0.0947** | **0.8361** |
| Fine-tuned DistilBERT | 0.5420 | 0.5333 | 0.1402 | 0.7105 |

*Fine-tuned DistilBERT was evaluated only under this per-label protocol, so its
row must not be reused in the global-threshold table.*

### Explanation Faithfulness (ERASER Benchmark)

Faithfulness metrics evaluated across 158 true test split assignments for the top-3 rationales:

| Model | Comprehensiveness $\uparrow$ | Sufficiency $\downarrow$ | Faithfulness Ratio (to Random) |
| :--- | :---: | :---: | :---: |
| **Contrastive Projection** | **0.0305** | **-0.0395** | **5.21x (Comp)** |
| TF-IDF Linear SVM | 0.0867 | 0.0484 | 4.01x (Comp) |

*The negative sufficiency metric for the Contrastive Projection model means
that keeping only the selected rationale slightly increases the prediction
score. This may indicate that other tokens add background noise, but it is not
evidence of human usefulness and is interpreted cautiously.*

---

## Manuscript Compilation

The scientific paper source files are located in the `paper/` directory.

To compile the LaTeX document (requires a local TeX Live/MiKTeX installation or Overleaf):
```bash
pdflatex paper/main.tex
bibtex paper/main
pdflatex paper/main.tex
pdflatex paper/main.tex
```

---

## Publication and Metadata

* **Conference:** EAI FISAT 2026 (EAI FPT International Conference on Intelligent Systems and Advanced Technologies)
* **Publisher:** Springer - Lecture Notes in Computer Science (LNCS) / EAISICC Series
* **Submissions Anonymization:** Double-blind review (names and source codes are anonymized for review purposes).
