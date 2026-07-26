# Artifact Submission Checklist

Use this checklist before submitting the EAI FISAT 2026 paper.

## Single-blind Review

1. Recreate the pinned Python environment if exact reproduction is required:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
   .\.venv\Scripts\python.exe -m pip install -e .
   ```

2. Pre-cache the Sentence-BERT baseline if the review machine has intermittent
   network access:

   ```powershell
   .\.venv\Scripts\python.exe -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
   ```

3. Run the full experiment pipeline and confirm every step passes:

   ```powershell
   .\.venv\Scripts\python.exe scripts\run_all_experiments.py
   ```

4. Rebuild `paper/main.pdf` from `paper/main.tex` and confirm the author
   block, references, and page count.

5. Run the artifact packager:

   ```powershell
   .\scripts\make_review_artifact.ps1
   ```

6. Upload or verify the public project repository:
   <https://github.com/Lancelot-sys25/Quantum-Inspired-NFR-Classification>.

7. Confirm the reproducibility link in the paper and submission form points to
   the public repository.

8. Check that the uploaded archive does not expose local machine paths, stale
   review-mode notes, or files unrelated to reproduction.

## Camera-ready

1. Keep the final public repository or archive synchronized with the accepted
   paper source.
2. Mint a Zenodo DOI for the camera-ready artifact.
3. Replace the public repository URL with the DOI if the proceedings require a
   DOI-backed artifact.
