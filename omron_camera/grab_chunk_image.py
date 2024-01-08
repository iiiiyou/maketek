"""
This sample shows the basic operation of using StApi and display chunk data
of the received image.
The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Acquire and display chunk data.
"""

import stapipy as st

# Number of images to grab
number_of_images_to_grab = 100

# Flag to indicate if all chunks are enabled
enable_all_chunks = True

# Feature names
CHUNK_MODE_ACTIVE = "ChunkModeActive"
CHUNK_SELECTOR = "ChunkSelector"
CHUNK_ENABLE = "ChunkEnable"

# If enable_all_chunks is False, enable only the following chunk:
TARGET_CHUNK_NAME = "ExposureTime"


def display_node_values(node_list):
    """
    Display node values.

    :param node_list: list of nodes to display.
    """
    for node in node_list:
        node_value = str(node.value) \
            if node.is_readable else "not readable"
        print("{0}: {1}".format(node.name, node_value))


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

        # Get the nodemap object to access current setting of the camera.
        st_nodemap_remote = st_device.remote_port.nodemap

        # Get related node to access and activate chunk
        st_chunk_mode_active = st_nodemap_remote.get_node(CHUNK_MODE_ACTIVE)
        st_chunk_mode_active.value = True

        # Get the PyIEnumeration of the chunk selector.
        # Here, .get() is used to shorten the code. To make the code more
        # understandable, casting can be used as well:
        # st_chunk_selector = \
        #   st.PyIEnumeration(st_nodemap_remote.get_node(CHUNK_SELECTOR))
        st_chunk_selector = st_nodemap_remote.get_node(CHUNK_SELECTOR).get()

        # Get chunk enable.
        st_chunk_enable = st_nodemap_remote.get_node(CHUNK_ENABLE)

        st_chunk_value_list = []
        if enable_all_chunks:
            chunk_lists = st_chunk_selector.entries
            for chunk_item in chunk_lists:
                # Skip unavailable chunk.
                if not chunk_item.is_available:
                    continue
                # Set selector to the chunk item and enable it.
                st_chunk_selector.set_int_value(chunk_item.value)
                if st_chunk_enable.is_writable:
                    st_chunk_enable.value = True

                # Get the node for the value of the Chunk and put to list.
                chunk_value = st_nodemap_remote.get_node(
                    "Chunk" + st.PyIEnumEntry(chunk_item).symbolic_value)
                if chunk_value:
                    st_chunk_value_list.append(chunk_value)
                    chunk_value = None
        else:
            # Get the entry for the specified chunk.
            chunk_item = st_chunk_selector[TARGET_CHUNK_NAME]
            if chunk_item.is_available:
                # Set the selector to the chunk and enable it.
                st_chunk_selector.set_int_value(chunk_item.value)
                if st_chunk_enable.is_writable:
                    st_chunk_enable.value = True
                # Get the node for the value of the Chunk and put to list.
                chunk_value = st_nodemap_remote.get_node(TARGET_CHUNK_NAME)
                if chunk_value:
                    st_chunk_value_list.append(chunk_value)
                    chunk_value = None

        # Start the image acquisition of the host (local machine) side.
        st_datastream.start_acquisition(number_of_images_to_grab)

        # Start the image acquisition of the camera side.
        st_device.acquisition_start()

        # A while loop for acquiring data and checking status
        while st_datastream.is_grabbing:
            # Create a localized variable st_buffer using 'with'
            with st_datastream.retrieve_buffer() as st_buffer:
                # Check if the acquired data contains image data.
                if st_buffer.info.is_image_present:
                    # Create an image object.
                    st_image = st_buffer.get_image()
                    # Display the information of the acquired image data.
                    print("BlockID={0} Size={1} x {2} First Byte={3} "
                          "Timestamp={4}".format(
                              st_buffer.info.frame_id,
                              st_image.width, st_image.height,
                              st_image.get_image_data()[0],
                              st_buffer.info.timestamp))
                    display_node_values(st_chunk_value_list)
                else:
                    # If the acquired data contains no image data.
                    print("Image data does not exist.")

        # Stop the image acquisition of the camera side
        st_device.acquisition_stop()

        # Stop the image acquisition of the host side
        st_datastream.stop_acquisition()

        # Stop event acquisition thread
        st_device.stop_event_acquisition()

    except Exception as exception:
        print(exception)
