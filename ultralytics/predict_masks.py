from ultralytics import YOLO

# Load a model
# model = YOLO('C:\\workspace\\maketek\\runs\\detect\\train3\\weights\\best.pt')  # pretrained YOLOv8n model
# model = YOLO('model\\two_class_full_best_seg_4.pt')  # pretrained YOLOv8n model
model = YOLO('model\\1664_4class_merge-1-1.pt')  # pretrained YOLOv8n model

images = ['images\\20240118\\1664_145957.jpg', \
                 'images\\20240118\\1664_155706_15.jpg', \
                 'images\\20240118\\1664_161826.jpg', \
                 'images\\20240118\\1664_163932.jpg']

# Run batched inference on a list of images
results = model(images, stream=True)  # return a generator of Results objects

# Run inference on 'bus.jpg' with arguments
results = model.predict(images, save=True, imgsz=1664, conf=0.50)

# Process results generator
if __name__ == '__main__':
    # View results
    for r in results:
        print(r.masks)  # print the Masks object containing the detected instance masks