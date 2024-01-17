from ultralytics import YOLO
import cv2

# Load a model
# model = YOLO('C:\\workspace\\maketek\\runs\\detect\\train3\\weights\\best.pt')  # pretrained YOLOv8n model
# model = YOLO('model\\two_class_full_best_seg_4.pt')  # pretrained YOLOv8n model
model = YOLO('model\\best.pt')  # pretrained YOLOv8n model

classes = [0, 1, 2, 3]
thresholds = [0.3, 0.9, 0.9, 0.9]

images = ['images\\20240114 방문\\실제환경반영\\흑점\\원본\\1024_091313.jpg']

# Run batched inference on a list of images
results = model(images, stream=False)  # return a generator of Results objects

# Run inference on 'bus.jpg' with arguments
results = model.predict(images, save=True, imgsz=1080, conf=0.3, classes=[0])
result = results[0]
    

# View results
for r in results:
    print(r.boxes.cls)  # print the Boxes object containing the detection bounding boxes
    print(r.boxes.conf)  # print the Boxes object containing the detection bounding boxes

filtered_predictions=[]

if(len(result.boxes)!=0):
    for box in results:
        i=0
        i = i + 1
        if box.boxes.cls[i] in classes and box.boxes.conf[i] >= thresholds[int(box.boxes.cls[i])]:
            annotated_frame = result[i].plot()
            cv2.imwrite('images\\20240114 방문\\실제환경반영\\흑점\\불량포함\\1024_091313_tst.jpg', annotated_frame)



# # Process results generator
# if __name__ == '__main__':
#     # View results
#     for r in results:
#         # print(r.boxes)  # print the Boxes object containing the detection bounding boxes