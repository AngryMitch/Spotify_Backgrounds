@echo off
REM Set the directory for the virtual environment
set VENV_DIR=..\venv

REM Check if the venv directory exists
if exist %VENV_DIR%\Scripts\activate.bat (
    REM Navigate to the virtual environment's Scripts directory
    call %VENV_DIR%\Scripts\activate.bat
) else (
    echo Virtual environment not found. Creating it now...
    REM Check if Python is installed
    where python >nul 2>&1
    if errorlevel 1 (
        echo Python is not installed or not found in PATH. Please install Python first.
        exit /b 1
    )
    
    REM Create the virtual environment
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Failed to create virtual environment.
        exit /b 1
    )

    REM Activate the virtual environment
    call %VENV_DIR%\Scripts\activate.bat
)
