# Artifact Submission Checklist

Use this checklist before submitting the EAI FISAT 2026 paper.

## Anonymous Review

1. Run the artifact packager:

   ```powershell
   .\scripts\make_review_artifact.ps1
   ```

2. Upload `artifacts\nfr_eai_fisat_2026_review_artifact.zip` to an anonymous
   artifact host, for example Anonymous GitHub or Anonymous 4open.science.

3. Replace the reproducibility placeholder in the paper or submission form with
   the anonymous artifact URL.

4. Check that the uploaded archive does not expose author names through Git
   history, local paths, PDF metadata, or account ownership.

## Camera-ready

1. Create a final public repository or archive after review.
2. Mint a Zenodo DOI for the camera-ready artifact.
3. Replace the anonymous review URL with the DOI.
