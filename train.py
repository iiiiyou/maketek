from ultralytics import YOLO
import os
import shutil

from roboflow import Roboflow

if not os.path.exists("datasets\\640_two_class_full_annotation-3"):
   
    rf = Roboflow(api_key="bxW7hooY5jiknZS3GIxI")
    project = rf.workspace("i4umaket").project("640_two_class_full_annotation")
    dataset = project.version(3).download("yolov8")

    shutil.move("640_two_class_full_annotation-3", "datasets/")

# 모델을 로드하세요.
model = YOLO('yolov8m-seg.yaml')  # YAML에서 새 모델 구축
model = YOLO('yolov8m-seg.pt')  # 사전 훈련된 모델 로드 (훈련을 위해 권장됨)
# model = YOLO('yolov8m.yaml').load('yolov8n.pt')  # YAML에서 구축 및 가중치 전달


# 모델을 훈련합니다.

if __name__ == '__main__':
    print("training start")
    # data.yaml안에 있는 경로 기본 설정 "C:\Users\<user>\AppData\Roaming\Ultralytics\settings.yaml"
    # datasets_dir: C:\workspace\maketek "in settings.yaml"
    results = model.train(data='datasets\\640_two_class_full_annotation-3\\data.yaml', epochs=5, imgsz=640)

    # data.yaml 안의 image파일 경로
    # test: test/images
    # train: train/images
    # val: valid/images