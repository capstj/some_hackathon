@echo off
REM WhisPay Setup Script for Windows
REM This script helps set up WhisPay on Windows systems

echo.
echo ============================================================
echo WhisPay - Voice Banking Assistant Setup
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/6] Python detected:
python --version
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo pip upgraded
echo.

REM Install dependencies
echo [5/6] Installing dependencies (this may take a while)...
echo This step might take 5-10 minutes depending on your internet connection
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies failed to install
    echo You may need to install them manually
    echo Common issue: pyaudio requires additional setup
    echo.
) else (
    echo Dependencies installed successfully
)
echo.

REM Create directories
echo [6/6] Creating required directories...
if not exist data mkdir data
if not exist data\users mkdir data\users
if not exist data\users\voice_prints mkdir data\users\voice_prints
if not exist data\transactions mkdir data\transactions
if not exist data\metrics mkdir data\metrics
if not exist data\models mkdir data\models
if not exist logs mkdir logs
echo Directories created
echo.

REM Copy environment file
if not exist .env (
    echo Creating .env from template...
    copy .env.example .env
    echo .env file created - please edit it with your settings
) else (
    echo .env file already exists
)
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Edit .env file if needed (optional for demo)
echo   2. Run test: python test_setup.py
echo   3. Run demo: python run_demo.py
echo   4. Run full app: python run_whispay.py
echo.
echo Note: To run WhisPay in future sessions:
echo   1. Open this folder in terminal
echo   2. Run: venv\Scripts\activate.bat
echo   3. Run: python run_whispay.py
echo.

pause
