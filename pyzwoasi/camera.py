import ctypes
import numpy as np, time

from . import pyzwoasi
from .pyzwoasi import ASIExposureStatus, ASIError, ASIImageType

class ZWOCamera:
    def __init__(self, cameraIndex):
        self._cameraIndex = cameraIndex

        # Opening and initializing camera
        pyzwoasi.openCamera(self._cameraIndex)
        pyzwoasi.initCamera(self._cameraIndex)

        self._isClosed = False

        # Let's get some information about the chosen camera
        cameraInfo = pyzwoasi.getCameraProperty(self._cameraIndex)

        self._name                 = cameraInfo.Name.decode('utf-8')
        self._cameraID             = cameraInfo.CameraID
        self._maxHeight            = cameraInfo.MaxHeight
        self._maxWidth             = cameraInfo.MaxWidth
        self._isColorCam           = bool(cameraInfo.IsColorCam)
        self._bayerPattern         = cameraInfo.BayerPattern
        self._supportedBins        = list(cameraInfo.SupportedBins)
        self._supportedVideoFormat = cameraInfo.SupportedVideoFormat
        self._pixelSize            = cameraInfo.PixelSize
        self._mechanicalShutter    = bool(cameraInfo.MechanicalShutter)
        self._st4port              = bool(cameraInfo.ST4Port)
        self._isCoolerCam          = bool(cameraInfo.IsCoolerCam)
        self._isUSB3Host           = bool(cameraInfo.IsUSB3Host)
        self._isUSB3Camera         = bool(cameraInfo.IsUSB3Camera)
        self._elecPerADU           = cameraInfo.ElecPerADU
        self._bitDepth             = cameraInfo.BitDepth
        self._isTriggerCam         = bool(cameraInfo.IsTriggerCam)

        # Read and save all camera controls for the getters/setters.
        numOfControls = pyzwoasi.getNumOfControls(self._cameraIndex)
        self._dictControlID = {}
        self._dictControlIDMin = {}
        self._dictControlIDMax = {}
        for controlIndex in range(numOfControls):
            controlCaps = pyzwoasi.getControlCaps(self._cameraIndex, controlIndex)
            controlName = controlCaps.Name.decode('utf-8')
            self._dictControlID[controlName] = controlCaps.ControlType
            self._dictControlIDMin[controlName] = controlCaps.MinValue
            self._dictControlIDMax[controlName] = controlCaps.MaxValue

            # Initialize both the exposure time and image type with default values
            if controlName == "Exposure"  : self.exposure  = controlCaps.DefaultValue
            if controlName == "Image Type": self.imageType = controlCaps.DefaultValue

    @property
    def imageType(self):
        _, _, _, imageType = pyzwoasi.getROIFormat(self._cameraIndex)
        return   imageType

    @property
    def bufferSize(self):
        width, height, _, imageType = pyzwoasi.getROIFormat(self._cameraIndex)
        if   imageType == ASIImageType.ASI_IMG_RAW8 or imageType == ASIImageType.ASI_IMG_Y8:
            bytesPerPixel = 1
        elif imageType == ASIImageType.ASI_IMG_RAW16:
            bytesPerPixel = 2
        elif imageType == ASIImageType.ASI_IMG_RGB24:
            bytesPerPixel = 3
        else:
            raise ValueError('Unsupported image type')

        return width * height * bytesPerPixel

    @imageType.setter
    def imageType(self, imageType):
        wd, ht, binning, _ = pyzwoasi.getROIFormat(self._cameraIndex)
        pyzwoasi.setROIFormat(self._cameraIndex, wd, ht, binning, imageType)

    @property
    def exposure(self):
        try:
            return pyzwoasi.getControlValue(self._cameraIndex, self._dictControlID["Exposure"])[0]
        except KeyError:
            print("Exposure control not available for this camera.")
            return None

    @exposure.setter
    def exposure(self, exposureTime_us):
        if self._dictControlIDMin["Exposure"] <= exposureTime_us <= self._dictControlIDMax["Exposure"]:
            try:
                pyzwoasi.setControlValue(self._cameraIndex, self._dictControlID["Exposure"], exposureTime_us, auto=False)
            except KeyError:
                print("Exposure control not available for this camera.")
        else:
            raise ValueError(f"Exposure time out of range. Selected value is {exposureTime_us} and range "
                       f"is [{self._dictControlIDMin["Exposure"]}, {self._dictControlIDMax["Exposure"]}].")

    @property
    def exposureLimits(self):
        try:
            return (self._dictControlIDMin["Exposure"], self._dictControlIDMax["Exposure"])
        except KeyError:
            print("Exposure control not available for this camera.")
            return (None, None)

    @property
    def gain(self):
        try:
            return pyzwoasi.getControlValue(self._cameraIndex, self._dictControlID["Gain"])[0]
        except KeyError:
            print("Gain control not available for this camera.")
            return None

    @gain.setter
    def gain(self, gainValue):
        if self._dictControlIDMin["Gain"] <= gainValue <= self._dictControlIDMax["Gain"]:
            try:
                pyzwoasi.setControlValue(self._cameraIndex, self._dictControlID["Gain"], gainValue, auto=False)
            except KeyError:
                print("Gain control not available for this camera.")
        else:
            raise ValueError(f"Gain value out of range. Selected value is {gainValue} and range "
                      f"is [{self._dictControlIDMin["Gain"]}, {self._dictControlIDMax["Gain"]}].")

    @property
    def softwareBinning(self):
        _, _, binning, _ = pyzwoasi.getROIFormat(self._cameraIndex)
        return binning

    @softwareBinning.setter
    def softwareBinning(self, binning):
        if binning not in self._supportedBins:
            raise ValueError(f"Binning value {binning} is not supported. Supported values are: {self._supportedBins}")

        width, height, _, imageType = pyzwoasi.getROIFormat(self._cameraIndex)
        pyzwoasi.setROIFormat(self._cameraIndex, int(width / binning), int(height / binning), binning, imageType)

    @property
    def hardwareBinning(self):
        try:
            return pyzwoasi.getControlValue(self._cameraIndex, self._dictControlID["HardwareBin"])[0]
        except KeyError:
            print("Hardware binning control not available for this camera.")
            return None

    @hardwareBinning.setter
    def hardwareBinning(self, hardwareBinningArg):
        if self._dictControlIDMin["HardwareBin"] <= hardwareBinningArg <= self._dictControlIDMax["HardwareBin"]:
            try:
                controlCaps = pyzwoasi.getControlCaps(self._cameraIndex, self._dictControlID["HardwareBin"])
                if controlCaps.IsWritable == False:
                    print("Hardware binning control not writable for this camera.")
                    return

                pyzwoasi.setControlValue(self._cameraIndex, self._dictControlID["HardwareBin"], hardwareBinningArg, auto=False)

            except KeyError:
                print("Hardware binning control not available for this camera.")
        else:
            raise ValueError(f"Hardware binning value out of range. Selected value is {hardwareBinningArg} and range "
                             f"is [{self._dictControlIDMin["HardwareBin"]}, {self._dictControlIDMax["HardwareBin"]}].")

    @property
    def hardwareBinningLimits(self):
        try:
            return (self._dictControlIDMin["HardwareBin"], self._dictControlIDMax["HardwareBin"])
        except KeyError:
            print("Hardware binning control not available for this camera.")
            return (None, None)

    @property
    def roi(self):
        width, height, binning, imageType = pyzwoasi.getROIFormat(self._cameraIndex)
        return (width, height, binning, imageType)

    def setROI(self, width, height, binning=None, imageType=None):
        if binning   is None: binning   = self.softwareBinning
        if imageType is None: imageType = self.imageType

        if width  % 8 != 0:
            raise ValueError("Width must be a multiple of 8")
        if height % 2 != 0:
            raise ValueError("Height must be a multiple of 2")

        pyzwoasi.setROIFormat(self._cameraIndex, width, height, binning, imageType)

    @property
    def highSpeedMode(self):
        try:
            return pyzwoasi.getControlValue(self._cameraIndex, self._dictControlID["HighSpeedMode"])[0]
        except KeyError:
            print("High Speed Mode control not available for this camera.")
            return None

    @highSpeedMode.setter
    def highSpeedMode(self, mode):
        try:
            pyzwoasi.setControlValue(self._cameraIndex, self._dictControlID["HighSpeedMode"], mode, auto=False)
        except KeyError:
            print("High Speed Mode control not available for this camera.")

    @property
    def bandwidth(self):
        try:
            return pyzwoasi.getControlValue(self._cameraIndex, self._dictControlID["BandWidth"])[0]
        except KeyError:
            print("Bandwidth control not available for this camera.")
            return None

    @bandwidth.setter
    def bandwidth(self, bandwidthValue):
        try:
            controlCaps = pyzwoasi.getControlCaps(self._cameraIndex, self._dictControlID["BandWidth"])
            if controlCaps.IsWritable == False:
                print("Bandwidth control not writable for this camera.")
                return

            if self._dictControlIDMin["BandWidth"] <= bandwidthValue <= self._dictControlIDMax["BandWidth"]:
                    pyzwoasi.setControlValue(self._cameraIndex, self._dictControlID["BandWidth"], bandwidthValue, auto=False)
            else:
                raise ValueError(f"Bandwidth value out of range. Selected value is {bandwidthValue} and range "
                          f"is [{self._dictControlIDMin["BandWidth"]}, {self._dictControlIDMax["BandWidth"]}].")
        except KeyError:
            print("Bandwidth control not available for this camera.")

    """
    @brief Take a single picture with the camera.

    The following arguments are optional, and if not provided,
    the current settings will be used. If provided, they will
    update the camera settings before starting the capture.

    @param exposureTime_us : exposure time in microseconds
    @param imageType       : image type. Can be either int
                             or ASIImageType.
      - ASIImageType.ASI_IMG_RAW8  = 0
      - ASIImageType.ASI_IMG_RGB24 = 1
      - ASIImageType.ASI_IMG_RAW16 = 2
      - ASIImageType.ASI_IMG_Y8    = 3
    """
    def shot(self, exposureTime_us = None, imageType = None):
        # Setting exposure and image type
        if exposureTime_us is not None:
            self.exposure  = exposureTime_us
        
        if imageType is not None:
            self.imageType = imageType

        # Let's start exposure
        pyzwoasi.startExposure(self._cameraIndex, True)
        time.sleep(self.exposure / 1_000_000) # seconds 

        failedRuns = 0
        while  pyzwoasi.getExpStatus(self._cameraIndex) != ASIExposureStatus.ASI_EXP_SUCCESS:
            if pyzwoasi.getExpStatus(self._cameraIndex) == ASIExposureStatus.ASI_EXP_WORKING:
                pass
            elif pyzwoasi.getExpStatus(self._cameraIndex) == ASIExposureStatus.ASI_EXP_FAILED:
                if failedRuns >= 3:
                    print("Exposure failed 3 times. Aborting...")
                    exit()

                # Exposure has failed (that may happen for various reasons)
                # Let's restart the process and watch if it happens again.
                failedRuns += 1

                pyzwoasi.stopExposure(self._cameraIndex)

                pyzwoasi.startExposure(self._cameraIndex, True)
                time.sleep(self.exposure / 1_000_000) # seconds  

        # Always check dropped frames before ending the capture
        droppedFrames = pyzwoasi.getDroppedFrames(self._cameraIndex)
        if droppedFrames > 0:
            print(f"Dropped frames: {droppedFrames}")

        # Stopping exposure and start conversion
        pyzwoasi.stopExposure(self._cameraIndex)

        width, height, _, _ = pyzwoasi.getROIFormat(self._cameraIndex)
        if   self.imageType == ASIImageType.ASI_IMG_RAW8 or self.imageType == ASIImageType.ASI_IMG_Y8:
            bytesPerPixel = 1
        elif self.imageType == ASIImageType.ASI_IMG_RAW16:
            bytesPerPixel = 2
        elif self.imageType == ASIImageType.ASI_IMG_RGB24:
            bytesPerPixel = 3
        else:
            raise ValueError('Unsupported image type')
        
        bufferSize = width * height * bytesPerPixel
        imageData = pyzwoasi.getDataAfterExp(self._cameraIndex, bufferSize)

        shape = [height, width]
        if   self.imageType == ASIImageType.ASI_IMG_RAW8 or self.imageType == ASIImageType.ASI_IMG_Y8:
            img = np.frombuffer(imageData, dtype=np.uint8)
        elif self.imageType == ASIImageType.ASI_IMG_RAW16:
            img = np.frombuffer(imageData, dtype=np.uint16)
        elif self.imageType == ASIImageType.ASI_IMG_RGB24:
            img = np.frombuffer(imageData, dtype=np.uint8)
            shape.append(3)
        
        img  = img.reshape(shape)
        return img

    def startVideoCapture(self):
        pyzwoasi.startVideoCapture(self._cameraIndex)

    def stopVideoCapture(self):
        pyzwoasi.stopVideoCapture(self._cameraIndex)

    """
    Live view with OpenCV interface. Press 'q' key to quit.
    Gives the ability to the user to change gain, exposure,
    and ROI on the fly.
    """
    def liveView(self):
        # Main frame
        import cv2
        windowName = "Live Camera Capture"
        cv2.namedWindow(windowName)
        cv2.createTrackbar("Exposure" , windowName, 0  , 100, lambda x: None)
        cv2.createTrackbar("Gain"     , windowName, 0  , 100, lambda x: None)
        cv2.createTrackbar("ROI"      , windowName, 100, 100, lambda x: None)

        # It is useless to go above 1 second exposure for live view testing
        maximumExposureLimit = np.minimum(self.exposureLimits[1], 1000)

        # Software binning does not change latence or FPS in live view
        self.softwareBinning = 1

        previousTime = time.time()
        self.startVideoCapture()
        while True:
            # Updating camera exposure
            exposureTime_percentage = cv2.getTrackbarPos("Exposure", windowName)
            exposureTime_us = (self.exposureLimits[0] + (maximumExposureLimit - self.exposureLimits[0]) * exposureTime_percentage / 100)
            self.exposure = int(exposureTime_us)

            # Updating camera gain
            gain_percentage = cv2.getTrackbarPos("Gain", windowName)
            cameraGainMin, cameraGainMax = self._dictControlIDMin["Gain"], self._dictControlIDMax["Gain"]
            gain = int(cameraGainMin + (cameraGainMax - cameraGainMin) * gain_percentage / 100)
            self.gain = gain

            roiPercentage = np.maximum(1, cv2.getTrackbarPos("ROI", windowName))

            width  = (int(self._maxWidth  * (roiPercentage / 100) / self.softwareBinning) // 8) * 8
            height = (int(self._maxHeight * (roiPercentage / 100) / self.softwareBinning) // 2) * 2

            widthBeforeUpdate, heighBeforeUpdate, _, _ = pyzwoasi.getROIFormat(self._cameraIndex)

            if (width != widthBeforeUpdate) or (height != heighBeforeUpdate):
                self.stopVideoCapture()
                self.setROI(width, height)
                self.startVideoCapture()

            # Getting image from camera and displaying it
            try:
                # As given by the manufacturer ZWO, the refresh rate should
                # be at least twice the exposure time plus 500 microseconds
                refreshRate = int(2 * exposureTime_us + 500)
                frame = pyzwoasi.getVideoData(self._cameraIndex, self.bufferSize, refreshRate)
            except ASIError as e:
                print(f"Error getting video data: {e}")
                continue
                
            img = np.frombuffer(frame, dtype=np.uint8).reshape(height, width, 1)

            target_height = 480
            scale = target_height / img.shape[0]
            target_width = int(img.shape[1] * scale)

            small = cv2.resize(img, (target_width, target_height))

            # Computing and displaying FPS
            currentTime = time.time()
            fps = 1 / (currentTime - previousTime)
            previousTime = currentTime
            cv2.putText(small, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow(windowName, small)

            # Let's close the window if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        self.stopVideoCapture()
        cv2.destroyAllWindows()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    # Camera should always be closed after use
    # in order to free all resources. Usually,
    # it will be called automatically.
    def close(self):
        if not self._isClosed:
            pyzwoasi.closeCamera(self._cameraIndex)
            self._isClosed = True

    def __exit__(self, exceptionType, exceptionValue, traceback):
        self.close()

if __name__ == "__main__":
    numOfConnectedCameras = pyzwoasi.getNumOfConnectedCameras()
    if (numOfConnectedCameras == 0):
        print("No camera connected")
        exit()

    for cameraIndex in range(numOfConnectedCameras):
        with ZWOCamera(cameraIndex) as camera:
            camera.liveView()