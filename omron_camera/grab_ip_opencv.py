"""
 This sample shows how to use StApi with OpenCV for format conversion and display.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Acquire image data
 - Copy image data for OpenCV
 - Convert Bayer image format to BGR8 using StApi IP
 - Preview image using OpenCV
 Note: opencv-python and numpy packages are required:
    pip install numpy
    pip install opencv-python
"""

import cv2
import numpy as np
import stapipy as st

# Number of images to grab
number_of_images_to_grab = 1000

# Image scale when displaying using OpenCV.
DISPLAY_RESIZE_FACTOR = 0.3

try:
    # Initialize StApi before using.
    st.initialize()

    # Initialize converter
    st_converter = st.create_converter(st.EStConverterType.PixelFormat)
    st_converter.destination_pixel_format = \
        st.EStPixelFormatNamingConvention.BGR8

    # Create a system object for device scan and connection.
    st_system = st.create_system()

    # Connect to first detected device.
    st_device = st_system.create_first_device()

    # Display DisplayName of the device.
    print('Device=', st_device.info.display_name)

    # Create a datastream object for handling image stream data.
    st_datastream = st_device.create_datastream()

    # Start the image acquisition of the host (local machine) side.
    st_datastream.start_acquisition(number_of_images_to_grab)

    # Start the image acquisition of the camera side.
    st_device.acquisition_start()

    # A while loop for acquiring data and checking status
    while st_datastream.is_grabbing:
        # Create a localized variable st_buffer using 'with'
        # Warning: if st_buffer is in a global scope, st_buffer must be
        #          assign to None to allow Garbage Collector release the buffer
        #          properly.
        with st_datastream.retrieve_buffer() as st_buffer:
            # Check if the acquired data contains image data.
            if st_buffer.info.is_image_present:
                # Create an image object.
                st_image = st_buffer.get_image()

                # Display the information of the acquired image data.
                print("BlockID={0} Size={1} x {2} First Byte={3}".format(
                      st_buffer.info.frame_id,
                      st_image.width, st_image.height,
                      st_image.get_image_data()[0]))

                # Convert image and get the NumPy array.
                st_image = st_converter.convert(st_image)
                data = st_image.get_image_data()
                nparr = np.frombuffer(data, np.uint8)
                nparr = nparr.reshape(st_image.height, st_image.width, 3)

                # Resize image.and display.
                nparr = cv2.resize(nparr, None,
                                   fx=DISPLAY_RESIZE_FACTOR,
                                   fy=DISPLAY_RESIZE_FACTOR)
                cv2.imshow('image', nparr)
                cv2.waitKey(1)
            else:
                # If the acquired data contains no image data.
                print("Image data does not exist.")

    # Stop the image acquisition of the camera side
    st_device.acquisition_stop()

    # Stop the image acquisition of the host side
    st_datastream.stop_acquisition()

except Exception as exception:
    print(exception)
