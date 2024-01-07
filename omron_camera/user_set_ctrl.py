"""
 This sample shows how to use UserSet to load/save setting from/into camera ROM.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Load/Save UserSet with FeatureBag
"""

import stapipy as st

# Feature names
USER_SET_SELECTOR = "UserSetSelector"
USER_SET_TARGET = "UserSet1"
USER_SET_LOAD = "UserSetLoad"
USER_SET_SAVE = "UserSetSave"
USER_SET_DEFAULT = "UserSetDefault"
USER_SET_DEFAULT_SELECTOR = "UserSetDefaultSelector"
PIXEL_FORMAT = "PixelFormat"


def set_enumeration(nodemap, enum_name, entry_name):
    """
    Function to set enumeration value.

    :param nodemap: node map.
    :param enum_name:  name of the enumeration node.
    :param entry_name:  symbolic value of the enumeration entry node.
    """
    enum_node = st.PyIEnumeration(nodemap.get_node(enum_name))
    entry_node = st.PyIEnumEntry(enum_node[entry_name])
    # Note that depending on your use case, there are three ways to set
    # the enumeration value:
    # 1) Assign the integer value of the entry with set_int_value(val) or .value
    # 2) Assign the symbolic value of the entry with set_symbolic_value("val")
    # 3) Assign the entry (PyIEnumEntry) with set_entry_value(entry)
    # Here set_entry_value is used:
    enum_node.set_entry_value(entry_node)


def display_current_enumeration(nodemap, enum_name):
    """
    Display the current setting of the indicated enumeration of the node map.

    :param nodemap: node map.
    :param enum_name: name of the enumeration node.
    """
    enum_node = st.PyIEnumeration(nodemap.get_node(enum_name))
    print("Current {0} = {1}".format(
        enum_name, st.PyIEnumEntry(enum_node.current_entry).symbolic_value))


def edit_enumeration(nodemap, enum_name):
    """
    Display and allow user to modify the enumeration value.

    :param nodemap: node map.
    :param enum_name: name of the enumeration node.
    """
    node = nodemap.get_node(enum_name)
    if not node.is_writable:
        return

    # Get PyIEnumeration from PyNode.
    enum_node = st.PyIEnumeration(node)

    while True:
        print(enum_name)
        enum_entries = enum_node.entries
        for index in range(len(enum_entries)):
            enum_entry = enum_entries[index]
            if enum_entry.is_available:
                print("{0} : {1} {2}".format(index, 
                      st.PyIEnumEntry(enum_entry).symbolic_value,
                      "(Current)" if enum_node.value == enum_entry.value
                                             else ""))
        selection = int(input("Select : "))
        if selection < len(enum_entries):
            enum_entry = enum_entries[selection]
            enum_node.set_int_value(enum_entry.value)
            break


if __name__ == "__main__":
    try:
        # Initialize StApi before using.
        st.initialize()

        # Create a system object for device scan and connection.
        st_system = st.create_system()

        # Connect to first detected device.
        st_device = st_system.create_first_device(
            st.ETLDeviceAccessFlags.AccessExclusive)

        # Display DisplayName of the device.
        print('Device=', st_device.info.display_name)

        # Get the remote nodemap.
        nodemap = st_device.remote_port.nodemap

        # Set the UserSet to be used by UserSetSelector.
        set_enumeration(nodemap, USER_SET_SELECTOR, USER_SET_TARGET)

        # Load the UserSet stored in the ROM to the camera.
        # Here, .get() is used to automatically cast the PyNode to PyICommand.
        nodemap.get_node(USER_SET_LOAD).get().execute()

        print("Loaded :", USER_SET_TARGET)

        # Create a FeatureBag object for acquiring/saving camera settings.
        featurebag = st.create_featurebag()

        # Save the current settings to FeatureBag.
        featurebag.store_nodemap_to_bag(nodemap)

        # Set the pixel format.
        edit_enumeration(nodemap, PIXEL_FORMAT)

        # Display current pixel format setting.
        display_current_enumeration(nodemap, PIXEL_FORMAT)

        # Load the UserSet that are stored in the ROM to the camera.
        # Here, .get() is used to automatically cast the PyNode to PyICommand.
        nodemap.get_node(USER_SET_LOAD).get().execute()
        print("Loaded :", USER_SET_TARGET)

        # Display current pixel format setting.
        display_current_enumeration(nodemap, PIXEL_FORMAT)

        # Load the settings in the FeatureBag to the camera.
        featurebag.load(nodemap)

        # Set the UserSet for UserSetSelector.
        set_enumeration(nodemap, USER_SET_SELECTOR, USER_SET_TARGET)

        # Save the current settings to UserSet.
        # Here, .get() is used to automatically cast the PyNode to PyICommand.
        nodemap.get_node(USER_SET_SAVE).get().execute()
        print("Saved :", USER_SET_TARGET)

        if nodemap.get_node(USER_SET_DEFAULT):
            display_current_enumeration(nodemap, USER_SET_DEFAULT)
        else:
            display_current_enumeration(nodemap, USER_SET_DEFAULT_SELECTOR)

    except Exception as exception:
        print(exception)
