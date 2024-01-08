import stapipy as st

st.initialize() # StApi 초기화
st_system = st.create_system() # GenTL의 시스템 모듈 및 인터페이스 모듈 open
st_device = st_system.create_first_device() # 처음 발견된 카메라 Open

# 원격 장지의 GenApi nodemap을 가져오고, 이름이 width라는 노드를 가져오기.
st_nodemap_remote = st_device.remote_port.nodemap #stapipy.PyNodeMap의 인스턴스를 반환
width_node = st_nodemap_remote.get_node("Width") # stapipy.PyNode의 인스턴스를 반환
print("Width value:", width_node.value)
print("Interface type:", width_node.principal_interface_type)