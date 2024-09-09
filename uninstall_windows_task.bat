@echo off
set TASK_NAME="SpotifyBackground"

REM Delete the scheduled task
schtasks /delete /tn %TASK_NAME% /f

echo Scheduled task deleted.
pause
