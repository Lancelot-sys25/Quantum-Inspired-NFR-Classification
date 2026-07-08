# Reproducibility Notes

This note summarizes the practical steps for checking the research artifact without reading the full paper first.

## Environment

- Python 3.10 or newer
- A virtual environment is recommended
- Dependencies are listed in `requirements.txt` and `pyproject.toml`
- **Exact versions used to generate the numbers in `paper/main.tex` and `reports/*.csv`
  are pinned in `requirements-lock.txt`.** `StratifiedKFold` / `train_test_split` with
  `shuffle=True` can produce a different fold assignment on a different scikit-learn
  version even with the same `random_state`, which silently changes every downstream
  metric. Use the lockfile, not the loose bounds in `requirements.txt`, if you need to
  reproduce the paper's tables exactly.

## Recommended Setup

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

Install dependencies (exact versions used for the paper):

```bash
pip install -r requirements-lock.txt
pip install -e .
```

Install dependencies (loose bounds, may drift over time):

```bash
pip install -r requirements.txt
pip install -e .[dev]
```

## Quick Verification

Run the unit tests first:

```bash
python -m pytest tests
```

Run a faster experiment smoke test:

```bash
python scripts/run_all_experiments.py --folds 2 --no-sbert --skip-promise --random-trials 5
```

Run the complete experiment pipeline:

```bash
python scripts/run_all_experiments.py
```

## Important Outputs

The main outputs are written to the `reports/` directory:

- `run_all_experiments_summary.md`
- `nice_multilabel_report.md`
- `nice_cv_report.md`
- `nice_ablation_report.md`
- `nice_explainability_deletion_report.md`
- `nice_robustness_report.md`

## Review Checklist

- Confirm that tests pass before running experiments.
- Confirm that the expected input dataset is available under `data/raw/`.
- Compare generated report files with the committed summaries.
- Check the paper sources in `paper/` when preparing an academic submission.
