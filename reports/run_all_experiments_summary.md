# Run-all Experiments Summary

- `PASS` `unit_tests`
  - Command: `D:\ProjectSWR\quantum_re_nfr_project\.venv\Scripts\python.exe -m pytest tests`
- `PASS` `nice_single_split`
  - Command: `D:\ProjectSWR\quantum_re_nfr_project\.venv\Scripts\python.exe scripts/run_nice_multilabel_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --out-dir reports`
- `PASS` `nice_cross_validation`
  - Command: `D:\ProjectSWR\quantum_re_nfr_project\.venv\Scripts\python.exe scripts/run_nice_cv_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports`
- `PASS` `nice_per_label_thresholds`
  - Command: `D:\ProjectSWR\quantum_re_nfr_project\.venv\Scripts\python.exe scripts/run_nice_per_label_threshold_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports`
- `PASS` `nice_ablation`
  - Command: `D:\ProjectSWR\quantum_re_nfr_project\.venv\Scripts\python.exe scripts/run_nice_ablation_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports`
- `PASS` `nice_explainability_deletion`
  - Command: `D:\ProjectSWR\quantum_re_nfr_project\.venv\Scripts\python.exe scripts/run_explainability_deletion_test.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --top-k 3 --random-trials 50 --out-dir reports`
- `PASS` `promise_auxiliary`
  - Command: `D:\ProjectSWR\quantum_re_nfr_project\.venv\Scripts\python.exe scripts/run_promise_experiment.py --data data/raw/PROMISE_exp.arff --seed 42 --out-dir reports`
