"""
 This sample shows how to save/load camera setting with using featureBag.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Save/load camera setting to/from file
 - Apply the loaded setting to camera
"""

import os
import tempfile

import stapipy as st

try:
    # Initialize StApi before using.
    st.initialize()

    # Create a system object for device scan and connection.
    st_system = st.create_system()

    # Connect to first detected device.
    st_device = st_system.create_first_device()

    # Display DisplayName of the device.
    print('Device=', st_device.info.display_name)

    filename = os.path.join(tempfile.gettempdir(), "features.cfg")

    # Get the remote nodemap.
    nodemap = st_device.remote_port.nodemap

    # Create feature bag object.
    featurebag = st.create_featurebag()
    featurebag.store_nodemap_to_bag(nodemap)

    # Display all settings.
    features = featurebag.save_to_string()
    print(features)

    # Save settings in the feature bag to file.
    print("Saving", filename)
    featurebag.save_to_file(filename)
    print("Saving done")

    # Create another feature bag for loading setting from file.
    featurebag2 = st.create_featurebag()

    # Load the setting from file created above to the feature bag
    featurebag2.store_file_to_bag(filename)

    # Load the setting from the feature bag to camera
    print("Loading to camera..")
    featurebag2.load(nodemap, True)
    print("Loading to camera done")

except Exception as exception:
    print(exception)
