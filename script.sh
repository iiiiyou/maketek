c:\> py -m venv .venv
c:\> .venv\scripts\activate
(.venv) c:\> python.exe -m pip install --upgrade pip

# https://pytorch.org/
(.venv) c:\> pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# https://docs.ultralytics.com/quickstart/
(.venv) c:\> pip install ultralytics