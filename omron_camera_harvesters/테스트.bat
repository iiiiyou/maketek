@echo off
:restart

call C:\workspace\maketek\.venv\Scripts\activate
cd C:\workspace\maketek\gui
python gui_test_model_tkinter_camera1_,NoPLC_save_img_function.py

REM 5초 대기
timeout /t 2 >nul

REM 다시 시작
goto restart