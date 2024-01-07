import time
import ipaddress
import stapipy as st

# Feature names
# GEV_INTERFACE_SUBNET_IP_ADDRESS = "GevInterfaceSubnetIPAddress"
# GEV_INTERFACE_SUBNET_MASK = "GevInterfaceSubnetMask"

DEVICE_SELECTOR = "DeviceSelector"
GEV_DEVICE_IP_ADDRESS = "GevDeviceIPAddress"
# GEV_DEVICE_SUBNET_MASK = "GevDeviceSubnetMask"

GEV_DEVICE_FORCE_IP_ADDRESS = "GevDeviceForceIPAddress"
# GEV_DEVICE_FORCE_SUBNET_MASK = "GevDeviceForceSubnetMask"
# GEV_DEVICE_FORCE_IP = "GevDeviceForceIP"
# DEVICE_LINK_HEARTBEAT_TIMEOUT = "DeviceLinkHeartbeatTimeout"
# GEV_HEARTBEAT_TIMEOUT = "GevHeartbeatTimeout"

st.initialize()
st_system = st.create_system()

index_size = st_system.interface_count
st_interface = st_system.get_interface(index_size-2)

nodemap = st_interface.port.nodemap

device_selector = nodemap.get_node(DEVICE_SELECTOR).get()
max_index = device_selector.max

# Display the current IP address of the device.
device_ip = nodemap.get_node(GEV_DEVICE_IP_ADDRESS).get()
print("Device IP Address =", device_ip.to_string())

st_device = st_interface.create_device_by_index(max_index)

# Display DisplayName of the device.
print('Device=', st_device.info.display_name)

# Create a datastream object for handling image stream data.
st_datastream = st_device.create_datastream()

# create_device_by_index