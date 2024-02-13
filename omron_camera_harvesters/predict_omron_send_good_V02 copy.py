import cv2
from ultralytics import YOLO
import sys
sys.path.append('C:/workspace/maketek')

from harvesters.core import Harvester
import sys
import traceback
import time
import sys
import numpy
import format_date_time as date
import LS_Modbus_test as modbus
from pymodbus.client import ModbusTcpClient
import os


client = ModbusTcpClient("192.168.1.2", port=502)

# Define the four classes you want to detect (replace with your actual classes)
class_ids = ['a', 'b', 'c', 'd', 'x'] 

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
        x = self.detected_defects.count('x')

        self.counts = (a,b,c,d,x)

        return self.counts


detector = Detector()

h = Harvester()
h.add_file('C:/Program Files/Common Files/OMRON_SENTECH/GenTL/v1_5/StGenTL_MD_VC141_v1_5_x64.cti')
h.files
h.update()
h.device_info_list
print(h.device_info_list)

# ia = h.create(0)
# ia = h.create({'serial_number': '23G7076'}) # - 1080 camera left
# ia = h.create({'serial_number': '23G7069'}) # - 1080 camera right
ia = h.create({'serial_number': '22FK019'}) # - 2048 camera left

# Create a list to count fire occurances


# Make folders if not exsist
def makedirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")


detector = Detector()

#count
def count_fire(detected_a):

    if detector.counts[3] > 2:

        # Make folders if not exsist
        path='C:/workspace/maketek/detect_image/'+date.format_date()+'/'
        makedirs(path)

        #send modbus [1,0,0] mean is stop vibration
        modbus.write_detected([1,0,0], client)

        for i in range(9):
            with ia.fetch() as buffer2:
                # Work with the Buffer object. It consists of everything you need.
                # The buffer will automatically be queued.
                img2 = buffer2.payload.components[0].data
                img2 = img2.reshape(buffer2.payload.components[0].height, buffer2.payload.components[0].width)
                img_copy2 = img2.copy()
                img_copy2 = cv2.cvtColor(img2, cv2.COLOR_BayerRG2RGB)


                results2 = model.predict(img_copy2, save=False, imgsz=1664, conf=0.85)
                result2 = results2[0]

                # Visualize the results on the frame
                annotated_frame2 = results2[0].plot()
                                
                # img_copy = img.copy()
                # img_copy = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)
                # cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
                imS2 = cv2.resize(annotated_frame2, (640, 640)) 

            
        # Modbus write
            if(i > 5 and len(result2.boxes)!=0):
                cords2 = result2.boxes.xyxy[0].tolist()
                cords2 = [round(x) for x in cords2]
                start2 = cords2[0:2]  # x1,y1

                start2.insert(0,1)
                
                cv2.imshow("YOLOv8 Inference2", imS2)
                
                # Saving images
                cv2.imwrite('C:/workspace/maketek/detect_image/'+date.format_date()+'/'+date.get_time_in_mmddss()+'.jpg', imS)

                modbus.write_detected(start2, client)

                modbus.write_detected([0,0,0], client)

        detector.detected_defects=['x','x','x','x','x','x','x','x','x','x']

        
        # Break the loop if the end of the video is reached
        modbus.write_detected([0,0,0], client)





# Load the YOLOv8 model
# model = YOLO('models/1664_four_class_annotation-2-1_19-seg.pt')  # pretrained YOLOv8n model
# model = YOLO('C:/workspace/maketek/models/1664_four_class_annotation-2-1_19-seg.pt')  # pretrained YOLOv8n model
# model = YOLO('C:/workspace/maketek/models/1664_4class_merge-1-2.pt')  # pretrained YOLOv8n model
model = YOLO('C:/workspace/maketek/models/1664_four_class_annotation_20240202.pt')  # pretrained YOLOv8n model
        

try:
    ia.start()
    # i = 0
    modbus.write_detected([0,0,0], client)
    done = False
    while not done:
        with ia.fetch() as buffer:
            # Work with the Buffer object. It consists of everything you need.
            # The buffer will automatically be queued.
            img = buffer.payload.components[0].data
            img = img.reshape(buffer.payload.components[0].height, buffer.payload.components[0].width)
            img_copy = img.copy()
            img_copy = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)

            results = model.predict(img_copy, save=False, imgsz=1664, conf=0.85)
            result = results[0]

            # Visualize the results on the frame
            annotated_frame = results[0].plot()
                            
            # img_copy = img.copy()
            # img_copy = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)
            # cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
            imS = cv2.resize(annotated_frame, (640, 640))

            if(len(result.boxes)==0):
                # Break the loop if the end of the video is reached
                detector.append_defect('x')
            
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                if class_id in class_id:
                    detector.append_defect(class_id)

            cv2.putText(imS, str(detector.detected_defects), (10, 620), cv2.FONT_HERSHEY_SIMPLEX, \
                            0.5, (0, 36, 255), 1, cv2.LINE_AA)
            
            cv2.imshow("YOLOv8 Inference", imS)
            fps = ia.statistics.fps

            #########################  
            # Make folders if not exsist
            # path='detect_image/'+date.format_date()+'/'
            # makedirs(path)

            # Saving images
            # cv2.imwrite('detect_image/'+date.format_date()+'/'+date.get_time_in_mmddss()+'.jpg', annotated_frame)

            count_fire(detector.detected_defects)
                           
          
            if cv2.waitKey(10) == ord('q'):
                done = True
                modbus.write_detected([1,0,0], client)
                client.close()
except Exception as e:
    traceback.print_exc(file=sys.stdout)
finally:
    ia.stop()
    ia.destroy()
    cv2.destroyAllWindows()
    modbus.write_detected([1,0,0], client)
    print('fin')
    h.reset()
    client.close()