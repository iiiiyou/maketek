"""
 This sample shows how to register an event callback with callback function.
 Here we register the callback function to "ExposureEnd" event (Defined as
 TARGET_EVENT_NAME) with a callback function to handle this event.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Acquire image data with callback function
 - Enable the event message sending function of camera
 - Register callback function of indicated event
"""

import stapipy as st

# Number of images to grab
number_of_images_to_grab = 100

# Feature names
EVENT_SELECTOR = "EventSelector"
EVENT_NOTIFICATION = "EventNotification"
EVENT_NOTIFICATION_ON = "On"
TARGET_EVENT_NAME = "ExposureEnd"
CALLBACK_NODE_NAME = "EventExposureEndTimestamp"


def node_callback(node=None, context=None):
    """
    Callback to handle events from GenICam node.

    :param node: node that trigger the callback.
    :param context: user data passed on during callback registration.
    """
    try:
        if node.is_readable:
            print("{0} = {1}".format(node.name, node.value))
        else:
            print("{0} is not readable".format(node.name))
    except Exception as my_exception:
        print("node_callback", my_exception)


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

        # Get node of "EventExposureEndTimestamp" for event registration.
        st_event_node = st_nodemap_remote.get_node(CALLBACK_NODE_NAME)

        # Register callback for EventExposureEndTimestamp.
        st_event_node.register_callback(node_callback)

        # Get event selector.
        st_event_selector = st_nodemap_remote.get_node(EVENT_SELECTOR).get()
        # As alternative of the above statement, it is also possible to
        # use the following statement to make the code easier to understand:
        # st_event_selector = st.PyIEnumeration(
        #                     st_nodemap_remote.get_node(EVENT_SELECTOR))

        # Select the target event.
        # Note that depending on your use case, there are three ways to set
        # the enumeration value:
        # 1) Assign the integer value of the entry with set_int_value or .value
        # st_event_selector_entry = st_event_selector[TARGET_EVENT_NAME].get()
        # st_event_selector.set_int_value(st_event_selector_entry.numeric_value)
        # or: st_event_selector.value = st_event_selector_entry.numeric_value
        # 2) Assign the symbolic value of the entry with set_symbolic_value
        # st_event_selector.set_symbolic_value(TARGET_EVENT_NAME)
        # 3) Assign the entry (PyIEnumEntry) with set_entry_value
        # st_event_selector_entry = st_event_selector[TARGET_EVENT_NAME].get()
        # st_event_selector.set_entry_value(st_event_selector_entry)
        # Here we used 2) because we already know and sure the symbolic name.
        st_event_selector.set_symbolic_value(TARGET_EVENT_NAME)

        # Enable event notification.
        st_event_notification = st.PyIEnumeration(st_nodemap_remote
                                                  .get_node(EVENT_NOTIFICATION))
        st_event_notification.set_symbolic_value(EVENT_NOTIFICATION_ON)

        # Start event handling thread
        st_device.start_event_acquisition()

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
