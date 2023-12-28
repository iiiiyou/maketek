from ultralytics import YOLO

# Load a model
# model = YOLO('C:\\workspace\\maketek\\runs\\detect\\train3\\weights\\best.pt')  # pretrained YOLOv8n model
# model = YOLO('model\\two_class_full_best_seg_4.pt')  # pretrained YOLOv8n model
model = YOLO('model\\two_class_full_best_detect_4.pt')  # pretrained YOLOv8n model

images = ['images\\deform_spot_142804.jpg', \
                 'images\\raw_151651.jpg']

# Run batched inference on a list of images
results = model(images, stream=False)  # return a generator of Results objects

# Run inference on 'bus.jpg' with arguments
results = model.predict(images, save=True, imgsz=1080, conf=0.9)

# Process results generator
if __name__ == '__main__':
    # View results
    for r in results:
        print(r.boxes)  # print the Boxes object containing the detection bounding boxes