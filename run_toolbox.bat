@echo off
cd /d "%~dp0"
rem Launch the toolbox server, then open the home page in the default browser
start "" /b cmd /c "ping -n 3 127.0.0.1 >nul && start "" http://localhost:8080"
python toolbox.py
pause