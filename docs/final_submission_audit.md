# Final Submission Audit for EAI FISAT 2026

Date checked: 2026-07-16

## Verified Experiment Run

The full experiment pipeline was rerun successfully with:

```powershell
.\.venv\Scripts\python.exe scripts\run_all_experiments.py
```

Passed steps:

- `unit_tests`
- `nice_single_split`
- `nice_cross_validation`
- `nice_per_label_thresholds`
- `nice_ablation`
- `nice_explainability_deletion`
- `nice_robustness_and_bootstrap`
- `promise_auxiliary`

The Sentence-BERT baseline was first cached locally with:

```powershell
.\.venv\Scripts\python.exe -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

The auxiliary PROMISE-expanded source file is included at
`data/raw/PROMISE_exp.arff`, so `scripts/run_promise_experiment.py` no longer
depends on an absent local-only file.

The fine-tuned transformer baseline was also run successfully with:

```powershell
.\.venv\Scripts\python.exe scripts\run_nice_finetuned_transformer_experiment.py --model-name distilbert-base-uncased --folds 5 --epochs 2 --batch-size 16 --learning-rate 5e-5 --use-pos-weight --calibration per_label
```

It produced Macro-F1 `0.5333 +/- 0.0591` in
`reports/nice_finetuned_transformer_distilbert_base_uncased_summary.csv`.

## Verified Manuscript Build

`paper/main.tex` was rebuilt successfully with Tectonic and the required
`lmodern` plus `microtype` packages. The generated `paper/main.pdf` has 15
pages total. Text extraction confirms:

- page 1 contains `Anonymous Author(s)`;
- `Conclusion`, `Reproducibility`, `Acknowledgements`, the disclosure of
  interests, and `References` begin on page 14;
- references continue and finish on page 15.

Under the supervisor's counting rule (body excluding references and disclosure
sections), the body is 14 pages.

PDF metadata contains only generic TeX fields (`Creator`, `Producer`, and
`CreationDate`) and no author name.

## Supervisor Feedback Coverage

### A1. Interference contradiction

Resolved in the paper and verified by `reports/nice_ablation_summary.csv`.
Interference is not presented as an accuracy contribution. It is reported as a
tested label-coupling mechanism that is largely inactive for positive
projection and harmful for contrastive projection in the current TF-IDF setup.

### A2. Quantum contribution

Resolved by reporting the isolated hybrid-vs-SVM contribution and paired
bootstrap results in `reports/quantum_contribution_effect_sizes.csv` and
`reports/nice_paired_bootstrap_summary.csv`. The paper states that the hybrid
gain is small, directionally positive, and not statistically significant.

### A3. Dataset scope

Improved. The main evidence remains one multi-label NICE dataset, and the
paper states this limitation explicitly. The PROMISE-expanded auxiliary
experiment is reproducible from the artifact, but it remains single-label and
does not replace a second multi-label NFR corpus. A cross-validated fine-tuned
DistilBERT baseline has been added, so the paper no longer relies only on
frozen Sentence-BERT embeddings for neural comparison.

### A4. Propositions

Resolved in `paper/main.tex`. Proposition 1 is now framed as ranking
invariance under row-wise normalization rather than as an independent
per-label threshold equivalence.

### A5. Explainability

Improved with ERASER-style comprehensiveness and sufficiency metrics, plus a
TF-IDF SVM coefficient baseline in `reports/nice_deletion_comparison_summary.csv`.
The paper keeps the claim scoped to model faithfulness, not human usefulness.
The sufficiency sign convention is now stated explicitly: lower is better, and
negative sufficiency means the rationale-only input received a slightly higher
score than the full input.

### Latest supervisor feedback

The latest feedback round is addressed in
`docs/supervisor_response_latest.md`. The main changes are:

- body reduced and verified at 14 pages;
- abstract, introduction, and conclusion reframed around positive intrinsic
  explanation and diagnostic geometry contributions;
- fine-tuned DistilBERT retained only in the per-label-threshold CV table after
  protocol provenance was checked;
- AI disclosure revised to describe assistance accurately while preserving
  author responsibility;
- the contingent institutional publication award is disclosed as a financial
  interest rather than being mislabeled as research funding;
- `docs/author_mastery_checklist.md` added for Proposition, statistics, power,
  and sufficiency oral-defense preparation.

## Submission Package Checks

- Anonymous manuscript source: `paper/main.tex`
- The non-anonymous camera-ready source must not be uploaded for review.
- Artifact packager: `scripts/make_review_artifact.ps1`
- Review artifact output: `artifacts/nfr_eai_fisat_2026_review_artifact.zip`
- Raw datasets included in artifact:
  - `data/raw/PROMISE-relabeled-NICE.csv`
  - `data/raw/PROMISE_exp.arff`
- Pinned dependencies included: `requirements-lock.txt`
- `reports/run_all_experiments_summary.md` was scrubbed of absolute local
  machine paths; commands are recorded as portable `python ...` invocations.

## Remaining Human Submission Checks

- Optionally rebuild `paper/main.pdf` in Overleaf, TeX Live, or MiKTeX before
  uploading, especially if Confy+ expects a PDF produced by pdfLaTeX rather
  than Tectonic/XeTeX.
- Confirm Confy+ track/scope selection manually.
- Upload only anonymous review files and the anonymized artifact.
