@echo off
echo ===== Grape Leaf Disease Detection Application =====
echo Starting setup and checks...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher and try again.
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo Creating requirements.txt file...
    echo flask==2.0.1 > requirements.txt
    echo tensorflow==2.8.0 >> requirements.txt
    echo numpy==1.21.5 >> requirements.txt
    echo opencv-python==4.5.5.64 >> requirements.txt
    echo Pillow==9.0.1 >> requirements.txt
    echo werkzeug==2.0.2 >> requirements.txt
    echo scikit-learn==1.0.2 >> requirements.txt
    echo matplotlib==3.5.1 >> requirements.txt
)

REM Run the Python script
echo Running application setup and checks...
python run.py

if %errorlevel% neq 0 (
    echo An error occurred while running the application.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo Application has been stopped.
pause 