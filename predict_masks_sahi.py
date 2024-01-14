from ultralytics import YOLO

from sahi.utils.yolov8 import download_yolov8s_model
from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from pathlib import Path
from IPython.display import Image

yolov8_model_path = "models\\2048_two_class_full_annotation-5_seg_9.pt"

# detection_model = AutoDetectionModel.from_pretrained(
#     model_type='yolov8',
#     model_path=yolov8_model_path,
#     confidence_threshold=0.3,
#     device="cuda:0",  # or 'cpu'
# )


predict(
    model_type="yolov8",
    model_path=yolov8_model_path,
    model_device="cuda:0",  # or 'cpu'
    model_confidence_threshold=0.6,
    source="images\\2048",
    slice_height=1024,
    slice_width=1024,
    overlap_height_ratio=0.2,
    overlap_width_ratio=0.2,
)
