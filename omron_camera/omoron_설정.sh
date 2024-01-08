Graphic Driver: 
NVIDIA RTX / Quadro Desktop And Notebook Driver Release 535
R535 U9 (537.99)  WHQL
https://www.nvidia.co.kr/download/driverResults.aspx/216862/kr
537.99-quadro-rtx-desktop-notebook-win10-win11-64bit-international-dch-whql.exe
CUDA
CUDA 11.8
https://developer.nvidia.com/cuda-11-8-0-download-archive
cuda_11.8.0_522.06_windows.exe
cuDNN
Download cuDNN v8.9.7 (December 5th, 2023), for CUDA 11.x
https://developer.nvidia.com/rdp/cudnn-download#a-collapse897-118
cudnn-windows-x86_64-8.9.7.29_cuda11-archive.zip
Python: 
Python 3.10.11
https://www.python.org/downloads/release/python-31011
python-3.10.11-amd64.exe
Code: 
https://code.visualstudio.com/docs/?dv=win64user
VSCodeUserSetup-x64-1.85.0.exe
==========================================
[Setup Python Virtual environment:]
c:\> py -m venv .venv
c:\> .venv\Scripts\activate
(.venv) c:\> python.exe -m pip install --upgrade pip
[Pytorch install]
https://pytorch.org/
(.venv) c:\> pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
(.venv) c:\> pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
[YOLOv8 Install]
https://docs.ultralytics.com/quickstart/
(.venv) c:\> pip install ultralytics
[Training data]
2 class (1080x1080)
https://app.roboflow.com/ds/GOSB8XPKhk?key=qo0iZw0of1
3 class (1080x1080)
https://app.roboflow.com/ds/u56AdDFShh?key=aBmFFvzmH4
=============================================================
roboflow
https://github.com/roboflow/notebooks/blob/main/README.md
github
git config --global user.email astroeye@hotmail.com
git config --global user.name had
git config --global core.autocrlf true
…or create a new repository on the command line
echo "# maketek" >> README.md
git init git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/iiiiyou/maketek.git
git push -u origin main
…or push an existing repository from the command line
git remote add origin https://github.com/iiiiyou/maketek.git
git branch -M main
git push -u origin main

===================================================================

https://blog.naver.com/laonple/220851774996

GenICam - 
	산업용 카메라들의 인터페이스 제조사, 보드 제조사들의 API가 다르다.
	어플리케이션 개발 통합을 위해 EMVA는 GenICam 표준을 제정했다.

GenTL(Generic Transport Layer)
	카메라를 검색, 카메라 레지스터에 엑세스, 스트리밍 데이터와 이벤트 수신
	
	

GenApi(Generic Application Programming Interface)는

XML(Extensible Markup Language) 포맷의 파일을

카메라로부터 가져와 카메라에서 수행되는 기능들을 열거하고

카메라의 레지스터를 맵핑하는 역할을 합니다.



SFNC(Standard Feature Naming Convention)은

카메라의 XML에 담긴 카메라의 기능 및 특징의

이름 및 형태 등을 표준화하는 역할을 합니다.

서로 다른 제조사 카메라일지라도 같은 이름으로

같은 기능을 수행하게 만드는 것에 목적이 있습니다.



GenCP(Generic Control Protocol)은 제어 프로토콜을 위한

패킷 레이아웃을 표준화하는 역할을 합니다.

앞서 설명한 GeniCAM 표준을 지원하는 카메라를 사용한다면,

어플리케이션의 변화 없이 카메라만 변경하여

쉽고 빠르게 적용시킬 수 있습니다.

이것이 GeniCAM 표준의 장점이라고 할 수 있습니다.


===========================================================
st_system.create_first_device()
<stapipy.PyStDevice object at 0x000001D620E6C040>

st_system.interface_count
3
st_system.get_interface(0)
<stapipy.PyStInterface object at 0x000001D621E85950>
st_system.get_interface(1)
<stapipy.PyStInterface object at 0x000001D621E87860>
st_system.get_interface(2)
<stapipy.PyStInterface object at 0x000001D620E32F40>

===========================================================
get_interface(self, size_t index) → PyStInterface
Open interface module of GenTL and acquire the module.

Parameters
index (int) – Interface index from 0 to interface_count - 1.

Returns
The Interface module.

Return type
PyStInterface
===========================================================
st_system.get_interface(1).device_count
1
st_system.get_interface(0).device_count
0
st_system.get_interface(2).device_count
0

st_system.get_interface(1).info.interface_id
'18:60:24:1A:61:F3'

st_interface.create_device_by_id(device_id)
st_device.info.device_id
'D4:7C:44:31:01:8E'


