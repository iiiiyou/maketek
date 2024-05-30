from tkinter import *
import tkinter as tk 
from PIL import Image, ImageTk 

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

######  tkinter  start ######
# Google search: Tkinter geometry site:www.geeksforgeeks.org
# https://076923.github.io/posts/Python-tkinter-12/
# Create a Tkinter window
cam_on = False
root = tk.Tk()
root.title("Detection Display")

# creating fixed geometry of the 
# tkinter window with dimensions 150x200
root.geometry("1300x700+600+0")

# Create a label to display the video frames
label = tk.Label(root)
label.pack()
  
# Create a label and display it on app 
label_widget = Label(root) 
# label_widget.pack() 
label_widget.place(x=650, y=47)

# Create a label and display it on app 
label_widget2 = Label(root) 
# label_widget.pack() 
label_widget2.place(x=3, y=47)

######  tkinter  end   ######

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

# Create a list to count fire occurances

# Make folders if not exsist
def makedirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")

# Load the YOLOv8 model
model = YOLO('C:/workspace/maketek/models/20240530_best.pt')  # pretrained YOLOv8n model
 
detector = Detector()

#count
def count_fire(detected_a):
    if cam_on:

        if detector.counts[0] > 2 or detector.counts[1] > 2 or detector.counts[2] > 2 or detector.counts[3] > 2:
        
            # Make folders if not exsist
            path='C:/Users/user/Desktop/detected_image/'+date.format_date()+'/'
            makedirs(path)
            path='C:/Users/user/Desktop/detected_image/'+date.format_date()+'/Original/'
            makedirs(path)
            path='C:/Users/user/Desktop/detected_image/'+date.format_date()+'/box/'
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
                    
                    # cv2.imshow("YOLOv8 Inference2", imS2)

                    ######  tkinter  start ######
                    # Capture the latest frame and transform to image 
                    image2 = Image.fromarray(imS2) 
                
                    # Convert captured image to photoimage 
                    photo2 = ImageTk.PhotoImage(image=image2) 
                
                    # Displaying photoimage in the label 
                    label_widget2.photo_image = photo2 
                
                    # Configure image in the label 
                    label_widget2.configure(image=photo2) 
                
                    ######  tkinter  end   ######

                    # Saving images
                    cv2.imwrite('C:/Users/user/Desktop/detected_image/'+date.format_date()+'/box/'+date.get_time_in_mmddss()+'.jpg', annotated_frame2)
                    cv2.imwrite('C:/Users/user/Desktop/detected_image/'+date.format_date()+'/Original/'+date.get_time_in_mmddss()+'_Original.jpg', img_copy2)

                    modbus.write_detected(start2, client)

                    modbus.write_detected([0,0,0], client)

            detector.detected_defects=['x','x','x','x','x','x','x','x','x','x']

            
            # Break the loop if the end of the video is reached
            modbus.write_detected([0,0,0], client)

def open_camera(): 
    if cam_on:
        
    ######  tkinter  start ######
        ia.start()
        # i = 0
        modbus.write_detected([0,0,0], client)
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
            
            # cv2.imshow("YOLOv8 Inference", imS)
            fps = ia.statistics.fps

            ######  tkinter  start ######
            # Capture the latest frame and transform to image 
            image = Image.fromarray(imS) 
        
            # Convert captured image to photoimage 
            photo = ImageTk.PhotoImage(image=image) 
        
            # Displaying photoimage in the label 
            label_widget.photo_image = photo 
        
            # Configure image in the label 
            label_widget.configure(image=photo) 
            ######  tkinter  end   ######

            #########################  
            # Make folders if not exsist
            # path='detect_image/'+date.format_date()+'/'
            # makedirs(path)

            # Saving images
            # cv2.imwrite('detect_image/'+date.format_date()+'/'+date.get_time_in_mmddss()+'.jpg', annotated_frame)
            count_fire(detector.detected_defects)


            ######  tkinter  start ######
            # Repeat the same process after every 10 milliseconds 
            label_widget.after(10, open_camera) 
            ######  tkinter  end   ######

def start_cam():
    global cam_on
    # stop_cam()
    cam_on = True
    open_camera()

def stop_cam():
    global cam_on
    modbus.write_detected([1,0,0], client)
    print("Sent modbus [1,0,0]")
    cam_on = False


######  tkinter  start   ######

# Create a button to open the camera in GUI app 
btn_open = Button(root, text="Start Camera", command=start_cam) 
# btn_open.grid(row=0,column=0) 
# btn_open.pack()
btn_open.place(x=2, y=2)

# Create a button to close the camera in GUI app 
btn_stop = Button(root, text="Stop Camera", command=stop_cam) 
# btn_open.grid(row=0,column=0) 
# btn_close.pack()
btn_stop.place(x=92, y=2)

# Create a button to close the camera in GUI app 
btn_close = Button(root, text="Close Program", command=root.destroy) 
# btn_open.grid(row=0,column=0) 
# btn_close.pack()
btn_close.place(x=182, y=2)

# Auto start
start_cam()
# Create an infinite loop for displaying app on screen 
root.mainloop() 

# Release resources
try: 
    # cap.release()
    # cv2.destroyAllWindows()
    print("Camera is released")
except Exception as e:
    print(f"Error opening webcam: {e}")
    modbus.write_detected([1,0,0], client)
    print("Sent modbus [1,0,0]")
    modbus.write_detected([2,0,0], client)
    print("Sent modbus [2,0,0]")
    traceback.print_exc(file=sys.stdout)
finally:
    ia.stop()
    ia.destroy()
    cv2.destroyAllWindows()
    modbus.write_detected([1,0,0], client)
    print("Sent modbus [1,0,0]")
    h.reset()
    client.close()
    print('fin')
######  tkinter  start   ######