
# Installation
# To get started, install the latest versions of SAHI and Ultralytics:


# pip install -U ultralytics sahi

# Import Modules and Download Resources
# Here's how to import the necessary modules and download a YOLOv8 model and some test images:

from sahi.utils.yolov8 import download_yolov8s_model
from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from pathlib import Path
from IPython.display import Image

# Download YOLOv8 model
yolov8_model_path = "models/yolov8s.pt"
download_yolov8s_model(yolov8_model_path)

# Download test images
download_from_url('https://raw.githubusercontent.com/obss/sahi/main/demo/demo_data/small-vehicles1.jpeg', 'demo_data/small-vehicles1.jpeg')
download_from_url('https://raw.githubusercontent.com/obss/sahi/main/demo/demo_data/terrain2.png', 'demo_data/terrain2.png')

# Standard Inference with YOLOv8
# Instantiate the Model
# You can instantiate a YOLOv8 model for object detection like this:
    
detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov8',
    model_path=yolov8_model_path,
    confidence_threshold=0.3,
    device="cpu",  # or 'cuda:0'
)

# Perform Standard Prediction
# Perform standard inference using an image path or a numpy image.
# With an image path
result = get_prediction("demo_data/small-vehicles1.jpeg", detection_model)

# With a numpy image
result = get_prediction(read_image("demo_data/small-vehicles1.jpeg"), detection_model)

result.export_visuals(export_dir="demo_data/")
Image("demo_data/prediction_visual.png")

# Visualize Results
# Export and visualize the predicted bounding boxes and masks:

result = get_sliced_prediction(
    "demo_data/small-vehicles1.jpeg",
    detection_model,
    slice_height=256,
    slice_width=256,
    overlap_height_ratio=0.2,
    overlap_width_ratio=0.2
)


# Handling Prediction Results
# SAHI provides a PredictionResult object, which can be converted into various annotation formats:


# Access the object prediction list
object_prediction_list = result.object_prediction_list

# Convert to COCO annotation, COCO prediction, imantics, and fiftyone formats
result.to_coco_annotations()[:3]
result.to_coco_predictions(image_id=1)[:3]
result.to_imantics_annotations()[:3]
result.to_fiftyone_detections()[:3]

# Batch Prediction
# For batch prediction on a directory of images:


predict(
    model_type="yolov8",
    model_path="path/to/yolov8n.pt",
    model_device="cpu",  # or 'cuda:0'
    model_confidence_threshold=0.4,
    source="path/to/dir",
    slice_height=256,
    slice_width=256,
    overlap_height_ratio=0.2,
    overlap_width_ratio=0.2,
)