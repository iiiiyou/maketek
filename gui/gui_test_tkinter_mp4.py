# Python program to open the 
# camera in Tkinter 
# Import the libraries, 
# tkinter, cv2, Image and ImageTk 
  
from tkinter import *
import tkinter as tk 
import cv2 
from PIL import Image, ImageTk 
import traceback
import sys


confidence = 0.8
reset_confidence = 0.8
# Define a video capture object 
# vid = cv2.VideoCapture(0) 
vid = cv2.VideoCapture("C:/workspace/maketek/mp4/output_02.mp4") 
  
# Declare the width and height in variables 
# width, height = 800, 600
  
######  tkinter  start ######
# Google search: Tkinter geometry site:www.geeksforgeeks.org
# https://076923.github.io/posts/Python-tkinter-12/
# Create a Tkinter window
cam_on = False
cam_count = 0
win = Tk()
win.title("Detection Display")

# creating fixed geometry of the 
# tkinter window with dimensions 150x200
win.geometry("1300x800+600+0")

# Create a label to display the video frames
# label = tk.Label(win)
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
  
#count
def count_fire(detected_a):
    if cam_on:
        global cam_count
        for i in range(1):
            # Capture the video frame by frame 
            _, frame = vid.read() 
        
            # Convert image from one color space to other 
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
            imS = cv2.resize(opencv_image, (640, 640))

            ######  tkinter  start ######
            # Capture the latest frame and transform to image 
            image2 = Image.fromarray(imS) 
        
            # Convert captured image to photoimage 
            photo2 = ImageTk.PhotoImage(image=image2) 
        
            # Displaying photoimage in the label 
            label_camera2.photo_image = photo2 
        
            # Configure image in the label 
            label_camera2.configure(image=photo2) 
        
            ######  tkinter  end   ######

            
def open_camera():   
    if cam_on:
        global cam_count
        cam_count = cam_count + 1
        # Capture the video frame by frame 
        _, frame = vid.read() 
    
        # Convert image from one color space to other 
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
        imS = cv2.resize(opencv_image, (640, 640))
    
        ######  tkinter  start ######
        # Capture the latest frame and transform to image 
        image = Image.fromarray(imS) 
    
        # Convert captured image to photoimage 
        photo = ImageTk.PhotoImage(image=image) 
    
        # Displaying photoimage in the label 
        label_camera1.photo_image = photo 
    
        # Configure image in the label 
        label_camera1.configure(image=photo)

        if cam_count >= 50:
            count_fire(cam_count)
        if cam_count >= 60:
            cam_count = 0
        
        # Repeat the same process after every 10 milliseconds 
        label_camera1.after(1, open_camera) 
        ######  tkinter  end   ######

show_confidence1_value(confidence)

def start_cam():
    global cam_on
    # stop_cam()
    cam_on = True
    open_camera()

def stop_cam():
    global cam_on
    # modbus.write_detected([1,0,0], client)
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
    traceback.print_exc(file=sys.stdout)
finally:
    cv2.destroyAllWindows()
    # modbus.write_detected([1,0,0], client)
    print("Sent modbus [1,0,0]")
    print('fin')
######  tkinter  start   ######