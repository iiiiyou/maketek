from ultralytics import YOLO

# Load a model
# model = YOLO('C:\\workspace\\maketek\\runs\\detect\\train3\\weights\\best.pt')  # pretrained YOLOv8n model
# model = YOLO('model\\two_class_full_best_seg_4.pt')  # pretrained YOLOv8n model
model = YOLO('model\\2048_two_class_full_annotation-5_seg_9.pt')  # pretrained YOLOv8n model

images = ['images\\2048\\2048_good_and_defective_01.jpg', \
                 'images\\2048\\2048_good_and_defective_02.jpg']

# Run batched inference on a list of images
results = model(images, stream=True)  # return a generator of Results objects

# Run inference on 'bus.jpg' with arguments
results = model.predict(images, save=True, imgsz=2048, conf=0.50)

# Process results generator
if __name__ == '__main__':
    # View results
    for r in results:
        print(r.masks)  # print the Masks object containing the detected instance masks