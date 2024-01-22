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

# Create a list to count fire occurances
global detected_list
detected_list=[]

# Create each classes threshold
classes = [0, 1, 2, 3]
thresholds = [0.5, 0.8, 0.8, 0.8]

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
        # Remove the first element
        detected_a.pop(0)
    
        if detected_a.count(1) > 3:

            #########################  
            # Make folders if not exsist
            path='detect_image\\'+date.format_date()+'\\'
            makedirs(path)

            #send modbus [1,0,0] mean is stop vibration
            modbus.write_detected([1,0,0]) 

            # Read camara after stop PLC
            for i in range(5):
                output_image2 = my_callback.image

                if output_image2 is not None:

                    img_copy2 = output_image2.copy()
                    img_copy2 = cv2.cvtColor(output_image2, cv2.COLOR_BayerRG2RGB)

                    # Run YOLOv8 inference on the frame
                    results2 = model.predict(img_copy2, save=False, imgsz=1024, conf=0.5)
                    result2 = results2[0]

                    # Visualize the results on the frame
                    annotated_frame2 = results2[0].plot()

                    # Display the annotated frame
                    imS2 = cv2.resize(annotated_frame2, (640, 640)) 
                    cv2.imshow("YOLOv8 Inference2", imS2)
                
            # Modbus write
            if(len(result2.boxes)!=0):
                cords2 = result2.boxes.xyxy[0].tolist()
                cords2 = [round(x) for x in cords2]
                start2 = cords2[0:2]  # x1,y1

                start2.insert(0,1)
                
                # Saving images
                cv2.imwrite('detect_image\\'+date.format_date()+'\\'+date.get_time_in_mmddss()+'.jpg', imS2)

                modbus.write_detected(start2)

                # Reset count list
                global detected_list
                detected_list=[0,0,0,0,0,0,0]
                print(detected_list)
                print("--")

            else:
                # Break the loop if the end of the video is reached
                print('no detacted')
                modbus.write_detected([0,0,0])
                return 0
                    

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




########################################################

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
                
                #########################  

                # append 1 if something has been detected
                if(len(result.boxes)!=0):
                    for box in results:
                        i=0
                        i = i + 1
                        if box.boxes.cls[i] in classes and box.boxes.conf[i] >= thresholds[int(box.boxes.cls[i])]:
                            detected_list.append(1)  # Add the last element
                else:
                    # Break the loop if the end of the video is reached
                    detected_list.append(0)
                    modbus.write_detected([0,0,0])
                    print('no detacted')

                print("detect_list: ", detected_list)
                count_fire(detected_list)

                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    done = True
                    modbus.write_detected([0,0,0])
                    break

########################################################
            
        # Stop the image acquisition of the camera side
        st_device.acquisition_stop()

        # Stop the image acquisition of the host side
        st_datastream.stop_acquisition()

    except Exception as exception:
        print(exception)
