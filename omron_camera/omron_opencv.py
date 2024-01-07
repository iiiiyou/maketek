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
import threading
import numpy as np
import stapipy as st
import omron_callback as oc

if __name__ == "__main__":
    my_callback = oc.CMyCallback()
    cb_func = my_callback.datastream_callback
    try:
        # Initialize StApi before using.
        st.initialize()

        # Create a system object for device scan and connection.
        st_system = st.create_system()

        # Connect to first detected device.
        st_device = st_system.create_first_device()

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
                cv2.imshow('image', output_image)
            # key_input = cv2.waitKey(1)
            # if key_input != -1:
            #     break
                
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
              break

        # Stop the image acquisition of the camera side
        st_device.acquisition_stop()

        # Stop the image acquisition of the host side
        st_datastream.stop_acquisition()

    except Exception as exception:
        print(exception)
