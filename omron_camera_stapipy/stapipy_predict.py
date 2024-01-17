"""
 This sample shows how to use OpenCV for format conversion and display.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Register and use callback function with StApi
 - Acquire image data via callback class function
 - Copy image data for OpenCV
 - Convert Bayer image format to RGB using OpenCV
 - Preview image using OpenCV
 Note: opencv-python and numpy packages are required:
    pip install numpy
    pip install opencv-python
"""

import cv2
from ultralytics import YOLO
import sys
sys.path.append('')

import format_date_time as date
import LS_Modbus as modbus
import os

import stapipy as st
import omron_callback as oc

# Load the YOLOv8 model
model = YOLO('models\\1664_four_class_annotation-2-1_19-seg.pt')  # pretrained YOLOv8n model

if __name__ == "__main__":
    my_callback = oc.CMyCallback()
    cb_func = my_callback.datastream_callback
    try:
        # Initialize StApi before using.
        st.initialize()

        # Create a system object for device scan and connection.
        st_system = st.create_system()
        interfacecount = st_system.interface_count
        is_find = 0
        for i in range(0, interfacecount) :
            if(is_find == 1):
                break
            st_interface = st_system.get_interface(i)
            devicecount = st_interface.device_count
            print(st_interface)
            print(devicecount)
            for j in range(0, devicecount) :
                device_info = st_interface.get_device_info(j)
                if(device_info.serial_number == "23G7076") : # - 1024 camera left
                # if(device_info.serial_number == "23G7069") : # - 1024 camera right
                # if(device_info.serial_number == "22FK019") : # - 1664 camera left
                    str_device_id = device_info.device_id
                    is_find = 1
                    break
                    

        st_device = st_interface.create_device_by_id(str_device_id)
        
        # Connect to first detected device.
        #st_device = st_system.create_first_device()

        # Display DisplayName of the device.
        print('Device=', st_device.info.display_name)

        # Create a datastream object for handling image stream data.
        st_datastream = st_device.create_datastream()

        # Register callback for datastream
        callback = st_datastream.register_callback(cb_func)

        # Start the image acquisition of the host (local machine) side.
        st_datastream.start_acquisition()

        # Start the image acquisition of the camera side.
        st_device.acquisition_start()

        print("To terminate, focus on the OpenCV window and press any key.")
        while True:
            output_image = my_callback.image
            if output_image is not None:

                img_copy = output_image.copy()
                img_copy = cv2.cvtColor(output_image, cv2.COLOR_BayerRG2RGB)

                # Run YOLOv8 inference on the frame
                results = model.predict(img_copy, save=False, imgsz=1024, conf=0.5)
                result = results[0]

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Display the annotated frame
                imS = cv2.resize(annotated_frame, (640, 640)) 
                cv2.imshow("YOLOv8 Inference", imS)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
              break

        # Stop the image acquisition of the camera side
        st_device.acquisition_stop()

        # Stop the image acquisition of the host side
        st_datastream.stop_acquisition()

    except Exception as exception:
        print(exception)
