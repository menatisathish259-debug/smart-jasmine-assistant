# Smart Jasmine Farming Assistant - Windows Setup Script (PowerShell)
Write-Host "============================================================" -ForegroundColor Green
Write-Host " 🌿 SMART JASMINE FARMING ASSISTANT - POWERSHELL SETUP" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

# 1. Check Python
$pyCmd = (Get-Command py -ErrorAction SilentlyContinue)
if (-not $pyCmd) {
    $pyCmd = (Get-Command python -ErrorAction SilentlyContinue)
}

if (-not $pyCmd) {
    Write-Host "[ERROR] Python was not found in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.10+ and enable 'Add Python to PATH'." -ForegroundColor Yellow
    exit 1
}

Write-Host "`n[1/4] Found Python executable: $($pyCmd.Source)" -ForegroundColor Cyan

# 2. Virtual Environment
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[2/4] Creating virtual environment (.venv)..." -ForegroundColor Cyan
    & $pyCmd.Source -m venv .venv
} else {
    Write-Host "[2/4] Virtual environment already exists." -ForegroundColor Cyan
}

# 3. Pip Install
Write-Host "[3/4] Installing dependencies from requirements.txt..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\pip.exe install -r requirements.txt

# 4. Check Environment
Write-Host "`n[4/4] Running check_environment.py..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe check_environment.py
