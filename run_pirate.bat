@echo off
title Desktop Pirate Launcher
echo Starting Desktop Pirate...
cd /d "%~dp0"
if exist .venv\Scripts\pythonw.exe (
    start "" ".venv\Scripts\pythonw.exe" main.py
) else if exist .venv\Scripts\python.exe (
    start "" ".venv\Scripts\python.exe" main.py
) else (
    python main.py
)
echo Desktop Pirate is sailing on your desktop!
timeout /t 2 >nul
exit

