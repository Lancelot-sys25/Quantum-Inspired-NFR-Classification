# Response to Latest Supervisor Feedback

Date checked: 2026-07-21

## Page limit

The anonymous manuscript builds to 15 pages. The Conclusion begins on page 13;
Reproducibility, LNCS credits, and References begin on page 14; References end
on page 15. The build has no overfull boxes or unresolved references.

Repeated wording in Results, Discussion, and Threats was removed without
changing reported values, propositions, limitations, or font size.

## Claims and baselines

The paper claims intrinsic interpretability and diagnostic geometric analysis,
not state-of-the-art accuracy. Sentence-BERT leads Macro-F1 and LRAP. The
hybrid model is competitive with TF-IDF baselines, but its small accuracy gain
is not statistically confirmed. Fine-tuned DistilBERT appears only under the
per-label-threshold protocol that was actually run.

## Explainability

ERASER-style comprehensiveness and sufficiency are compared with random
deletion and an SVM coefficient baseline. Conclusions are restricted to model
faithfulness; no human-rationale usefulness claim is made.

## AI disclosure and author ownership

The disclosure is inside the LNCS `credits` environment. It reports AI
assistance and leaves responsibility with the authors. This statement is valid
only if every author can independently explain the propositions, Wilcoxon and
bootstrap results, effect size, power analysis, and sufficiency convention.

## Submission files

Use only the audited anonymous PDF and audited Overleaf source ZIP. The public
artifact must remain at the existing anonymous URL; do not create a new mirror.
