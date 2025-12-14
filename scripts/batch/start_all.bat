@echo off
chcp 65001 > nul
cls
echo ========================================
echo    EMAIL VALIDATOR - ALL IN ONE
echo ========================================
echo.
echo Project: Email Validator Tool
echo Author:  Volodyaonly
echo Version: 1.0.0
echo ========================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
python --version
echo ✓ Python is installed
echo.

echo [2/3] Installing dependencies...
pip install dnspython requests -q
echo ✓ Dependencies installed
echo.

echo [3/3] Running email validation...
echo ----------------------------------------
python src/check_email.py --file data\emails.txt
echo ----------------------------------------
echo.

echo [BONUS] Sending test to Telegram...
python src/telegram_sender.py
echo.

echo [BONUS] System architecture...
powershell -ExecutionPolicy Bypass -File "scripts\powershell\show_architecture.ps1"
echo.

echo ========================================
echo    ALL OPERATIONS COMPLETED
echo ========================================
echo.
echo Next steps:
echo 1. Edit config.ini.example with your data
echo 2. Rename to config.ini
echo 3. Run again to test Telegram integration
echo.
pause
