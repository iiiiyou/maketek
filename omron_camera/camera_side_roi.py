"""
 This sample shows how to set ROI in camera side and handle the image data.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Set image ROI parameter
 - Acquire image data
 - Process the acquired ROI images
"""

import stapipy as st

# Number of images to grab
number_of_images_to_grab = 100

# Feature names
PIXEL_FORMAT = "PixelFormat"
REGION_SELECTOR = "RegionSelector"
REGION_MODE = "RegionMode"
OFFSET_X = "OffsetX"
OFFSET_Y = "OffsetY"
WIDTH = "Width"
HEIGHT = "Height"


def edit_enumeration(nodemap, enum_name) -> bool:
    """
    Display and edit enumeration value.

    :param nodemap: Node map.
    :param enum_name: Enumeration name.
    :return: True if enumeration value is updated. False otherwise.
    """
    node = nodemap.get_node(enum_name)
    if not node.is_writable:
        return False
    enum_node = st.PyIEnumeration(node)
    enum_entries = enum_node.entries
    print(enum_name)
    for index in range(len(enum_entries)):
        enum_entry = enum_entries[index]
        if enum_entry.is_available:
            print("{0} : {1} {2}".format(index,
                  st.PyIEnumEntry(enum_entry).symbolic_value,
                  "(Current)" if enum_node.value == enum_entry.value
                                         else ""))
    print("Else : Exit")
    selection = int(input("Select : "))
    if selection < len(enum_entries) and enum_entries[selection].is_available:
        enum_entry = enum_entries[selection]
        enum_node.set_int_value(enum_entry.value)
        return True


def edit_setting(nodemap, node_name):
    """
    Edit setting which has numeric type.

    :param nodemap:  Node map.
    :param node_name: Node name.
    """
    node = nodemap.get_node(node_name)
    if not node.is_writable:
        return
    if node.principal_interface_type == st.EGCInterfaceType.IFloat:
        node_value = st.PyIFloat(node)
    elif node.principal_interface_type == st.EGCInterfaceType.IInteger:
        node_value = st.PyIInteger(node)
    while True:
        print(node_name)
        print(" Min={0} Max={1} Current={2}{3}".format(
              node_value.min, node_value.max, node_value.value,
              " Inc={0}".format(node_value.inc) if\
                    node_value.inc_mode == st.EGCIncMode.FixedIncrement\
                    else ""))
        new_value = int(input("New value : "))
        print()
        if node_value.min <= new_value <= node_value.max:
            node_value.value = new_value
            return


def set_camera_side_roi(nodemap):
    """
    Set camera side ROI.

    :param nodemap: Node map.
    """
    region_selector = nodemap.get_node(REGION_SELECTOR)
    if not region_selector.is_writable:
        # Single ROI:
        edit_setting(nodemap, OFFSET_X)
        edit_setting(nodemap, WIDTH)
        edit_setting(nodemap, OFFSET_Y)
        edit_setting(nodemap, HEIGHT)
    else:
        while True:
            if not edit_enumeration(nodemap, REGION_SELECTOR):
                return

            edit_enumeration(nodemap, REGION_MODE)
            region_mode = st.PyIEnumeration(nodemap.get_node(REGION_MODE))
            if region_mode.current_entry.value != region_mode["Off"].value:
                edit_setting(nodemap, OFFSET_X)
                edit_setting(nodemap, WIDTH)
                edit_setting(nodemap, OFFSET_Y)
                edit_setting(nodemap, HEIGHT)


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

        # Get INodeMap object to access the setting of the device.
        remote_nodemap = st_device.remote_port.nodemap

        # Check and set PixelFormat
        edit_enumeration(remote_nodemap, PIXEL_FORMAT)

        # Check and set CameraSideROI
        set_camera_side_roi(remote_nodemap)

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
                if st_buffer.info.is_image_present:
                    # Create an image object.
                    st_image = st_buffer.get_image()
                    # Display the information of the acquired image data.
                    print("BlockID={0} Size={1} x {2} First Byte={3}".format(
                          st_buffer.info.frame_id,
                          st_image.width, st_image.height,
                          st_image.get_image_data()[0]))
                else:
                    # If the acquired data contains no image data.
                    print("Image data does not exist.")

        # Stop the image acquisition of the camera side
        st_device.acquisition_stop()

        # Stop the image acquisition of the host side
        st_datastream.stop_acquisition()

    except Exception as exception:
        print(exception)
