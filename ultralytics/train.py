from ultralytics import YOLO

# 모델을 로드하세요.
model = YOLO('yolov8m-seg.yaml')  # YAML에서 새 모델 구축
model = YOLO('yolov8m-seg.pt')  # 사전 훈련된 모델 로드 (훈련을 위해 권장됨)
# model = YOLO('yolov8m.yaml').load('yolov8n.pt')  # YAML에서 구축 및 가중치 전달

# from roboflow import Roboflow
# rf = Roboflow(api_key="bxW7hooY5jiknZS3GIxI")
# project = rf.workspace("i4umaket").project("640_two_class_full_annotation")
# dataset = project.version(3).download("yolov8")


# 모델을 훈련합니다.
if __name__ == '__main__':
    results = model.train(data='C:\\workspace\\maketek\\ultralytics\\640_two_class_full_annotation-3\\data.yaml', epochs=200, imgsz=640)

