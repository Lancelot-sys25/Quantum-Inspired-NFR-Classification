# Review Artifact

This anonymized artifact contains the implementation, scripts, data files, and
generated reports needed to reproduce the experiments for the EAI FISAT 2026
submission.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe scripts\run_all_experiments.py
.\.venv\Scripts\python.exe scripts\run_nice_finetuned_transformer_experiment.py --model-name distilbert-base-uncased --folds 5 --epochs 2 --batch-size 16 --learning-rate 5e-5 --use-pos-weight --calibration per_label
.\.venv\Scripts\python.exe scripts\reproduce_statistical_analysis.py
.\.venv\Scripts\python.exe scripts\run_nice_robustness_experiment.py
```

The pinned `requirements-lock.txt` is used above for exact reproduction; the
loose `requirements.txt` is provided for exploratory installation. The first
full run downloads the `sentence-transformers/all-MiniLM-L6-v2` model into the
local Hugging Face cache; subsequent runs can be executed from that cache.

The reported fine-tuned DistilBERT result was generated with per-label
threshold calibration only. It must not be interpreted as a global-threshold
result.

The main paper source is in `paper/main.tex`.
