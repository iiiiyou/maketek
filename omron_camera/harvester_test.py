# https://pypi.org/project/harvesters/
# pip install harvesters

# Harvester’s Documentation
# https://harvesters.readthedocs.io/en/latest/index.html

# Harvester & OpenCV sample code
# https://gist.github.com/immengineer/d071831e4553bbd885a542212509ee55

from harvesters.core import Harvester
import cv2
import sys
import traceback


h = Harvester()
h.add_file('C:\\Program Files\\Common Files\\OMRON_SENTECH\\GenTL\\v1_5\\StGenTL_MD_VC141_v1_5_x64.cti')
h.files
h.update()
h.device_info_list
print(h.device_info_list)

# ia = h.create(0)
ia = h.create({'serial_number': '23G7076'})

try:
    ia.start()
    i = 0
    done = False
    while not done:
        with ia.fetch() as buffer:
            # Work with the Buffer object. It consists of everything you need.
            print(buffer)
            # The buffer will automatically be queued.
            img = buffer.payload.components[0].data
            img = img.reshape(buffer.payload.components[0].height, buffer.payload.components[0].width)
            img_copy = img.copy()
            img_copy = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)
            # cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
            imS = cv2.resize(img, (960, 960)) 
            cv2.imshow("window", imS)
            fps = ia.statistics.fps
            print("FPS: ", fps)
            if cv2.waitKey(10) == ord('q'):
                done = True
                print('break')
            i = i + 1
except Exception as e:
    traceback.print_exc(file=sys.stdout)
finally:
    ia.stop()
    ia.destroy()
    cv2.destroyAllWindows()
    print('fin')
    h.reset()

