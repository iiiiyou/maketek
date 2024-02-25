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
h.add_file('C:\\Program Files\\Common Files\\OMRON_SENTECH\\GenTL\\v1_5\\StGenTL_MD_VC141_v1_5_x64.cti')
h.files
h.update()
h.device_info_list
print(h.device_info_list)

# ia = h.create(0)
ia = h.create({'serial_number': '23G7076'}) # - 1080 camera left
# ia = h.create({'serial_number': '23G7069'}) # - 1024 camera right
# ia = h.create({'serial_number': '22FK019'}) # - 1664 camera left



######  tkinter  start ######
# Google search: Tkinter geometry site:www.geeksforgeeks.org
# https://076923.github.io/posts/Python-tkinter-12/
# Create a Tkinter window
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
label_widget.place(x=650, y=25)
######  tkinter  end   ######

# Make folders if not exsist
def makedirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")


# Load the YOLOv8 model
model = YOLO('C:/workspace/maketek/models/1664_four_class_annotation_20240202.pt')  # pretrained YOLOv8n model


######  tkinter  start ######
# Create a function to open camera and 
# display it in the label_widget on app 
######  tkinter  end   ######


def open_camera(): 
    
######  tkinter  start ######

    ia.start()
    with ia.fetch() as buffer:
        # Work with the Buffer object. It consists of everything you need.
        print(buffer)
        # The buffer will automatically be queued.
        img = buffer.payload.components[0].data
        img = img.reshape(buffer.payload.components[0].height, buffer.payload.components[0].width)
        img_copy = img.copy()
        img_copy = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)

        results = model.predict(img_copy, save=False, imgsz=320, conf=0.2)
        result = results[0]

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        
        imS = cv2.resize(annotated_frame, (640, 640)) 
        # cv2.imshow("YOLOv8 Inference", imS)
        fps = ia.statistics.fps
        print("FPS: ", fps)


        ######  tkinter  start ######
        # Capture the latest frame and transform to image 
        image = Image.fromarray(imS) 
    
        # Convert captured image to photoimage 
        photo = ImageTk.PhotoImage(image=image) 
    
        # Displaying photoimage in the label 
        label_widget.photo_image = photo 
    
        # Configure image in the label 
        label_widget.configure(image=photo) 
    
        # Repeat the same process after every 10 milliseconds 
        label_widget.after(10, open_camera) 
        ######  tkinter  end   ######


######  tkinter  start   ######

# Create a button to open the camera in GUI app 
btn_open = Button(root, text="Open Camera", command=open_camera) 
# btn_open.grid(row=0,column=0) 
# btn_open.pack()
btn_open.place(x=0, y=0)

# Create a button to close the camera in GUI app 
btn_close = Button(root, text="Close Camera", command=root.destroy) 
# btn_open.grid(row=0,column=0) 
# btn_close.pack()
btn_close.place(x=90, y=0)

# Create an infinite loop for displaying app on screen 
root.mainloop() 

# Release resources
try: 
    # cap.release()
    # cv2.destroyAllWindows()
    print("Camera is released")
except Exception as e:
    print(f"Error opening webcam: {e}")

######  tkinter  start   ######
