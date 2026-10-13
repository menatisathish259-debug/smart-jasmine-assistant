@echo off
REM ========================================================================
REM Smart Jasmine Farming Assistant - Windows Setup Script (Command Prompt)
REM ========================================================================

echo [1/4] Checking Python on your system...
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PY_CMD=py
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set PY_CMD=python
    ) else (
        echo [ERROR] Python was not found on your system!
        echo Please install Python 3.10+ from python.org and check "Add Python to PATH".
        pause
        exit /b 1
    )
)

echo [2/4] Setting up virtual environment (.venv)...
if not exist ".venv\Scripts\python.exe" (
    %PY_CMD% -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo [3/4] Installing dependencies from requirements.txt...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Package installation failed. Please check your internet connection.
    pause
    exit /b 1
)

echo [4/4] Verifying setup with check_environment.py...
python check_environment.py

pause
