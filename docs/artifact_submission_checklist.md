# Artifact Submission Checklist

Use this checklist before submitting the EAI FISAT 2026 paper.

## Anonymous Review

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

4. Rebuild `paper/main.pdf` from `paper/main.tex` and confirm the anonymous
   author block, references, and page count.

5. Run the artifact packager:

   ```powershell
   .\scripts\make_review_artifact.ps1
   ```

6. Upload `artifacts\nfr_eai_fisat_2026_review_artifact.zip` to an anonymous
   artifact host, for example Anonymous GitHub or Anonymous 4open.science.

7. Replace the reproducibility placeholder in the paper or submission form with
   the anonymous artifact URL.

8. Check that the uploaded archive does not expose author names through Git
   history, local paths, PDF metadata, or account ownership.

## Camera-ready

1. Create a final public repository or archive after review.
2. Mint a Zenodo DOI for the camera-ready artifact.
3. Replace the anonymous review URL with the DOI.
