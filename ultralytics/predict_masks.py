from ultralytics import YOLO

# Load a model
# model = YOLO('C:\\workspace\\maketek\\runs\\detect\\train3\\weights\\best.pt')  # pretrained YOLOv8n model
# model = YOLO('model\\two_class_full_best_seg_4.pt')  # pretrained YOLOv8n model
model = YOLO('models\\1664_two_class_annotation-2-1_19.pt')  # pretrained YOLOv8n model

images = ['images\\test\\1664_102709.jpg', \
                 'images\\test\\1664_102854.jpg', \
                 'images\\test\\1664_105155.jpg', \
                 'images\\test\\1664_105312.jpg', \
                 'images\\test\\1664_120623.jpg', \
                 'images\\test\\1664_121007.jpg', \
                 'images\\test\\1664_130503.jpg', \
                 'images\\test\\1664_130704.jpg', \
                 'images\\test\\1664_133044.jpg', \
                 'images\\test\\1664_141728.jpg', \
                 'images\\test\\1664_141833.jpg', \
                 'images\\test\\1664_142059.jpg', \
                 'images\\test\\1664_142150.jpg', \
                 'images\\test\\1664_142701.jpg', \
                 'images\\test\\1664_142915.jpg', \
                 'images\\test\\1664_143019.jpg']

# Run batched inference on a list of images
results = model(images, stream=True)  # return a generator of Results objects

# Run inference on 'bus.jpg' with arguments
results = model.predict(images, save=True, imgsz=1664, conf=0.50)

# Process results generator
if __name__ == '__main__':
    # View results
    for r in results:
        print(r.masks)  # print the Masks object containing the detected instance masks