import pyzwoasi

from pyzwoasi import ZWOCamera

if __name__ == "__main__":
    numOfConnectedCameras = pyzwoasi.getNumOfConnectedCameras()
    if (numOfConnectedCameras == 0):
        print("No camera connected")
        exit()

    for cameraIndex in range(numOfConnectedCameras):
        with ZWOCamera(cameraIndex) as camera:
            camera.liveView()