@echo off
REM Install Python requirements

REM Check if the venv directory exists
if not exist windows_dist\venv\Scripts\activate.bat (
    echo Virtual environment not found. Creating virtual environment...
    python -m venv windows_dist\venv
)

REM Activate the virtual environment
call windows_dist\activate_venv.bat

REM Install the requirements
pip install -r requirements.txt
