param(
    [string]$OutputPath = "artifacts\nfr_eai_fisat_2026_review_artifact.zip"
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$output = Join-Path $root $OutputPath
$staging = Join-Path $root "artifacts\review_artifact_staging"

if (Test-Path -LiteralPath $staging) {
    Remove-Item -LiteralPath $staging -Recurse -Force
}
New-Item -ItemType Directory -Path $staging | Out-Null

$include = @(
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "src",
    "scripts",
    "tests",
    "docs\artifact_submission_checklist.md",
    "data\raw\PROMISE-relabeled-NICE.csv",
    "data\processed\nice_multilabel_nfr.csv",
    "reports",
    "paper\main.tex",
    "paper\references.bib",
    "paper\llncs.cls",
    "paper\splncs04.bst"
)

foreach ($item in $include) {
    $source = Join-Path $root $item
    if (-not (Test-Path -LiteralPath $source)) {
        Write-Warning "Skipping missing path: $item"
        continue
    }
    $destination = Join-Path $staging $item
    $destinationParent = Split-Path -Parent $destination
    New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
}

$readme = @"
# Review Artifact

This anonymized artifact contains the implementation, scripts, data files, and
generated reports needed to reproduce the experiments for the EAI FISAT 2026
submission.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\run_all_experiments.py
.\.venv\Scripts\python.exe scripts\run_nice_robustness_experiment.py
```

The main paper source is in `paper/main.tex`.
"@
$readme | Set-Content -LiteralPath (Join-Path $staging "ARTIFACT_README.md") -Encoding UTF8

New-Item -ItemType Directory -Path (Split-Path -Parent $output) -Force | Out-Null
if (Test-Path -LiteralPath $output) {
    Remove-Item -LiteralPath $output -Force
}
Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $output -Force
Remove-Item -LiteralPath $staging -Recurse -Force
Write-Host "Wrote artifact archive: $output"
