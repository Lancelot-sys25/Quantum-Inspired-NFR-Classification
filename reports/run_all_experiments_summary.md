# Run-all Experiments Summary

- `PASS` `unit_tests`
  - Command: `C:\Users\Win 11\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests`
- `PASS` `nice_single_split`
  - Command: `C:\Users\Win 11\AppData\Local\Programs\Python\Python312\python.exe scripts/run_nice_multilabel_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --out-dir reports_rerun`
- `PASS` `nice_cross_validation`
  - Command: `C:\Users\Win 11\AppData\Local\Programs\Python\Python312\python.exe scripts/run_nice_cv_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports_rerun`
- `PASS` `nice_per_label_thresholds`
  - Command: `C:\Users\Win 11\AppData\Local\Programs\Python\Python312\python.exe scripts/run_nice_per_label_threshold_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports_rerun`
- `PASS` `nice_ablation`
  - Command: `C:\Users\Win 11\AppData\Local\Programs\Python\Python312\python.exe scripts/run_nice_ablation_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports_rerun`
- `PASS` `nice_explainability_deletion`
  - Command: `C:\Users\Win 11\AppData\Local\Programs\Python\Python312\python.exe scripts/run_explainability_deletion_test.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --top-k 3 --random-trials 50 --out-dir reports_rerun`
- `PASS` `nice_robustness_and_bootstrap`
  - Command: `C:\Users\Win 11\AppData\Local\Programs\Python\Python312\python.exe scripts/run_nice_robustness_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --top-k 3 --random-trials 50 --out-dir reports_rerun`
