# Paper Files

Upload these files to Overleaf:

- `main.tex`
- `references.bib`
- `llncs.cls`
- `splncs04.bst`

Keep all four files in the same Overleaf folder. If `references.bib` is
missing or placed in another folder, BibTeX will report that it cannot open
the database file and every citation will appear as undefined.

Recommended compiler: `pdfLaTeX`.

The clean Overleaf source archive is
`../artifacts/fisat_2026_overleaf_source_final.zip`. It contains exactly the
four files listed above. If an existing Overleaf project still contains an
older ZIP as a file inside its file tree, remove that file before exporting
the project source; otherwise the exported archive will also contain the old
manuscript. The ZIP inside this repository is for importing source into
Overleaf, not yet the final Confy+ upload archive.

For the FISAT 2026 camera-ready submission, compile and inspect the final PDF,
then upload that PDF separately in Confy+. Also create an archive containing
the same PDF and these four LaTeX source files for the source-file field.

The report uses the real experimental results generated in:

- `reports/nice_multilabel_report.md`
- `reports/nice_cv_report.md`
- `reports/promise_exp_report.md`
