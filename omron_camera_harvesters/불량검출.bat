@echo off
:restart

call C:\workspace\maketek\.venv\Scripts\activate
cd C:\workspace\maketek\gui
python gui.py

REM 5초 대기
timeout /t 2 >nul

REM 다시 시작
goto restart