import cv2

def countCameras():
    """Returns count of found cameras (not opened yet).
    Brute force - just tries them all till it fails."""

    camCount = 0

    while True:
        cam = cv2.VideoCapture(camCount)

        if cam.isOpened():
            print("Found camera", camCount)
            cam.release()
            camCount += 1

        else:
            return camCount

countCameras()