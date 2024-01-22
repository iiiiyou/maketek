import cv2
from ultralytics import YOLO
import sys
sys.path.append('')

from harvesters.core import Harvester
import sys
import traceback
import time
import sys
import numpy
import format_date_time as date
import LS_Modbus as modbus
import os
# numpy.set_printoptions(threshold=sys.maxsize)

h = Harvester()
h.add_file('C:\\Program Files\\Common Files\\OMRON_SENTECH\\GenTL\\v1_5\\StGenTL_MD_VC141_v1_5_x64.cti')
h.files
h.update()
h.device_info_list
print(h.device_info_list)

# ia = h.create(0)
# ia = h.create({'serial_number': '23G7076'}) # - 1080 camera left
# ia = h.create({'serial_number': '23G7069'}) # - 1080 camera right
ia = h.create({'serial_number': '22FK019'}) # - 2048 camera left

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


#count
def count_fire(detected_a):

    if len(detected_a) > 7:
        detected_a.pop(0)  # Remove the first element
    
        if detected_a.count(1) > 3:

            
            #########################  
            # Make folders if not exsist
            path='detect_image\\'+date.format_date()+'\\'
            makedirs(path)

            modbus.write_detected([1,0,0]) #send modbus [1,0,0] mean is stop vibration
            # time.sleep(10)\q
            for i in range(5):
                with ia.fetch() as buffer2:
                    # Work with the Buffer object. It consists of everything you need.
                    print(buffer2)
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
                    cv2.imshow("YOLOv8 Inference2", imS2)
                
            # Modbus write
            if(len(result2.boxes)!=0):
                cords2 = result2.boxes.xyxy[0].tolist()
                cords2 = [round(x) for x in cords2]
                start2 = cords2[0:2]  # x1,y1

                start2.insert(0,1)
                
                # Saving images
                cv2.imwrite('detect_image\\'+date.format_date()+'\\'+date.get_time_in_mmddss()+'.jpg', imS)

                modbus.write_detected(start2)

                global detected_list

                detected_list=[0,0,0,0,0,0,0]
                print(detected_list)
                print("--")

            else:
                # Break the loop if the end of the video is reached
                print('no detacted')
                modbus.write_detected([0,0,0])
                return 0




# Load the YOLOv8 model
# model = YOLO('models\\1664_four_class_annotation-2-1_19-seg.pt')  # pretrained YOLOv8n model
model = YOLO('models\\1664_4class_merge-1-2.pt')  # pretrained YOLOv8n model
# model = YOLO('models\\1664_two_class_annotation-1_seg-1.pt')  # pretrained YOLOv8n model
        

try:
    ia.start()
    # i = 0
    done = False
    while not done:
        with ia.fetch() as buffer:
            # Work with the Buffer object. It consists of everything you need.
            print(buffer)
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
            cv2.imshow("YOLOv8 Inference", imS)
            fps = ia.statistics.fps
            print("FPS: ", fps)

            #########################  
            # Make folders if not exsist
            # path='detect_image\\'+date.format_date()+'\\'
            # makedirs(path)

            # Saving images
            # cv2.imwrite('detect_image\\'+date.format_date()+'\\'+date.get_time_in_mmddss()+'.jpg', annotated_frame)

            

            # Break the loop if 'q' is pressed
            #########################  

            # Modbus write
            if(len(result.boxes)!=0):
                detected_list.append(1)  # Add the last element
            else:
                # Break the loop if the end of the video is reached
                detected_list.append(0)
                modbus.write_detected([0,0,0])
                print('no detacted')

            print("detect_list: ", detected_list)
            count_fire(detected_list)
          
            if cv2.waitKey(10) == ord('q'):
                done = True
                modbus.write_detected([0,0,0])
                print('break')
            # i = i + 1
except Exception as e:
    traceback.print_exc(file=sys.stdout)
finally:
    ia.stop()
    ia.destroy()
    cv2.destroyAllWindows()
    print('fin')
    h.reset()