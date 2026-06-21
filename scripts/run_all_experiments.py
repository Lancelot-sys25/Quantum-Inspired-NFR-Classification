import argparse
import subprocess
import sys
from pathlib import Path


def run_step(name: str, command: list[str], cwd: Path) -> dict:
    print(f"\n=== {name} ===")
    print(" ".join(command))
    completed = subprocess.run(command, cwd=cwd, text=True)
    return {"step": name, "returncode": completed.returncode, "command": " ".join(command)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/PROMISE-relabeled-NICE.csv")
    parser.add_argument("--promise-data", default="data/raw/PROMISE_exp.arff")
    parser.add_argument("--out-dir", default="reports")
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-sbert", action="store_true", help="Skip optional Sentence-BERT baselines.")
    parser.add_argument("--skip-promise", action="store_true", help="Skip the auxiliary PROMISE-expanded experiment.")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--random-trials", type=int, default=50)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    python = sys.executable
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    common_cv = ["--data", args.data, "--folds", str(args.folds), "--seed", str(args.seed), "--out-dir", str(out_dir)]
    sbert_flag = ["--no-sbert"] if args.no_sbert else []

    steps = [
        (
            "unit_tests",
            [python, "-m", "pytest", "tests"],
        ),
        (
            "nice_single_split",
            [
                python,
                "scripts/run_nice_multilabel_experiment.py",
                "--data",
                args.data,
                "--seed",
                str(args.seed),
                "--out-dir",
                str(out_dir),
                *sbert_flag,
            ],
        ),
        (
            "nice_cross_validation",
            [python, "scripts/run_nice_cv_experiment.py", *common_cv, *sbert_flag],
        ),
        (
            "nice_per_label_thresholds",
            [python, "scripts/run_nice_per_label_threshold_experiment.py", *common_cv, *sbert_flag],
        ),
        (
            "nice_ablation",
            [python, "scripts/run_nice_ablation_experiment.py", *common_cv],
        ),
        (
            "nice_explainability_deletion",
            [
                python,
                "scripts/run_explainability_deletion_test.py",
                "--data",
                args.data,
                "--seed",
                str(args.seed),
                "--top-k",
                str(args.top_k),
                "--random-trials",
                str(args.random_trials),
                "--out-dir",
                str(out_dir),
            ],
        ),
    ]

    if not args.skip_promise:
        steps.append(
            (
                "promise_auxiliary",
                [
                    python,
                    "scripts/run_promise_experiment.py",
                    "--data",
                    args.promise_data,
                    "--seed",
                    str(args.seed),
                    "--out-dir",
                    str(out_dir),
                ],
            )
        )

    results = []
    for name, command in steps:
        result = run_step(name, command, root)
        results.append(result)
        if result["returncode"] != 0:
            print(f"\nStopping because step `{name}` failed with exit code {result['returncode']}.")
            break

    summary_path = out_dir / "run_all_experiments_summary.md"
    lines = ["# Run-all Experiments Summary", ""]
    for result in results:
        status = "PASS" if result["returncode"] == 0 else "FAIL"
        lines.append(f"- `{status}` `{result['step']}`")
        lines.append(f"  - Command: `{result['command']}`")
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    failed = [result for result in results if result["returncode"] != 0]
    print(f"\nWrote run summary: {summary_path}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
