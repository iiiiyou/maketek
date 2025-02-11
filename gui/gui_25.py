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
confidence = 0.6
reset_confidence = 0.6

# ia = h.create(0)
# ia = h.create({'serial_number': '23G7076'}) # - 1080 camera left
# ia = h.create({'serial_number': '23G7069'}) # - 1080 camera right
ia = h.create({'serial_number': '22FK019'}) # - 2048 camera left

######  tkinter  start ######
# Google search: Tkinter geometry site:www.geeksforgeeks.org
# https://076923.github.io/posts/Python-tkinter-12/
# Create a Tkinter window
cam_on = False
win = Tk()
win.title("Detection Display")

# creating fixed geometry of the 
# tkinter window with dimensions 150x200
win.geometry("1300x800+600+0")

# Create a label to display the video frames
# label = tk.Label(root)
# label.pack()
  
# Create a label and display it on app 
label_camera1 = Label(win) 
# label_widget.pack() 
label_camera1.place(x=650, y=100)

# Create a label and display it on app 
label_camera2 = Label(win) 
# label_widget.pack() 
label_camera2.place(x=3, y=100)

# Confidence 라벨
label_confidence1 = Label(win)
label_confidence1.config(text = "Confidence: ")
label_confidence1.place(x=20, y=40)
# label_cable2.pack()

# Confidence 값
value_confidence1 = Label(win)
value_confidence1.config(text = "준비 중")
value_confidence1.place(x=120, y=40)
def show_confidence1_value(current_confidence):
    value_confidence1.config(text = current_confidence)
# value_cable2.pack()

# function to display user text when 
# button is clicked
def confidence_change():
    global confidence
    new_confidence = float(entry_confidence2.get())
    confidence = new_confidence
    show_confidence1_value(confidence)

def confidence_init():
    global reset_confidence
    entry_confidence2.delete(0, END)
    entry_confidence2.insert(0, reset_confidence) # 0.5를 기본값으로 설정  
    label_confidence2.place(x=450, y=2)

# "Confidence 변경" 라벨
label_confidence2 = Label(win)
label_confidence2.config(text = "Confidence 변경: ")
label_confidence2.place(x=20, y=60)

# "Confidence 변경" 입력 필드
entry_confidence2 = Entry(win, width = 10)
entry_confidence2.insert(0, confidence) # 0.5를 기본값으로 설정
entry_confidence2.place(x=120, y=60)
    
# "Confidence 변경"을 위한 버튼
btn_confidence2 = Button(win, text="Change", command=confidence_change) 
btn_confidence2.place(x=200, y=60)

######  tkinter  end   ######

client = ModbusTcpClient("192.168.200.2", port=502)

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

detected = []

# 이전과 현재가 바뀌었나 확인
def is_detected(x):
    if (x in detected):
        file_path = "C:/source/log/"+str(date.get_date_in_yyyymmdd())+"_detected.txt"
        # duplicated = str(date.get_date_time()) + ": " + str(x) + ", "
        duplicated = str(x) + ", "
        # with open(file_path, "a") as file:
        #     # file.write(duplicated + "\n")
        #     file.write(duplicated)
        return False
    else:
        if len(detected) >= 30:
            detected.pop(0)
        detected.append(x)
        return True

# Load the YOLOv8 model
# model = YOLO('C:/workspace/maketek/models/20240725_best.pt')  # pretrained YOLOv8n model
model = YOLO('C:/workspace/maketek/models/maketech-7-1_3rd_20250131_yolov8m-seg_best.pt')  # pretrained YOLOv8n model
 
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


                    results2 = model.predict(img_copy2, save=False, imgsz=1664, conf=confidence)
                    result2 = results2[0]

                    # Visualize the results on the frame
                    annotated_frame2 = results2[0].plot()
                                    
                    # img_copy = img.copy()
                    # img_copy = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)
                    # cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
                    imS2 = cv2.resize(annotated_frame2, (640, 640)) 

                xy = []

            # Modbus write
                if(i > 5 and len(result2.boxes)!=0):
                    # cords2 = result2.boxes.xyxy[0].tolist()
                    # cords2 = [round(x) for x in cords2]

                    for box in result2.boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        xy.append([1,int(x1),int(y1)])
                        print(xy)

                    # start2 = cords2[0:2]  # x1,y1

                    # start2.insert(0,1)
                    
                    # cv2.imshow("YOLOv8 Inference2", imS2)

                    ######  tkinter  start ######
                    # Capture the latest frame and transform to image 
                    image2 = Image.fromarray(imS2) 
                
                    # Convert captured image to photoimage 
                    photo2 = ImageTk.PhotoImage(image=image2) 
                
                    # Displaying photoimage in the label 
                    label_camera2.photo_image = photo2 
                
                    # Configure image in the label 
                    label_camera2.configure(image=photo2) 
                
                    ######  tkinter  end   ######

                    # Saving images
                    cv2.imwrite('C:/Users/user/Desktop/detected_image/'+date.format_date()+'/box/'+date.get_time_in_mmddss()+'.jpg', annotated_frame2)
                    cv2.imwrite('C:/Users/user/Desktop/detected_image/'+date.format_date()+'/Original/'+date.get_time_in_mmddss()+'_Original.jpg', img_copy2)

                    modbus.write_detected(xy, client)

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

            results = model.predict(img_copy, save=False, imgsz=1664, conf=confidence)
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

            # 테두리 색 (파란색)
            color_border = (0, 36, 255)
            # 글자 색 (흰색)
            color_text = (255, 255, 255)

            # 테두리 그리기
            cv2.putText(imS, str(detector.detected_defects), (10, 620), cv2.FONT_HERSHEY_SIMPLEX, \
                            0.5, color_border, 3, cv2.LINE_AA)

            # 글자 그리기
            cv2.putText(imS, str(detector.detected_defects), (10, 620), cv2.FONT_HERSHEY_SIMPLEX, \
                            0.5, color_text, 1, cv2.LINE_AA)
            
            # cv2.imshow("YOLOv8 Inference", imS)
            fps = ia.statistics.fps

            ######  tkinter  start ######
            # Capture the latest frame and transform to image 
            image = Image.fromarray(imS) 
        
            # Convert captured image to photoimage 
            photo = ImageTk.PhotoImage(image=image) 
        
            # Displaying photoimage in the label 
            label_camera1.photo_image = photo 
        
            # Configure image in the label 
            label_camera1.configure(image=photo) 
            ######  tkinter  end   ######

            #########################  
            # Make folders if not exsist
            # path='detect_image/'+date.format_date()+'/'
            # makedirs(path)

            # Saving images
            # cv2.imwrite('detect_image/'+date.format_date()+'/'+date.get_time_in_mmddss()+'.jpg', annotated_frame)
            # count_fire(detector.detected_defects)

            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                if is_detected((x1, y1))== True:
                    count_fire(detector.detected_defects)
                else:
                    print("duplicated")


            ######  tkinter  start ######
            # Repeat the same process after every 10 milliseconds 
            label_camera1.after(10, open_camera) 
            ######  tkinter  end   ######

show_confidence1_value(confidence)

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
btn_open = Button(win, text="일시정지 해제", command=start_cam) 
# btn_open.grid(row=0,column=0) 
# btn_open.pack()
btn_open.place(x=2, y=2)

# Create a button to close the camera in GUI app 
btn_stop = Button(win, text="   일시정지   ", command=stop_cam) 
# btn_open.grid(row=0,column=0) 
# btn_close.pack()
btn_stop.place(x=92, y=2)

# Create a button to close the camera in GUI app 
btn_close = Button(win, text="프로그램 종료", command=win.destroy) 
# btn_open.grid(row=0,column=0) 
# btn_close.pack()
btn_close.place(x=182, y=2)

# Auto start
start_cam()
# Create an infinite loop for displaying app on screen 
win.mainloop() 

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