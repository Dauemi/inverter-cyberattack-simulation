$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "== 2ASICYA One-Click Dashboard ==" -ForegroundColor Cyan
Write-Host "Repo: $repoRoot"

# 1) Download Kaggle datasets
Write-Host "`n[1/3] Downloading Kaggle datasets..."
powershell -ExecutionPolicy Bypass -File "$repoRoot\scripts\download_kaggle.ps1"

# 2) Build combined dashboard JSON
Write-Host "`n[2/3] Building combined dashboard data..."
python "dashboard\build_dashboard_data.py" `
  --html "2ASICYA_Dashboard.html" `
  --out "dashboard\data\combined_dashboard.json" `
  --france-dir "data\france_sprint3" `
  --kaggle-dir "dashboard\data" `
  --inject

# 3) Start local server
Write-Host "`n[3/3] Starting local server..."
Write-Host "Open: http://localhost:8000/2ASICYA_Dashboard.html" -ForegroundColor Green
python -m http.server 8000
