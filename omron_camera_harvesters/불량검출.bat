@echo off
:restart

call C:\workspace\maketek\.venv\Scripts\activate
cd C:\workspace\maketek\omron_camera_harvesters
python predict_omron_send_good_V02.py

REM 5초 대기
timeout /t 5 >nul

REM 다시 시작
goto restart