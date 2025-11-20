@echo off
chcp 65001 >nul
title OpenBIM Tool Setup & Launch
color 0A

echo ========================================
echo    OpenBIM Cost Allocation Tool
echo        Automated Setup & Launch
echo ========================================
echo.

:: Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from:
    echo https://python.org
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo ✓ Python is installed
echo.

echo Checking Git Submodules...
git submodule update --init --recursive


:: Upgrade pip first
echo Updating pip...
python -m pip install --upgrade pip
echo.

:: Install required packages
echo Installing required libraries...
echo.

:: Core dependencies
python -m pip install streamlit
echo ✓ Streamlit installed

python -m pip install ifcopenshell
echo ✓ ifcopenshell installed

python -m pip install pandas
echo ✓ pandas installed

python -m pip install altair
echo ✓ altair installed

python -m pip install pathlib2
echo ✓ pathlib2 installed

python -m pip install numpy
echo ✓ numpy installed

python -m pip install csv
echo ✓ csv installed




echo.
echo All dependencies installed successfully!
echo.

:: Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found in current directory
    echo Please make sure this batch file is in your project folder
    pause
    exit /b 1
)

echo Starting the application...
echo.
echo The app will open in your default browser shortly...
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo Press Ctrl+C in this window to stop the server
echo ========================================
echo.

:: Run the Streamlit app
streamlit run main.py

pause