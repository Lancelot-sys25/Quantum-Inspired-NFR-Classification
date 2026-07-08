# Review Artifact

This anonymized artifact contains the implementation, scripts, data files, and
generated reports needed to reproduce the experiments for the EAI FISAT 2026
submission.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\run_all_experiments.py
.\.venv\Scripts\python.exe scripts\run_nice_robustness_experiment.py
```

The main paper source is in `paper/main.tex`.
