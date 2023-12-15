import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
# model = YOLO('C:\\workspace\\maketek\\runs\\detect\\train3\\weights\\best.pt')  # pretrained YOLOv8n model
model = YOLO('model\\best.pt')  # pretrained YOLOv8n model

# Open the video file
# video_path = "C:\\workspace\\maketek\\deform_spot__output_02.mp4"
video_path = "mp4\\raw_output_03.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        # results = model(frame)
        # Run inference on 'bus.jpg' with arguments
        results = model.predict(frame, save=False, imgsz=1080, conf=0.85)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()