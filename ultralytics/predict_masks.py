from ultralytics import YOLO

# Load a model
# model = YOLO('C:\\workspace\\maketek\\runs\\detect\\train3\\weights\\best.pt')  # pretrained YOLOv8n model
model = YOLO('C:\\workspace\\maketek\\runs\\segment\\train\\weights\\best.pt')  # pretrained YOLOv8n model

images = ['C:\\workspace\\maketek\\raw_151651.jpg', \
                 'C:\\workspace\\maketek\\deform_spot_142804.jpg']

# Run batched inference on a list of images
results = model(images, stream=True)  # return a generator of Results objects

# Run inference on 'bus.jpg' with arguments
results = model.predict(images, save=True, imgsz=1080, conf=0.5)

# Process results generator
if __name__ == '__main__':
    # View results
    for r in results:
        print(r.masks)  # print the Masks object containing the detected instance masks