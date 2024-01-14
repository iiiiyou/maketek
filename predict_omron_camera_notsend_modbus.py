import cv2
from ultralytics import YOLO
import format_date_time as date
import LS_Modbus as modbus
import os

from harvesters.core import Harvester
import sys
import traceback


h = Harvester()
h.add_file('C:\\Program Files\\Common Files\\OMRON_SENTECH\\GenTL\\v1_5\\StGenTL_MD_VC141_v1_5_x64.cti')
h.files
h.update()
h.device_info_list
print(h.device_info_list)

# ia = h.create(0)
# ia = h.create({'serial_number': '23G7076'}) # - 1080 camera left
# ia = h.create({'serial_number': '23G7069'}) # - 1024 camera right
ia = h.create({'serial_number': '22FK019'}) # - 1664 camera left

# Make folders if not exsist
def makedirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")


# Load the YOLOv8 model
# model = YOLO('models\\1664_two_class_annotation-1_seg-1.pt')  # pretrained YOLOv8n model
model = YOLO('models\\1664_four_class_annotation-2-1_19-seg.pt')  # pretrained YOLOv8n model
        

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

            results = model.predict(img_copy, save=False, imgsz=1664, conf=0.50)
            result = results[0]

            # Visualize the results on the frame
            annotated_frame = results[0].plot()
                            
            # img_copy = img.copy()
            # img_copy = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)
            # cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
            imS = cv2.resize(annotated_frame, (960, 960)) 
            cv2.imshow("YOLOv8 Inference", imS)
            fps = ia.statistics.fps
            print("FPS: ", fps)

            #########################  
            # Make folders if not exsist
            # path='detect_image\\'+date.format_date()+'\\'
            # makedirs(path)

            # Saving images
            # cv2.imwrite('detect_image\\'+date.format_date()+'\\'+date.get_time_in_mmddss()+'.jpg', annotated_frame)

            # Modbus write
            if(len(result.boxes)!=0):
                cords = result.boxes.xyxy[0].tolist()
                cords = [round(x) for x in cords]
                start = cords[0:2]  # x1,y1

                start.insert(0,1)

                # print("-----------------------")
                # print(start)
                
                # Saving images
                # cv2.imwrite('detect_image\\'+date.format_date()+'\\'+date.get_time_in_mmddss()+'.jpg', imS)

                # modbus.write_detected(start)
            else:
                # Break the loop if the end of the video is reached
                print('no detacted')
                # modbus.write_detected([0,0,0])

            # Break the loop if 'q' is pressed
            #########################  
          
            if cv2.waitKey(10) == ord('q'):
                done = True
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