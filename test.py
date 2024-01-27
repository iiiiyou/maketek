import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(0)
model = YOLO('C:/workspace/maketek/models/1664_4class_merge-1-2.pt')  # pretrained YOLOv8n model

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

''' 
# Create an object
detector = Detector()

# Detections occurs 
detector.append_defect('a')
detector.append_defect('b')
detector.append_defect('c')
detector.append_defect('d')


# Detections occurs. Class a (counts[0] shall have a higher priority) 
if detector.counts[0] > 3:
    print('type a is detected more than 3 times, take some actions')
else:
    print('do nothing yet')


if detector.counts[1] > 5:
    print('type b is detected more than 3 times, take some actions')
else:
    print('do nothing yet')

'''




while True:
    ret, frame = cap.read()
    result = model(frame)[0]
    
    detector = Detector()

    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        if class_id in class_id:
            detector.append_defect(class_id)

        if detector.counts[0] > 3:
            message = f'type {class_id} is detected more than 3 times, take some actions'
            print('a is more than 3')

        if detector.counts[1] > 5:
            message = f'type {class_id} is detected more than 5 times, take some actions'
            print('b is more than 3')

        image = cv2.putText(frame, str(detector.detected_defects) , (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)


        # Display the frame
        cv2.imshow('result image', image)
        # Press `q` to quit
        if cv2.waitKey(1) == ord("q"):
            cap.release()
            cv2.destroyAllWindows()

