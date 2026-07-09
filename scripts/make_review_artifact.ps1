param(
    [string]$OutputPath = "artifacts\nfr_eai_fisat_2026_review_artifact.zip"
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$output = Join-Path $root $OutputPath
$staging = Join-Path ([System.IO.Path]::GetTempPath()) ("nfr_review_artifact_staging_" + [System.Guid]::NewGuid().ToString("N"))

if (Test-Path -LiteralPath $staging) {
    Remove-Item -LiteralPath $staging -Recurse -Force
}
New-Item -ItemType Directory -Path $staging | Out-Null

$include = @(
    "requirements.txt",
    "requirements-lock.txt",
    "pyproject.toml",
    "src",
    "scripts",
    "tests",
    "docs\artifact_submission_checklist.md",
    "docs\final_submission_audit.md",
    "data\raw\PROMISE-relabeled-NICE.csv",
    "data\raw\PROMISE_exp.arff",
    "data\processed\nice_multilabel_nfr.csv",
    "data\processed\promise_exp_nfr_11class.csv",
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

Get-ChildItem -LiteralPath $staging -Recurse -Directory -Force |
    Where-Object { $_.Name -eq "__pycache__" -or $_.Name -like "*.egg-info" } |
    Remove-Item -Recurse -Force

Get-ChildItem -LiteralPath $staging -Recurse -File -Force |
    Where-Object { $_.Extension -in @(".pyc", ".pyo") } |
    Remove-Item -Force

$readme = @'
# Review Artifact

This anonymized artifact contains the implementation, scripts, data files, and
generated reports needed to reproduce the experiments for the EAI FISAT 2026
submission.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe scripts\run_all_experiments.py
.\.venv\Scripts\python.exe scripts\run_nice_robustness_experiment.py
```

For exact reproduction of the submitted tables, use `requirements-lock.txt`
instead of the loose dependency bounds in `requirements.txt`. The first full
run downloads the `sentence-transformers/all-MiniLM-L6-v2` model into the
local Hugging Face cache; subsequent runs can be executed from that cache.

The main paper source is in `paper/main.tex`.
'@
$readme | Set-Content -LiteralPath (Join-Path $staging "README.md") -Encoding UTF8
$readme | Set-Content -LiteralPath (Join-Path $staging "ARTIFACT_README.md") -Encoding UTF8

New-Item -ItemType Directory -Path (Split-Path -Parent $output) -Force | Out-Null
if (Test-Path -LiteralPath $output) {
    Remove-Item -LiteralPath $output -Force
}
Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $output -Force
Remove-Item -LiteralPath $staging -Recurse -Force
Write-Host "Wrote artifact archive: $output"
