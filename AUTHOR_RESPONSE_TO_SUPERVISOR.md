# Response to Supervisor

Latest feedback round: see `docs/supervisor_response_latest.md` for the
2026-07-13 response covering page count, positive contribution framing,
DistilBERT table placement, AI disclosure ownership, ERASER sufficiency, and
artifact anonymity.

This document responds point-by-point to `NHAN_XET_BAI_NFR_FISAT_2026.md`. Every claim below is backed by a file or number that can be independently checked; all newly added numbers come from rerun scripts recorded in `reports/`, and no numbers were invented.

---

## A1 — Interference contradiction (theory vs. ablation)

**Issue identified.** The submitted Proposition 2 presented the interference matrix as a genuine contribution, but the original ablation only tested interference on/off for the *contrastive* projection, not the *positive* projection, and the paper did not confront the fact that interference measurably hurt the contrastive variant.

**Experiments (re-)run.** `scripts/run_nice_ablation_experiment.py`, 5-fold CV on NICE, all four combinations: positive projection with/without interference, contrastive projection with/without interference.

**Numerical evidence** (`reports/nice_ablation_summary.csv`, reproduced in Table 4 of `paper/main.tex`):

| Variant | Macro-F1 (mean ± std) |
|---|---|
| Positive projection, no interference | 0.5526 ± 0.0285 |
| Positive projection, with interference | 0.5490 ± 0.0237 |
| Contrastive projection, no interference | 0.5397 ± 0.0398 |
| Contrastive projection, with interference | 0.4118 ± 0.0275 |

Interference leaves the positive projection essentially unchanged (−0.0037) and substantially worsens the contrastive projection (−0.1279).

**Conclusion.** Interference is not a reliable accuracy contribution. It is retained in the paper only as a mathematically interesting label-coupling mechanism (Proposition "Interference as label coupling"), explicitly downgraded to "secondary, largely inactive" — not listed as an unconditional contribution.

**Files/sections modified.** `paper/main.tex`: Introduction contribution list (line 83–87), §Ablation Study interpretation (line 535–544), Table `tab:nice-ablation`.

---

## A2 — Is the "quantum" contribution real?

**Quantum contribution, quantified.** Two separate claims were tested, not conflated:
- *Standalone*: pure quantum projection vs. TF-IDF SVM alone.
- *Fusion*: Hybrid (quantum+SVM) vs. SVM alone, isolating exactly the quantum score's marginal contribution (same TF-IDF backbone).

**Statistical significance and bootstrap** (`reports/quantum_contribution_effect_sizes.csv`, `reports/nice_paired_bootstrap_summary.csv`):

| Comparison | Δ Macro-F1 | Cohen's $d_z$ | Wilcoxon $p$ |
|---|---|---|---|
| Contrastive projection − SVM (standalone) | −0.1931 | −5.92 | 0.0625 (floor at n=5) |
| Positive projection − SVM (standalone) | −0.0559 | −1.36 | 0.0625 (floor at n=5) |
| Hybrid − SVM-only, same backbone (isolated quantum contribution) | +0.0140 | 0.49 | 0.3125 |
| Hybrid − TF-IDF SVM (main comparison) | +0.0035 | 0.73 | 0.1875 |
| Hybrid − TF-IDF LR (main comparison) | +0.0107 | 0.54 | 0.4375 |

Bootstrap (2000 resamples, held-out split): Hybrid vs. SVM +0.0081, 95% CI [−0.0100, 0.0263]; Hybrid vs. LR +0.0020, CI [−0.0205, 0.0227] — both overlap zero.

**Interpretation.** Standalone quantum is significantly *worse* than SVM (large effect, 5/5 folds — the strongest signal obtainable at n=5). The fusion gain is directionally positive but small, not significant by Wilcoxon or bootstrap, and the isolated-contribution test shows it is negative in 2 of 5 folds — i.e., fragile, not robust. A power calculation shows ~30–35 paired folds would be needed to reliably detect $d_z\approx0.5$; one 381-instance dataset under 5-fold CV cannot supply that.

**Why the final wording is scientifically justified.** The paper no longer claims the hybrid model is "competitive with, rather than superior to" baselines as a settled finding. It now states plainly that the accuracy advantage is "small, directionally positive, and not statistically significant," and repositions the contribution around interpretability and a diagnostic account of where the quantum geometry helps (fusion) and where it does not (standalone, under interference). This is the literal outcome the supervisor asked for: "nếu không [có ý nghĩa thống kê], tự quyết định tái định vị bài quanh interpretability."

**Files/sections modified.** `paper/main.tex`: Abstract, Discussion (three paragraphs rewritten with effect sizes/CI), Conclusion.

---

## A3 — Single, small dataset (~381 samples)

**Why only one multi-label dataset is currently used.** Multi-label NFR datasets with fine-grained requirement subclasses are scarce; to the best of our knowledge, NICE is the only public dataset suitable for evaluating multi-label co-occurrence and interference at the time of writing. This is stated explicitly in the paper, not left implicit.

**Fine-tuned transformer baseline added.** A cross-validated DistilBERT baseline was added via `scripts/run_nice_finetuned_transformer_experiment.py`: `distilbert-base-uncased`, 5 folds, 2 epochs per fold, batch size 16, max length 128, learning rate 5e-5, BCE loss with clipped per-label positive weights, and per-label thresholds selected on validation data. It obtains Macro-F1 `0.5333 ± 0.0591`, Micro-F1 `0.5420 ± 0.0569`, Hamming loss `0.1402 ± 0.0361`, and LRAP `0.7105 ± 0.0516` (`reports/nice_finetuned_transformer_distilbert_base_uncased_summary.csv`). It is weaker than the frozen Sentence-BERT+LR baseline and the TF-IDF/hybrid models in this small-data setting.

**Explicit acknowledgment of the limitation.** `paper/main.tex`, §Threats to Validity ("Dataset size and availability", "Baseline scope"): states plainly that a single dataset cannot establish that the observed model ranking generalizes, that NICE's own vocabulary/label distribution could independently drive the ranking, and that the new DistilBERT baseline reduces but does not eliminate baseline-scope risk because NoRBERT, RoBERTa, ML-kNN, and the NICE paper's small-language-model classifier are still not included.

**Future work.** Conclusion, Future Work paragraph now explicitly lists additional tuned BERT/RoBERTa/NoRBERT baselines under broader tuning budgets, ML-kNN as a classical multi-label baseline, evaluation on a second multi-label NFR corpus, and human rationale judgments.

**Files/sections modified.** `paper/main.tex`: Compared Models, Hyperparameters, Results, §Threats to Validity ("Dataset size and availability", "Baseline scope"), Conclusion; `scripts/run_nice_finetuned_transformer_experiment.py`; `reports/nice_finetuned_transformer_distilbert_base_uncased_*`.

---

## A4 — Proposition correctness

**What inconsistency existed.** The original Proposition 1 claimed that thresholding the projection score $s_c(r)\geq\tau$ was equivalent to a fixed, instance-independent cosine-similarity cutoff. But `predict_proba()` in `src/quantum_re_nfr/quantum_model.py` (line 35) **always** applies row-wise min–max normalization before returning a score, regardless of $\lambda$. A fixed global threshold on the normalized score does not correspond to a fixed cosine cutoff, because the normalization's min/max are computed per instance across all labels.

**How Proposition 1 now matches implementation.** Replaced with "Ranking invariance under row-wise normalization" (`paper/main.tex`, line 283–333): proves (a) within-instance label ranking is preserved by the normalization (so LRAP is unaffected, and at $\lambda=0$ this ranking equals cosine-similarity ranking — this part of the old claim was true and is kept), and (b) the actual decision threshold $\tau_i$ is instance-dependent, so two instances with identical raw scores for a label can receive opposite decisions. A concrete two-label numeric counterexample is included.

**How mathematical correctness was verified.** The proof was checked against the literal code path (`_minmax_rows` is called unconditionally on line 35 of `quantum_model.py`, independent of `interference_weight`), and the LaTeX was checked for structural integrity: `\begin`/`\end` counts for `proposition` (2/2), `proof` (2/2), `remark` (1/1) all balance; all `\label`/`\ref` pairs resolve with zero dangling or duplicate labels (verified programmatically, not by inspection alone).

**Files/sections modified.** `paper/main.tex`, §Theoretical Characterization (full replacement of Proposition 1, adjusted framing sentence for Proposition 2). No other section depends on the old proposition's specific wording.

---

## A5 — Explainability evaluation depth

**Evaluation used.** ERASER framework metrics — Comprehensiveness and Sufficiency — computed over all 158 true label assignments in the test split, with a random-deletion control baseline, and directly compared against the TF-IDF Linear SVM's own coefficient-based explanation (same data, same RNG stream, via `scripts/run_nice_robustness_experiment.py`).

**Numbers** (`reports/nice_deletion_comparison_summary.csv`):

| | Comprehensiveness | vs. random | Sufficiency | vs. random |
|---|---|---|---|---|
| Contrastive projection (intrinsic) | 0.0305 | 5.21× | −0.0395 | −1.17× |
| TF-IDF Linear SVM (coefficients) | 0.0867 | 4.01× | 0.0484 | 0.42× |

**Why this evaluation is sufficient for the current claim.** This goes beyond the original self-referential deletion test (which only compared the model's own score to itself) by (i) using ERASER's two standard metrics rather than one ad hoc one, (ii) benchmarking against a classical model's own attribution rather than only against random deletion, and (iii) reporting both directions honestly: the paper states explicitly that in *absolute* score-drop terms the SVM explanation removes more score mass (0.0867 vs. 0.0305), so the claim is scoped to "competitive on a relative, random-normalized basis," not "uniformly stronger." This qualified framing is what justifies keeping "Explainable" in the title — the claim is about faithfulness relative to chance, which is supported, not about outperforming every classical attribution method in absolute terms, which is not claimed.

**Files/sections modified.** `paper/main.tex`, §Explainability Evaluation (interpretation sentence rewritten to remove the absolute/relative conflation the earlier draft had).

---

# Conference Compliance Checklist

## B1 — Anonymity

Verified by direct, repository-wide search for usernames, real names, emails, institution names, and original repository links across every `.tex`, `.md`, `.py`, `.bib`, `.json`, `.txt`, `.ps1` file. Found and fixed one active leak in `README.md`; replaced it with a generic instruction that preserves usability. Re-ran the same search after the fix: clean, with the single expected exception of the non-anonymous camera-ready source, which is explicitly not submitted for review.

## B2 — Artifact

The anonymized artifact (`artifacts/nfr_eai_fisat_2026_review_artifact.zip`) was **regenerated from scratch**, not patched, via `scripts/make_review_artifact.ps1` (an allowlist-based packager that only copies the reproducibility files needed for review and writes fresh, generic `README.md`/`ARTIFACT_README.md` content — never touching `.git`, non-anonymous camera-ready sources, caches, or logs). After regeneration: the zip's `paper/main.tex` was diffed against the current file and found **byte-identical**; the full extracted contents were re-searched for identifying strings and found clean (only third-party citation URLs in `references.bib` and the paper's own anonymous 4open.science link remain).

## B3 — AI disclosure

Confirmed the disclosure in `paper/main.tex`, §Use of AI Tools matches the actual scope of AI assistance used in this revision: reproducibility diagnosis (dependency pinning, random-seed fix), effect-size/bootstrap/significance computation, derivation and verification of the corrected Proposition, and text drafting/revision including the contribution framing. Nothing broader or narrower than what was actually done.

## B4 — Submission package (human action required)

This repository cannot submit the paper on the authors' behalf. At submission time, the authors must manually confirm:
- The file uploaded to Confy+ is the **anonymous** `paper/main.tex` (author block reads "Anonymous Author(s)").
- The accompanying source `.zip` contains `llncs.cls`, `splncs04.bst`, `references.bib`, and the anonymous `main.tex` only.
- The non-anonymous camera-ready source is never uploaded for review; it exists solely for post-acceptance use.

## B5 — Compilation, page count, track/scope

**Compilation status:** Successful. Compiled end-to-end with Tectonic 0.16.9; the build completed with BibTeX and produced `paper/main.pdf`. Zero undefined citations or references remained after the final pass. Remaining warnings are minor overfull/underfull boxes and the known `amsmath: Unable to redefine math accent \vec` warning, with no content impact.

**Page count:** 17 pages total after adding the fine-tuned DistilBERT baseline. Per-page text extraction (via `pypdf`) shows `Conclusion` begins on page 14, `Reproducibility` and `Use of AI Tools` begin on page 15, and `References` begin on page 16. Body (Introduction through Conclusion, excluding references and disclosure sections, per the supervisor's counting rule) is therefore **approximately 14 pages** — within the requested 12–15 page body range.

**Track/Scope:** Not verifiable from the repository — selecting the correct track and Scope on Confy+ is a Confy+ web-form action the authors must perform manually; no file in this repository records or determines it.

---

# Final Verification

Cross-checked this document against every numbered item in `NHAN_XET_BAI_NFR_FISAT_2026.md`:
- Section A (A1–A5): all five items answered above with file-level evidence. Nothing in the supervisor's A-section is unaddressed.
- Section B (B1–B5): all five items checked above; B4 is correctly reported as a human action, not a repository state, per the supervisor's own framing ("các em tự soi lại... tôi sẽ kiểm lại").
- Section C (camera-ready: BOM encoding, DOI, ORCID, Acknowledgements): explicitly out of scope per the supervisor's own note ("chỉ làm sau khi có kết quả nhận — chưa gấp") and is not claimed as complete here.
- The supervisor's closing instruction asks for exactly three things: (1) the revised `.tex` — present at `paper/main.tex`; (2) an A1–A5 response with evidence — this document (and its companion `REVIEWER_RESPONSE.md`); (3) confirmation that B1–B5 were self-checked — provided above. No requested item is missing.
