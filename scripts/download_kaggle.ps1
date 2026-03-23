$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $repoRoot "dashboard\data"

if (-not (Test-Path $dataDir)) {
  New-Item -ItemType Directory -Path $dataDir | Out-Null
}

Write-Host "== Kaggle download script ==" -ForegroundColor Cyan
Write-Host "Target folder: $dataDir"

Write-Host "`nChecking Kaggle CLI..."
try {
  python -m kaggle.cli --version | Out-Null
} catch {
  Write-Host "Kaggle CLI not found. Installing (user scope)..." -ForegroundColor Yellow
  python -m pip install --user kaggle
}

$kaggleDir = Join-Path $HOME ".kaggle"
$tokenPath = Join-Path $kaggleDir "kaggle.json"

if (-not (Test-Path $tokenPath)) {
  Write-Host "`nERROR: kaggle.json not found at $tokenPath" -ForegroundColor Red
  Write-Host "Download it from https://www.kaggle.com/settings and place it there."
  exit 1
}

Write-Host "`nDownloading Solar Power Generation Data..."
python -m kaggle.cli datasets download -d anikannal/solar-power-generation-data -p $dataDir --unzip

Write-Host "`nDownloading Smart Grid Intrusion Detection..."
python -m kaggle.cli datasets download -d hussainsheikh03/smart-grid-intrusion-detection-dataset -p $dataDir --unzip

Write-Host "`nDone. Kaggle datasets are in $dataDir" -ForegroundColor Green
