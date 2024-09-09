@echo off
set EXE_PATH="%~dp0__init__.exe"
set TASK_NAME="SpotifyBackground"
set TASK_DESCRIPTION="Runs Python script daily"

REM Create scheduled task to run daily at 2:00 AM
schtasks /create /tn %TASK_NAME% /tr %EXE_PATH% /sc daily /st 02:00 /f /rl HIGHEST /d MON,TUE,WED,THU,FRI,SAT,SUN /v "1.0" /description %TASK_DESCRIPTION%

echo Scheduled task created.
pause
