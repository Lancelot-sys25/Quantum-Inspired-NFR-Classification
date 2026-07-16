# Response to Latest Supervisor Feedback

Date checked: 2026-07-13

## 1. Page Limit

`paper/main.tex` was rebuilt with `lmodern` and `microtype` using Tectonic.
The generated `paper/main.pdf` has 15 pages total.

PDF text extraction shows:

- pages 1-14: manuscript body through `Conclusion`;
- page 14: `Reproducibility`, `Use of AI Tools`, and beginning of references;
- page 15: remaining references.

Under the requested counting rule, excluding references and `Use of AI Tools`,
the body is at most 14 pages. The total PDF is now also within 15 pages.

Cuts made:

- compressed the long `Dataset size and availability` threat;
- shortened the Proposition 2 remark;
- removed repeated caveat wording from `Discussion`;
- folded the separate DistilBERT subsection into the result-table discussion;
- compacted `Related Work`, `Future Work`, `Reproducibility`, and `Use of AI
  Tools` so the full PDF is 15 pages, not 16.

## 2. Positive Contribution Framing

The abstract, introduction contribution paragraph, contribution list, and
conclusion were rewritten to put the positive contribution first:

- an intrinsically explainable multi-label NFR classifier;
- token-level semantic amplitude contributions without a post-hoc explainer;
- a theoretical characterization of when the quantum-inspired geometry reduces
  to cosine-style ranking and when interference or row-wise normalization gives
  cross-label coupling;
- a diagnostic ablation showing which parts help, fail, or remain inactive.

The limitations are still present, but they no longer dominate the opening
message. The paper now argues for publication as an interpretability and
diagnostic-modeling contribution, not as an inflated state-of-the-art accuracy
claim.

## 3. DistilBERT in Result Tables

Fine-tuned DistilBERT is retained only in Table `tab:nice-per-label`. Metadata
confirms that the reported run used per-label calibration, so the same row was
removed from the global-threshold Table `tab:nice-cv`.

Numbers come from
`reports/nice_finetuned_transformer_distilbert_base_uncased_summary.csv`:

- Micro-F1: `0.5420 +/- 0.0569`
- Macro-F1: `0.5333 +/- 0.0591`
- Hamming loss: `0.1402 +/- 0.0361`
- LRAP: `0.7105 +/- 0.0516`

No single-split or global-threshold DistilBERT number is reported because those
protocols were not run.

## 4. AI Disclosure and Author Ownership

`Use of AI Tools` was rewritten to describe AI as assistance for
implementation checks, dependency diagnosis, experiment re-runs,
statistical-script review, consistency checks, and language editing. It no
longer states that AI computed the intellectual core of the paper.

This is only valid if the authors actually perform the ownership check:

- re-derive and explain both propositions;
- understand the effect-size, bootstrap, Wilcoxon, and power analyses;
- explain why the paper is framed around intrinsic interpretability and
  diagnostic geometry;
- verify final claims against the code and exported result files.

A separate checklist was added in `docs/author_mastery_checklist.md` for oral
defense preparation. The paper should not be submitted until every author can
answer those questions without reading notes.

## 5. ERASER Sufficiency Convention

The Explainability Evaluation section now states the sign convention:

`Sufficiency = f(x)_c - f(x_top-k)_c`.

Lower is better because the rationale-only input should preserve the original
score. A negative value means the rationale-only input scored slightly higher
than the full requirement. The paper now interprets this cautiously as possible
background-noise filtering, not as a guarantee of human rationale quality.

The reported value remains:

- contrastive projection sufficiency: `-0.0395`;
- random keep-top baseline: score drop `0.0337`;
- sufficiency ratio: about `-1.17`.

## 6. Anonymous Artifact

The anonymous link was checked by HTTP request:

- `https://anonymous.4open.science/r/nfr-review-artifact-CE2D/`
- response status: `200 OK`.

The local review artifact was extracted and scanned for identifying strings.
One metadata issue was found: `reports/run_all_experiments_summary.md`
included absolute local machine paths. This has been fixed in both the report
and `scripts/run_all_experiments.py`; the summary now records portable
`python ...` commands.

The artifact still needs one final human browser check in an incognito window
before submission, because only the authors can inspect the live anonymous
mirror exactly as a reviewer will see it.
