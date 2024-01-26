REM @echo off
call C:\workspace\maketek\.venv\Scripts\activate
cd C:\workspace\maketek\omron_camera_harvesters
python predict_omron_send_count_modbus_test.py
pause