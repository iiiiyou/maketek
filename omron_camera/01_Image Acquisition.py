import stapipy as st

st.initialize() # StApi 초기화
st_system = st.create_system() # GenTL의 시스템 모듈 및 인터페이스 모듈 open
st_device = st_system.create_first_device() # 처음 발견된 카메라 Open
st_datastream = st_device.create_datastream() # 장치의 datastream Open
st_datastream.start_acquisition(100) # 호스트의 이미지 데이터 수집 시작(100 frames)
st_device.acquisition_start() # 이미지 데이터 전송 시작

while st_datastream.is_grabbing:
   with st_datastream.retrieve_buffer() as st_buffer:
       if st_buffer.info.is_image_present:
           st_image = st_buffer.get_image()
           print("BlockID={0} Size={1} x {2} First Byte={3}".format(
                 st_buffer.info.frame_id,
                 st_image.width,
                 st_image.height,
                 st_image.get_image_data()[0]))
       else:
           print("Image data does not exist.")
st_device.acquisition_stop() # 이미지 데이터 전송 중지
st_datastream.stop_acquisition() # 호스트의 이미지 데이터 수집 중지