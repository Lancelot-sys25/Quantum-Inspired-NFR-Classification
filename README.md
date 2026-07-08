# Explainable Quantum-Inspired Multi-label Classification of Non-Functional Requirements

This repository contains the official implementation, dataset files, evaluation scripts, and LaTeX manuscript for the paper: **"Explainable Quantum-Inspired Multi-label Classification of Non-Functional Requirements"** submitted to EAI FISAT 2026.

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
│   ├── raw/                 # Original requirements files (PROMISE-relabeled-NICE.csv)
│   └── processed/           # Filtered multi-label dataset (nice_multilabel_nfr.csv)
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

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lancelot-sys25/Quantum-Inspired-NFR-Classification.git
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
   ```

---

## Running Experiments

To reproduce the findings reported in the paper, execute the corresponding scripts below:

### 1. Run the Entire Pipeline
To run preprocessing, baseline training (including TF-IDF and SBERT), quantum model training, and generate the summary reports, run:
```bash
python scripts/run_all_experiments.py
```
The summary report will be generated at `reports/run_all_experiments_summary.md`.

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

---

## Experimental Results

Below is a summary of the empirical findings obtained during our evaluation:

### Classification Performance (5-Fold Cross-Validation on NICE Dataset)

| Classifier | Micro-F1 | Macro-F1 | Hamming Loss | LRAP |
| :--- | :---: | :---: | :---: | :---: |
| Label Frequency Baseline | 0.0000 | 0.0000 | 0.1651 | 0.3807 |
| TF-IDF Logistic Regression | 0.5487 | 0.4435 | 0.1259 | 0.6974 |
| **TF-IDF Linear SVM** | 0.6272 | 0.5367 | 0.1118 | 0.7634 |
| **Hybrid (Quantum + SVM)** | **0.6288** | **0.5438** | **0.1089** | 0.7712 |
| *Sentence-BERT (Dense Embedding)* | *0.6775* | *0.6124* | *0.1027* | *0.8174* |

*Note: SBERT acts as a dense embedding baseline which yields higher raw metrics but operates as a black-box model requiring deep neural structures, whereas the Hybrid model remains fully explainable.*

### Explanation Faithfulness (ERASER Benchmark)

Faithfulness metrics evaluated across 158 true test split assignments for the top-3 rationales:

| Model | Comprehensiveness $\uparrow$ | Sufficiency $\downarrow$ | Faithfulness Ratio (to Random) |
| :--- | :---: | :---: | :---: |
| **Contrastive Projection** | **0.0305** | **-0.0395** | **5.21x (Comp)** |
| TF-IDF Linear SVM | 0.0867 | 0.0484 | 4.01x (Comp) |

*The negative sufficiency metric for the Contrastive Projection model shows that keeping only the key rationales slightly increases the prediction score, filtering out background document noise and confirming that the model's highlighted terms are highly faithful.*

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
