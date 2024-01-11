import cv2
from ultralytics import YOLO

import sys
sys.path.append('C:\\workspace\\maketek')
import format_date_time as date
import LS_Modbus as modbus
import os

from harvesters.core import Harvester
import sys
import traceback

import tkinter as tk 
from PIL import Image, ImageTk 

h = Harvester()
h.add_file('C:\\Program Files\\Common Files\\OMRON_SENTECH\\GenTL\\v1_5\\StGenTL_MD_VC141_v1_5_x64.cti')
h.files
h.update()
h.device_info_list
print(h.device_info_list)

# ia = h.create(0)
ia = h.create({'serial_number': '23G7076'}) # - 1080 camera left
# ia = h.create({'serial_number': '23G7069'}) # - 1080 camera right
# ia = h.create({'serial_number': '22FK019'}) # - 2048 camera left

# Make folders if not exsist
def makedirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")


# Load the YOLOv8 model
model = YOLO('model\\2048_two_class_full_annotation-5_seg_9.pt')  # pretrained YOLOv8n model
# model = YOLO('model\\2048_two_class_full_annotation-2_detect.pt')  # pretrained YOLOv8n model
        
# Create a Tkinter window
root = tk.Tk()
root.title("Detection Display")
root.geometry("640x480")

# Create a label to display the video frames
label = tk.Label(root)
label.pack()

# Create a label and display it on app 
label_widget = tk.Label(root) 
label_widget.pack() 

# Create a function to open camera and 
# display it in the label_widget on app 

def open_camera(): 

    try:
        ia.start()
        i = 0
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

                results = model.predict(img_copy, save=False, imgsz=2048, conf=0.65)
                result = results[0]

                # Visualize the results on the frame
                annotated_frame = results[0].plot()
                                
                # img_copy = img.copy()
                # img_copy = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)
                # cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
                # imS = cv2.resize(annotated_frame, (960, 960)) 
                # cv2.imshow("YOLOv8 Inference", imS)

                # Capture the latest frame and transform to image 
                image = Image.fromarray(annotated_frame) 
                # Convert captured image to photoimage 
                photo = ImageTk.PhotoImage(image=image) 

                # Displaying photoimage in the label 
                label_widget.photo_image = photo 

                # Configure image in the label 
                label_widget.configure(image=photo) 

                # Repeat the same process after every 10 seconds 
                label_widget.after(10, open_camera) 

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
                i = i + 1
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    finally:
        ia.stop()
        ia.destroy()
        cv2.destroyAllWindows()
        print('fin')
        h.reset()

# Create a button to open the camera in GUI app 
btn_open = tk.Button(root, text="Open Camera", command=open_camera) 
# btn_open.grid(row=0,column=0) 
btn_open.pack()
  
# Create an infinite loop for displaying app on screen 
root.mainloop() 


cv2.destroyAllWindows()
