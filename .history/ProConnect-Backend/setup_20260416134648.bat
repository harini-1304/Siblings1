@echo off
REM ProConnect Backend Setup Script for Windows

echo.
echo ============================================================
echo     ProConnect Backend Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

echo Step 1: Creating Virtual Environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo Step 2: Activating Virtual Environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

echo.
echo Step 3: Installing Dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo Step 4: Checking Environment Configuration...
if not exist ".env" (
    echo Warning: .env file not found
    echo Please create .env file with your MongoDB credentials
) else (
    echo ✓ .env file found
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Update .env file with your MongoDB connection string
echo   2. Run: python app.py
echo.
echo MongoDB Connection String should look like:
echo mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0
echo.
pause
