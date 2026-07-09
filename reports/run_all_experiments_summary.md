# Run-all Experiments Summary

- `PASS` `unit_tests`
  - Command: `E:\SU26\Reports\.venv\Scripts\python.exe -m pytest tests`
- `PASS` `nice_single_split`
  - Command: `E:\SU26\Reports\.venv\Scripts\python.exe scripts/run_nice_multilabel_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --out-dir reports`
- `PASS` `nice_cross_validation`
  - Command: `E:\SU26\Reports\.venv\Scripts\python.exe scripts/run_nice_cv_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports`
- `PASS` `nice_per_label_thresholds`
  - Command: `E:\SU26\Reports\.venv\Scripts\python.exe scripts/run_nice_per_label_threshold_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports`
- `PASS` `nice_ablation`
  - Command: `E:\SU26\Reports\.venv\Scripts\python.exe scripts/run_nice_ablation_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports`
- `PASS` `nice_explainability_deletion`
  - Command: `E:\SU26\Reports\.venv\Scripts\python.exe scripts/run_explainability_deletion_test.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --top-k 3 --random-trials 50 --out-dir reports`
- `PASS` `nice_robustness_and_bootstrap`
  - Command: `E:\SU26\Reports\.venv\Scripts\python.exe scripts/run_nice_robustness_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --top-k 3 --random-trials 50 --out-dir reports`
- `PASS` `promise_auxiliary`
  - Command: `E:\SU26\Reports\.venv\Scripts\python.exe scripts/run_promise_experiment.py --data data/raw/PROMISE_exp.arff --seed 42 --out-dir reports`
