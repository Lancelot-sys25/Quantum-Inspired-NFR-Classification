# Author Mastery Checklist Before Submission

This checklist exists because the paper must be defensible by the listed
authors, not only reproducible from scripts. Do not submit until every author
can explain the following without reading notes.

## Proposition 1: Interference as Label Coupling

- Define `p_l`, `M`, `M'`, and `lambda`.
- Expand `p M'` into `(1 - lambda) p_l + lambda sum_k p_k M_kl`.
- Explain why off-diagonal `M_kl` entries are cross-label coupling.
- Explain why the ablation shows interference is mathematically present but
  empirically weak or harmful in this TF-IDF setup.

## Proposition 2: Row-wise Normalization

- State what `_minmax_rows` does in `src/quantum_re_nfr/quantum_model.py`.
- Prove why row-wise min-max normalization preserves the within-instance
  ranking of labels.
- Explain why a global threshold after row-wise normalization becomes an
  instance-dependent raw-score threshold.
- Give the two-label example:
  - `u = (0.5, 0.0)` predicts label 1 after normalization;
  - `u = (0.5, 0.9)` has the same raw label-1 score but does not predict label 1.
- Explain why this means the deployed decision rule is not just independent
  per-label centroid thresholding.

## Statistical Analyses

- Explain Micro-F1, Macro-F1, Hamming loss, and LRAP.
- Explain why Wilcoxon over 5 folds has very low resolution and why `p=0.0625`
  is the smallest attainable non-zero two-sided value at `n=5`.
- Explain paired Cohen's `d_z`: mean paired difference divided by the standard
  deviation of paired differences.
- Explain why bootstrap intervals over held-out requirements are useful but do
  not replace a second independent dataset.
- Explain why an effect around `d_z = 0.5` needs roughly 30-35 paired folds for
  conventional power, and why this dataset cannot honestly provide that.

## ERASER Sufficiency

- Define comprehensiveness as score drop after deleting the rationale tokens.
- Define sufficiency as `f(x)_c - f(x_top-k)_c`.
- State that lower sufficiency is better.
- Explain why negative sufficiency is unusual but possible: the rationale-only
  input scored higher than the full input.
- Explain why the paper treats negative sufficiency cautiously as possible
  background-noise filtering, not as proof of human-useful explanations.

## Contribution Framing

- State the paper's positive contribution in one sentence:
  an intrinsically explainable quantum-inspired multi-label NFR classifier plus
  a theoretical and empirical diagnosis of when its geometry helps or does not.
- State what the paper does not claim:
  it does not claim state-of-the-art accuracy or a statistically confirmed
  accuracy gain over classical baselines.
- Explain why this is still publishable:
  reviewers can value a transparent scoring framework, intrinsic explanations,
  and a careful negative/diagnostic result if the claims are honest and useful.

## Reproducibility Ownership

- Know which script generated each major result table.
- Know where the DistilBERT numbers are stored.
- Know why the anonymous artifact should not include local paths, author names,
  institution names, email addresses, or the original GitHub link.
