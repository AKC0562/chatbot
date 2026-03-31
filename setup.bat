@echo off
REM Advanced Chatbot Setup Script for Windows

echo ============================================
echo Nexus AI - Advanced Chatbot Setup
echo ============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in your PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Python version:
python --version
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists. Skipping...
)
echo.

REM Activate virtual environment and install dependencies
echo [3/4] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Display next steps
echo [4/4] Setup Complete!
echo.
echo ============================================
echo Next Steps:
echo ============================================
echo.
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Start the backend server:
echo    python server/app.py
echo.
echo 3. Open the frontend in your browser:
echo    - Open: client/index.html
echo    - Or serve with: python -m http.server 8000 --directory client
echo.
echo 4. Access at: http://localhost:8000
echo.
echo ============================================
echo.
pause
