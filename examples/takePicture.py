import matplotlib.pyplot as plt
import numpy as np, time

import pyzwoasi

from pyzwoasi.pyzwoasi import ASIExposureStatus

if __name__ == "__main__":
    numOfConnectedCameras = pyzwoasi.getNumOfConnectedCameras()
    if (numOfConnectedCameras == 0):
        print("No camera connected")
        exit()

    for cameraIndex in range(numOfConnectedCameras):
        # Let's get some information about the chosen camera
        cameraInfo = pyzwoasi.getCameraProperty(cameraIndex)

        # Let's open and init the camera
        pyzwoasi.openCamera(cameraIndex)
        pyzwoasi.initCamera(cameraIndex)

        # Read and save all camera controls
        numOfControls = pyzwoasi.getNumOfControls(cameraIndex)
        controlValues = {}
        for controlIndex in range(numOfControls):
            controlCaps  = pyzwoasi.getControlCaps(cameraIndex, controlIndex)
            controlValue = pyzwoasi.getControlValue(cameraIndex, controlIndex)
            controlName  = controlCaps.Name.decode('utf-8')
            controlValues[controlName] = controlValue
            
        # Now that the camera is initialized, we can set the ROI format
        wd, ht, binning, imageType = pyzwoasi.getROIFormat(cameraIndex)
        print(f"Camera {cameraIndex} - Resolution: {wd}x{ht}, Binning: {binning}, Image Type: {imageType}")

        # Selection of the exposure time (in microseconds)
        exposureTime = 10 # 1 second
        pyzwoasi.setControlValue(cameraIndex, 1, exposureTime, auto=False)

        print("Exposure started...")

        pyzwoasi.startExposure(cameraIndex, True)
        time.sleep(exposureTime / 1000)
        
        failedRuns = 0
        while  pyzwoasi.getExpStatus(cameraIndex) != ASIExposureStatus.ASI_EXP_SUCCESS:
            if pyzwoasi.getExpStatus(cameraIndex) == ASIExposureStatus.ASI_EXP_WORKING:
                pass
            elif pyzwoasi.getExpStatus(cameraIndex) == ASIExposureStatus.ASI_EXP_FAILED:
                if failedRuns >= 3:
                    print("Exposure failed 3 times. Aborting...")
                    exit()

                # Exposure has failed (that may happen for various reasons)
                # Let's restart the process and watch if it happens again.
                failedRuns += 1

                pyzwoasi.stopExposure(cameraIndex)
                pyzwoasi.startExposure(cameraIndex, True)
                time.sleep(exposureTime / 1000)

        pyzwoasi.stopExposure(cameraIndex)
        status = pyzwoasi.getExpStatus(cameraIndex)
        print("Exposure over. Status:", status.name)

        # Getting the image data after exposure
        if imageType == 0 or imageType == 3:   # 0 = ASI_IMG_RAW8, 3 = ASI_IMG_Y8
            bytesBerPixel = 1
        elif imageType == 2:                   # 2 = ASI_IMG_RAW16
            bytesBerPixel = 2
        elif imageType == 1:                   # 1 = ASI_IMG_RGB24
            bytesBerPixel = 3

        bufferSize = wd * ht * bytesBerPixel
        imageData = pyzwoasi.getDataAfterExp(cameraIndex, bufferSize)

        # Printing image
        shape = [ht, wd]
        if imageType == 0 or imageType == 3: # 0 = ASI_IMG_RAW8 and 3 = ASI_IMG_Y8
            img = np.frombuffer(imageData, dtype=np.uint8)
        elif imageType == 2:                 # 2 = ASI_IMG_RAW16
            img = np.frombuffer(imageData, dtype=np.uint16)
        elif imageType == 1:                 # 1 = ASI_IMG_RGB24
            img = np.frombuffer(imageData, dtype=np.uint8)
            shape.append(3)
        else:
            raise ValueError('Unsupported image type')
        img = img.reshape(shape)

        # Display image with matplotlib
        if imageType == 1:
            # RGB24: dtype uint8, shape (H, W, 3)
            plt.imshow(img)
        else:
            # Mono images: convert 16-bit to 8-bit for display if necessary
            if img.dtype == np.uint16:
                # simple downscale from 16-bit to 8-bit (keep top 8 bits)
                display_img = (img >> 8).astype(np.uint8)
            else:
                display_img = img
            plt.imshow(display_img, cmap='gray', interpolation='nearest')
        plt.axis('off')
        plt.show()

        # Always checking dropped frames before ending capture
        droppedFrames = pyzwoasi.getDroppedFrames(cameraIndex)
        if droppedFrames > 0:
            print(f"Dropped frames: {droppedFrames}")

        # Camera will be closed after use
        pyzwoasi.closeCamera(cameraIndex)