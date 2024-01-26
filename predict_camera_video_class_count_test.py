import cv2
from ultralytics import YOLO
import format_date_time as date
import LS_Modbus as modbus
import os


# Define the four classes you want to detect (replace with your actual classes)
class_ids = ['a', 'b', 'c', 'd'] 

class Detector:
    def __init__(self):
        self.detected_defects = []
        self.counts = ()

    def append_defect(self, detected_defect):
        self.detected_defects.append(detected_defect)

        # Main tain the lengh shorter than 10
        if len(self.detected_defects) > 10:
            self.detected_defects.pop(0)  # Remove the first element
        
        a = self.detected_defects.count('a')
        b = self.detected_defects.count('b')
        c = self.detected_defects.count('c')
        d = self.detected_defects.count('d')

        self.counts = (a,b,c,d)

        return self.counts


detector = Detector()

# Make folders if not exsist
def makedirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")


# #count
# def count_fire(detected_list,result):

#     if len(detected_list) > 10:
#         detected_list.pop(0)  # Remove the first element
        

#         if detected_list.count(1) > 3:

#             if(len(result.boxes)!=0):
#                 cords = result.boxes.xyxy[0].tolist()
#                 cords = [round(x) for x in cords]
#                 start = cords[0:2]  # x1,y1

#                 start.insert(0,1)

#                 print("-----------------------")
#                 print(start)
                
#                 # Saving images
#                 # cv2.imwrite('C:/Workplace/i4u/maketek/detect_image/'+date.format_date()+'/'+date.get_time_in_mmddss()+'.jpg', imS)

#                 modbus.write_detected(start)
#             else:
#                 # Break the loop if the end of the video is reached
#                 return 0




# Load the YOLOv8 model
# model = YOLO('model\\two_class_full_best_seg_4.pt')  # pretrained YOLOv8n model
model = YOLO('model/1664_4class_merge-1-2.pt')  # pretrained YOLOv8n model
# model = YOLO('C:/Workplace/i4u/maketek/yolov8n.pt')  # pretrained YOLOv8n model   
cap = cv2.VideoCapture(1)


# Create a list to count fire occurances
detected_list = []

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        # results = model(frame)
        # Run inference on 'bus.jpg' with arguments
        results = model.predict(frame, save=False, imgsz=1080, conf=0.75)
        result = results[0]

        # print(result)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        imS = cv2.resize(annotated_frame, (960, 960)) 
        cv2.imshow("YOLOv8 Inference", imS)
        # cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Make folders if not exsist
        # path='C:/Workplace/i4u/maketek/detect_image/'+date.format_date()+'/'
        # makedirs(path)

        # Saving images
        # cv2.imwrite('detect_images\\'+date.format_date()+'\\'+date.get_time_in_mmddss()+'.jpg', annotated_frame)



        # print("result.boxes: ", result.boxes)

        


        for box in result.boxes:
            class_id = result.names[box.cls[0].item()]
            cords = result.boxes.xyxy[0].tolist()
            cords = [round(x) for x in cords]
            start = cords[0:2]  # x1,y1

            start.insert(0,1)

            if class_id in class_id:
                detector.append_defect(class_id)

            if detector.counts[0] > 3:
                message = f'type {class_id} is detected more than 3 times, take some actions'
                modbus.write_detected(start)

            if detector.counts[1] > 3:
                message = f'type {class_id} is detected more than 5 times, take some actions'
                modbus.write_detected(start)

            if detector.counts[2] > 3:
                message = f'type {class_id} is detected more than 3 times, take some actions'
                modbus.write_detected(start)

            if detector.counts[3] > 3:
                message = f'type {class_id} is detected more than 5 times, take some actions'
                modbus.write_detected(start)


            image = cv2.putText(imS, str(detector.detected_defects) , (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)

            cv2.imshow("YOLOv8 Inference2", imS)


        # print("detect_list: ", detected_list)
        # count_fire(detected_list,result)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()