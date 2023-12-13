!nvidia-smi

import os
HOME = os.getcwd()
print(HOME)

# from IPython import display
# display.clear_output()

# import ultralytics
# ultralytics.checks()

from ultralytics import YOLO

from IPython.display import display, Image

%cd {HOME}
!mkdir {HOME}\\datasets
%cd {HOME}\\datasets

# !pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="bxW7hooY5jiknZS3GIxI")
# project = rf.workspace("i4umaket").project("640_two_class_20_annotation")
# dataset = project.version(2).download("yolov8")

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="bxW7hooY5jiknZS3GIxI")
project = rf.workspace("i4umaket").project("640_two_class_full_annotation")
dataset = project.version(3).download("yolov8")


%cd {HOME}

!yolo task=detect mode=train model=yolov8m.pt data={dataset.location}/data.yaml epochs=100 imgsz=640 plots=True

!dir/w {HOME}\\runs\\detect\\train6\\

%cd {HOME}
Image(filename=f'{HOME}/runs/detect/train6/confusion_matrix.png', width=640)

%cd {HOME}
Image(filename=f'{HOME}/runs/detect/train6/results.png', width=640)

%cd {HOME}
Image(filename=f'{HOME}/runs/detect/train6/val_batch0_pred.jpg', width=640)

%cd {HOME}
!yolo task=detect mode=val model={HOME}/runs/detect/train6/weights/best.pt data={dataset.location}/data.yaml

%cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train6/weights/best.pt conf=0.25 source={dataset.location}/test/images save=True

import glob
from IPython.display import Image, display

for image_path in glob.glob(f'{HOME}/runs/detect/predict2/*.jpg')[:2]:
      display(Image(filename=image_path, width=640))
      print("\n")



















