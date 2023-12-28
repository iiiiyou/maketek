''' 
streamlit run webcam_streamlit_sandbox3.py --server.headless true --server.port 8888
'''

import av
import cv2
import streamlit as st
import pymodbus
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes, WebRtcMode, VideoProcessorBase, RTCConfiguration
from ultralytics import YOLO
import time
import threading
import LS_Modbus as modbus
import format_date_time as date
import os
import datetime


def makedirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")
        

model = YOLO("yolov8n.pt") 
st.title("Live Detection")

def process(result, frame):
    if(len(result.boxes)!=0):
        class_id = result.names[result.boxes.cls[0].item()]
        cords = result.boxes.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        conf = round(result.boxes.conf[0].item(), 2)
        
        print(result.names[result.boxes.cls[0].item()])

        print(len(result.boxes))

        print(type(class_id))

        start = cords[0:2]  # x1,y1
        end = cords[2:4]  # x2,y2
        frame = cv2.rectangle(frame, start, end, (255, 0, 0), 2)

        message = f"{class_id}, {start}, {conf}"
        frame = cv2.putText(frame, message , (0,30) , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        start.insert(0,1)

        print(start)

        # path='C:/Users/admin/Downloads/yolov81/yolov8/'+date.format_date()+'/'

        # makedirs(path)
        
        # cv2.imwrite('C:/Users/admin/Downloads/yolov81/yolov8/'+date.format_date()+'/'+date.get_time_in_mmddss()+'.jpg', frame)

        modbus.write_detected(start)
    else:
        # frame = cv2.
        print('no detacted')
        modbus.write_detected([0,0,0])

    return frame



def callback(frame):
    frame = frame.to_ndarray(format="bgr24")

    result = model(frame)[0]
    # for box in result.boxes:
    #     class_id = result.names[box.cls[0].item()]
    #     cords = box.xyxy[0].tolist()
    #     cords = [round(x) for x in cords]
    #     conf = round(box.conf[0].item(), 2)
        
    #     print(result.names[box.cls[0].item()])

    #     print(len(result.boxes))

    #     print(type(class_id))

    #     start = cords[0:2]  # x1,y1
    #     end = cords[2:4]  # x2,y2
    #     image = cv2.rectangle(frame, start, end, (255, 0, 0), 2)

    #     message = f"{class_id}, {start}, {conf}"
    #     image = cv2.putText(frame, message , (0,30) , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    #     start.insert(0,1)

    #     modbus.write_detected(start)

    
    image = process(result,frame)
        
    return av.VideoFrame.from_ndarray(image, format="bgr24")



webrtc_ctx = webrtc_streamer(
    key="live",
    mode=WebRtcMode.SENDRECV,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
    video_frame_callback=callback,
)


