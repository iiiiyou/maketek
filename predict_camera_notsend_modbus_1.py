import cv2
from ultralytics import YOLO
import format_date_time as date
import LS_Modbus as modbus
import os


classes = [0, 1, 2, 3]
thresholds = [0.3, 0.1, 0.3, 0.3]

# Create a list to count fire occurances
global detected_list
detected_list=[]

# Make folders if not exsist
def makedirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")


def count_fire(detected_a):

    if len(detected_a) > 7:
        # Remove the first element
        detected_a.pop(0)
    
        if detected_a.count(1) > 3:
            return


# Load the YOLOv8 model
# model = YOLO('model\\two_class_full_best_seg_4.pt')  # pretrained YOLOv8n model
# model = YOLO('models\\1664_four_class_annotation-2-1_19-seg.pt')  # pretrained YOLOv8n model
model = YOLO('model\\best.pt')  # pretrained YOLOv8n model
        

# Open the video file
cap = cv2.VideoCapture(1)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        # results = model(frame)
        # Run inference on 'bus.jpg' with arguments
        results = model.predict(frame, save=False, imgsz=1024, conf=0.1)
        result = results[0]

        # print(result)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        imS = cv2.resize(annotated_frame, (960, 960)) 
        cv2.imshow("YOLOv8 Inference", imS)
        # cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Make folders if not exsist
        # path='detect_image\\'+date.format_date()+'\\'
        # makedirs(path)

        # Saving images
        # cv2.imwrite('detect_images\\'+date.format_date()+'\\'+date.get_time_in_mmddss()+'.jpg', annotated_frame)

        # Modbus write
        if(len(result.boxes)!=0):
            for box in results:
                i=0
                i = i + 1
                if box.boxes.cls[i] in classes and box.boxes.conf[i] >= thresholds[int(box.boxes.cls[i])]:
                    annotated_frame = result[i].plot()
                    # cv2.imwrite('images\\20240114 방문\\실제환경반영\\흑점\\불량포함\\1664_093430_tst.jpg', annotated_frame)
                    detected_list.append(1)
        else:
            # Break the loop if the end of the video is reached
            print('no detacted')
            detected_list.append(0)
            # modbus.write_detected([0,0,0])

        count_fire(detected_list)
        print(detected_list)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):            
            print("inputted Q!!!!!")
            # modbus.write_detected([0,0,0])
            print("endded Q!!!!!")
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()