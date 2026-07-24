# Dataset acquisition

Dataset files are downloaded from their authoritative public records rather
than duplicated in this repository. From the repository root, run:

```bash
python scripts/download_datasets.py
```

The downloader verifies the SHA-256 digest of each file used in the submitted
experiments and writes:

- `data/raw/PROMISE-relabeled-NICE.csv` from the
  [NICE Zenodo record](https://doi.org/10.5281/zenodo.14590935), released under
  CC BY 4.0.
- `data/raw/PROMISE_exp.arff` from the public
  [PROMISE_exp source repository](https://github.com/AleksandarMitrevski/se-requirements-classification).

The raw and generated processed files remain ignored by Git. Their original
terms and attribution requirements continue to apply.
