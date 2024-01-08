"""
 This sample shows how to use the multicast function of GigE camera for multiple receivers.
 The monitor clients must connect after any one client connect to camera in control mode.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Acquire image data (with waiting in main thread)
 - Connect to camera in control mode / monitor mode
 - Multicast the image data
 - Broadcast the image data
"""

import stapipy as st

# Number of images to grab
number_of_images_to_grab = 100

# Feature names
DESTINATION_IP_ADDRESS = "DestinationIPAddress"
DESTINATION_PORT = "DestinationPort"
TRANSMISSION_TYPE = "TransmissionType"
TRANSMISSION_TYPE_USE_CAMERA_CONFIGURATION = "UseCameraConfiguration"

try:
    # Initialize StApi before using.
    st.initialize()

    # Select the connecting mode (control/monitor) of the camera.
    # You can connect to a camera in monitor mode if it has already connected
    # by other host with control mode.
    # Note if you connect to a camera in monitor mode, you cannot modify the
    # camera settings.
    is_monitor = False
    while True:
        print()
        print("c : Control mode")
        print("m : Monitor mode")
        selection = input("Select a mode : ")
        if selection not in ['c', 'C', 'm', 'M']:
            continue
        is_monitor = True if selection == 'm' or selection == 'M' else False
        break

    st_system = st.create_system(st.EStSystemVendor.Default,
                                 st.EStInterfaceType.GigEVision)

    # Connect to first detected device.
    st_device = st_system.create_first_device(
        st.ETLDeviceAccessFlags.AccessReadOnly if is_monitor else \
            st.ETLDeviceAccessFlags.AccessControl)

    # Display DisplayName of the device.
    print('Device=', st_device.info.display_name)

    # Create a datastream object for handling image stream data.
    st_datastream = st_device.create_datastream()

    # Get the IENumeration of TransmissionType.
    transtype = st_datastream.port.nodemap\
        .get_node(TRANSMISSION_TYPE).get()
    # Get the setting based on the connection type.
    if is_monitor:
        camera_config = transtype[TRANSMISSION_TYPE_USE_CAMERA_CONFIGURATION]
        transtype_value = camera_config.value
    else:
        transtype_list = transtype.entries
        while True:
            print("Supported transmission types are as follows.")
            for index in range(len(transtype_list)):
               print("{0} : {1}".format(index,
                     transtype_list[index].get().symbolic_value))
            selection = int(input("Select a transmission type : "))
            if 0 <= selection  <= len(transtype_list):
                transtype_value = transtype_list[selection].value
                break

    # Configure the selected transmission type.
    transtype.set_int_value(transtype_value)

    # Get and display the IP address of the image data.
    dest_ip = st_datastream.port.nodemap.get_node(DESTINATION_IP_ADDRESS).get()
    print("Destination IP Address =", dest_ip.to_string())

    # Start the image acquisition of the host (local machine) side.
    st_datastream.start_acquisition(number_of_images_to_grab)

    # Start the image acquisition of the camera side if in control mode.
    if not is_monitor:
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
            else:
                # If the acquired data contains no image data.
                print("Image data does not exist.")

    # Stop the image acquisition of the camera side if in control mode.
    if not is_monitor:
        st_device.acquisition_stop()

    # Stop the image acquisition of the host side
    st_datastream.stop_acquisition()

except Exception as exception:
    print(exception)
