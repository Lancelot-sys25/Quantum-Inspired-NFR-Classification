# Run-all Experiments Summary

- `PASS` `unit_tests`
  - Command: `python -m pytest tests`
- `PASS` `nice_single_split`
  - Command: `python scripts/run_nice_multilabel_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --out-dir reports`
- `PASS` `nice_cross_validation`
  - Command: `python scripts/run_nice_cv_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports`
- `PASS` `nice_per_label_thresholds`
  - Command: `python scripts/run_nice_per_label_threshold_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports`
- `PASS` `nice_ablation`
  - Command: `python scripts/run_nice_ablation_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --folds 5 --seed 42 --out-dir reports`
- `PASS` `statistical_effect_sizes_and_power`
  - Command: `python scripts/reproduce_statistical_analysis.py --out-dir reports`
- `PASS` `nice_explainability_deletion`
  - Command: `python scripts/run_explainability_deletion_test.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --top-k 3 --random-trials 50 --out-dir reports`
- `PASS` `nice_robustness_and_bootstrap`
  - Command: `python scripts/run_nice_robustness_experiment.py --data data/raw/PROMISE-relabeled-NICE.csv --seed 42 --top-k 3 --random-trials 50 --out-dir reports`
- `PASS` `promise_auxiliary`
  - Command: `python scripts/run_promise_experiment.py --data data/raw/PROMISE_exp.arff --seed 42 --out-dir reports`
