import cv2
from ultralytics import YOLO
import format_date_time as date
import LS_Modbus as modbus
import os


# Make folders if not exsist
def makedirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")


# Load the YOLOv8 model
model = YOLO('model\\two_class_full_best_seg_4.pt')  # pretrained YOLOv8n model
        

# Open the video file
cap = cv2.VideoCapture(0)

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

        print(result)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        imS = cv2.resize(annotated_frame, (960, 960)) 
        cv2.imshow("YOLOv8 Inference", imS)
        # cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Make folders if not exsist
        path='detect_image\\'+date.format_date()+'\\'
        makedirs(path)

        # Saving images
        # cv2.imwrite('detect_images\\'+date.format_date()+'\\'+date.get_time_in_mmddss()+'.jpg', annotated_frame)

        # Modbus write
        if(len(result.boxes)!=0):
            cords = result.boxes.xyxy[0].tolist()
            cords = [round(x) for x in cords]
            start = cords[0:2]  # x1,y1

            start.insert(0,1)

            print("-----------------------")
            print(start)
            
            # Saving images
            cv2.imwrite('detect_image\\'+date.format_date()+'\\'+date.get_time_in_mmddss()+'.jpg', imS)

            modbus.write_detected(start)
        else:
            # Break the loop if the end of the video is reached
            print('no detacted')
            modbus.write_detected([0,0,0])

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):            
            print("inputted Q!!!!!")
            modbus.write_detected([0,0,0])
            print("endded Q!!!!!")
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()