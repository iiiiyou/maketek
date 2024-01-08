"""
 This sample shows how to divide image data into multiple ROI images in local
 side and display them using OpenCV.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Acquire image
 - Process image ROI in host side (local computer)
 - Copy image data for OpenCV
 - Convert Bayer image format to RGB using OpenCV
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
DISPLAY_RESIZE_FACTOR = 0.5

# Regions of each direction.
HORIZONTAL_ROI_COUNT = 4
VERTICAL_ROI_COUNT = 2


def display_with_opencv(window_title, img, pixel_format_info):
    """
    Function to convert PyIStImage pixel format and display it using OpenCV.

    :param img: Image to process
    :param pixel_format_info: Pixel format info.
    """
    # Get raw image data.
    data = img.get_image_data()

    # Perform pixel value scaling if each pixel component is
    # larger than 8bit. Example: 10bit Bayer/Mono, 12bit, etc.
    if pixel_format_info.each_component_total_bit_count > 8:
        nparr = np.frombuffer(data, np.uint16)
        division = pow(2, pixel_format_info
                       .each_component_valid_bit_count - 8)
        nparr = (nparr / division).astype('uint8')
    else:
        nparr = np.frombuffer(data, np.uint8)

    # Process image for display.
    nparr = nparr.reshape(img.height, img.width, 1)

    # Perform color conversion for Bayer.
    if pixel_format_info.is_bayer:
        bayer_type = pixel_format_info.get_pixel_color_filter()
        if bayer_type == st.EStPixelColorFilter.BayerRG:
            nparr = cv2.cvtColor(nparr, cv2.COLOR_BAYER_RG2RGB)
        elif bayer_type == st.EStPixelColorFilter.BayerGR:
            nparr = cv2.cvtColor(nparr, cv2.COLOR_BAYER_GR2RGB)
        elif bayer_type == st.EStPixelColorFilter.BayerGB:
            nparr = cv2.cvtColor(nparr, cv2.COLOR_BAYER_GB2RGB)
        elif bayer_type == st.EStPixelColorFilter.BayerBG:
            nparr = cv2.cvtColor(nparr, cv2.COLOR_BAYER_BG2RGB)

    # Resize image and display.
    nparr = cv2.resize(nparr, None,
                       fx=DISPLAY_RESIZE_FACTOR,
                       fy=DISPLAY_RESIZE_FACTOR)
    cv2.imshow(window_title, nparr)


if __name__ == "__main__":
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

        # Get the device nodemap to access the device settings.
        remote_nodemap = st_device.remote_port.nodemap

        # Get current setting of the image size.
        image_size = [remote_nodemap.get_node("Width").value,
                      remote_nodemap.get_node("Height").value]

        # Get current pixel format information.
        pixel_format = remote_nodemap.get_node("PixelFormat").value
        pixel_format_info = st.get_pixel_format_info(pixel_format)

        # Get the minimum setting unit of both sides (X and Y).
        pixel_increment = [pixel_format_info.pixel_increment_x,
                           pixel_format_info.pixel_increment_y]

        # Calculate the size of the ROI.
        roi_window_count = [HORIZONTAL_ROI_COUNT, VERTICAL_ROI_COUNT]
        roi_image_size = []
        for index in range(2):
            size = image_size[index] // roi_window_count[index]
            size = size - (size % pixel_increment[index])
            roi_image_size.append(size)

        # Prepare display window
        for pos_y in range(roi_window_count[1]):
            for pos_x in range(roi_window_count[0]):
                window_title = "image_{0}{1}".format(pos_y, pos_x)
                cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
                cv2.moveWindow(window_title,
                    int(pos_x * roi_image_size[0] * DISPLAY_RESIZE_FACTOR),
                    int(pos_y * roi_image_size[1] * DISPLAY_RESIZE_FACTOR))
                cv2.resizeWindow(window_title,
                    int(roi_image_size[0] * DISPLAY_RESIZE_FACTOR),
                    int(roi_image_size[1] * DISPLAY_RESIZE_FACTOR))

        # Start the image acquisition of the host (local machine) side.
        st_datastream.start_acquisition(number_of_images_to_grab)

        # Start the image acquisition of the camera side.
        st_device.acquisition_start()

        # A while loop for acquiring data and checking status
        while st_datastream.is_grabbing:
            # Create a localized variable st_buffer using 'with'
            # Warning: if st_buffer is in a global scope, st_buffer must be
            # assign to None to allow Garbage Collector release the buffer
            # properly.
            with st_datastream.retrieve_buffer() as st_buffer:
                # Check if the acquired data contains image data.
                if not st_buffer.info.is_image_present:
                    print("Image data does not exist.")
                    continue

                # Create an image object.
                st_image = st_buffer.get_image()

                # Display the information of the acquired image data.
                print("BlockID={0} Size={1} x {2} {3}[fps]".format(
                      st_buffer.info.frame_id,
                      st_image.width, st_image.height,
                      st_datastream.current_fps))

                # Only mono or bayer is processed.
                if not(pixel_format_info.is_mono or pixel_format_info.is_bayer):
                    continue

                # Display image.
                display_with_opencv("image", st_image, pixel_format_info)

                # Process and display each ROI image.
                for pos_y in range(roi_window_count[1]):
                    for pos_x in range(roi_window_count[0]):
                        roi_image = st_image.get_roi_image(
                            pos_x * roi_image_size[0],
                            pos_y * roi_image_size[1],
                            roi_image_size[0],
                            roi_image_size[1])
                        window_title = "image_{0}{1}".format(pos_y, pos_x)
                        display_with_opencv(window_title,
                                            roi_image, pixel_format_info)
                cv2.waitKey(1)

        # Stop the image acquisition of the camera side
        st_device.acquisition_stop()

        # Stop the image acquisition of the host side
        st_datastream.stop_acquisition()

    except Exception as exception:
        print(exception)
