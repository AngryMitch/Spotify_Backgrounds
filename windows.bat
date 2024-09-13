@echo off
REM Script to initialize venv
call windows_dist\activate_venv.bat

REM Call the batch files in windows_dist to set up the environment and install requirements
call windows_dist\install_requirements.bat

REM Run the Python script
python scripts\__init__.py

pause
