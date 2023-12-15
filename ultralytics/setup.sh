
py -m venv .venv
.venv\Scripts\activate
python.exe -m pip install --upgrade pip

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install ultralytics

pip install pymodbus
# pip install pyModbusTCP