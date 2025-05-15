from multiprocessing import Value
import ctypes, os, tempfile, unittest

from pyzwoasi.pyzwoasi import CameraInfo, ControlCaps, ID
from pyzwoasi.pyzwoasi import cameraCheck, closeCamera, disableDarkSubtract, enableDarkSubtract, getCameraMode, getCameraProperty, getCameraPropertyByID, getControlCaps, getControlValue, getDroppedFrames, getID, getNumOfConnectedCameras, getNumOfControls, getProductIDs, getROIFormat, getSDKVersion, getSerialNumber, getStartPos, getVideoData, initCamera, openCamera, pulseGuideOn, pulseGuideOff, sendSoftTrigger, setCameraMode, setControlValue, setID, setROIFormat, setStartPos, startExposure, startVideoCapture, stopExposure, stopVideoCapture

class TestASICamera2(unittest.TestCase):
        def test_getNumOfConnectedCameras(self):
            numCameras = getNumOfConnectedCameras()
            self.assertIsInstance(numCameras, int)
            self.assertGreaterEqual(numCameras, 0)

        def test_getProductIDs(self):
            productIDs = getProductIDs()
            self.assertIsInstance(productIDs, list)
            for productID in productIDs:
                self.assertIsInstance(productID, int)
                self.assertGreaterEqual(productID, 0)

        def test_cameraCheck(self):
            vendorID = 0x03C3 # ID number of ZWO manufacturer
            productIDs = getProductIDs()
            for productID in productIDs:
                isASICamera = cameraCheck(vendorID, productID)
                self.assertIsInstance(isASICamera, bool)
                self.assertIn(isASICamera, [True, False])
        
        def test_getCameraProperty(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                self.assertIsInstance(cameraInfo                     , CameraInfo)
                self.assertIsInstance(cameraInfo.Name                , bytes)
                self.assertIsInstance(cameraInfo.CameraID            , int)
                self.assertIsInstance(cameraInfo.MaxHeight           , int)
                self.assertIsInstance(cameraInfo.MaxWidth            , int)
                self.assertIsInstance(cameraInfo.IsColorCam          , int)
                self.assertIsInstance(cameraInfo.BayerPattern        , int)
                self.assertIsInstance(cameraInfo.SupportedBins       , ctypes.Array)
                self.assertIsInstance(cameraInfo.SupportedVideoFormat, ctypes.Array)
                self.assertIsInstance(cameraInfo.PixelSize           , float)
                self.assertIsInstance(cameraInfo.MechanicalShutter   , int)
                self.assertIsInstance(cameraInfo.ST4Port             , int)
                self.assertIsInstance(cameraInfo.IsCoolerCam         , int)
                self.assertIsInstance(cameraInfo.IsUSB3Host          , int)
                self.assertIsInstance(cameraInfo.IsUSB3Camera        , int)
                self.assertIsInstance(cameraInfo.ElecPerADU          , float)
                self.assertIsInstance(cameraInfo.BitDepth            , int)
                self.assertIsInstance(cameraInfo.IsTriggerCam        , int)
                self.assertIsInstance(cameraInfo.Unused              , bytes)

        def test_getCameraPropertyByID(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                try:
                    cameraInfo = getCameraProperty(i)
                    openCamera(cameraInfo.CameraID) # Camera must be opened to call by ID
                    cameraInfo = getCameraPropertyByID(cameraInfo.CameraID)
                    self.assertIsInstance(cameraInfo                     , CameraInfo)
                    self.assertIsInstance(cameraInfo.Name                , bytes)
                    self.assertIsInstance(cameraInfo.CameraID            , int)
                    self.assertIsInstance(cameraInfo.MaxHeight           , int)
                    self.assertIsInstance(cameraInfo.MaxWidth            , int)
                    self.assertIsInstance(cameraInfo.IsColorCam          , int)
                    self.assertIsInstance(cameraInfo.BayerPattern        , int)
                    self.assertIsInstance(cameraInfo.SupportedBins       , ctypes.Array)
                    self.assertIsInstance(cameraInfo.SupportedVideoFormat, ctypes.Array)
                    self.assertIsInstance(cameraInfo.PixelSize           , float)
                    self.assertIsInstance(cameraInfo.MechanicalShutter   , int)
                    self.assertIsInstance(cameraInfo.ST4Port             , int)
                    self.assertIsInstance(cameraInfo.IsCoolerCam         , int)
                    self.assertIsInstance(cameraInfo.IsUSB3Host          , int)
                    self.assertIsInstance(cameraInfo.IsUSB3Camera        , int)
                    self.assertIsInstance(cameraInfo.ElecPerADU          , float)
                    self.assertIsInstance(cameraInfo.BitDepth            , int)
                    self.assertIsInstance(cameraInfo.IsTriggerCam        , int)
                    self.assertIsInstance(cameraInfo.Unused             , bytes)
                except ValueError as e:
                    self.fail(f"getCameraPropertyByID raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_openCamera(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                except ValueError as e:
                    self.fail(f"openCamera raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_initCamera(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                except ValueError as e:
                    self.fail(f"initCamera raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_closeCamera(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    closeCamera(cameraInfo.CameraID)
                except ValueError as e:
                    self.fail(f"closeCamera raised error unexpectedly: {e}")

        def test_getNumOfControls(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    numOfControls = getNumOfControls(cameraInfo.CameraID)
                    self.assertIsInstance(numOfControls, int)
                    self.assertGreaterEqual(numOfControls, 0)
                except ValueError as e:
                    self.fail(f"getNumOfControls raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_getControlCaps(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    for controlIndex in range(getNumOfControls(cameraInfo.CameraID)):
                        controlCaps = getControlCaps(cameraInfo.CameraID, controlIndex)
                        self.assertIsInstance(controlCaps, ControlCaps)
                except ValueError as e:
                    self.fail(f"getControlCaps raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_getSDKVersion(self):
            sdkVersion = getSDKVersion()
            self.assertIsInstance(sdkVersion, str)
            self.assertEqual(sdkVersion, "1, 37, 0, 0") # Current version of the SDK

        def test_sendSoftTrigger(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
            
                    sendSoftTrigger(cameraInfo.CameraID, True)  # Test sending start trigger
                    sendSoftTrigger(cameraInfo.CameraID, False) # Test sending stop trigger
            
                except ValueError as e:
                    self.fail(f"sendSoftTrigger raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_getSerialNumber(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    serialNumber = getSerialNumber(cameraInfo.CameraID)
                    self.assertIsInstance(serialNumber, str)
                    self.assertEqual(len(serialNumber), 16)
                    self.assertRegex(serialNumber, r'^[0-9A-F]{16}$')
                except ValueError as e:
                    self.fail(f"getSerialNumber raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_getControlValue(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    numOfControls = getNumOfControls(cameraInfo.CameraID)
                    for controlIndex in range(numOfControls):
                        controlCaps = getControlCaps(cameraInfo.CameraID, controlIndex)
                        controlType = controlCaps.ControlType
                        value, auto = getControlValue(cameraInfo.CameraID, controlType)
                        self.assertIsInstance(value, int)
                        self.assertIsInstance(auto, bool)
                except ValueError as e:
                    self.fail(f"getControlValue raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_setControlValue(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    numOfControls = getNumOfControls(cameraInfo.CameraID)
                    for controlIndex in range(numOfControls):
                        controlCaps = getControlCaps(cameraInfo.CameraID, controlIndex)
                        
                        if controlCaps.IsWritable: # Testing only for writable controls
                            controlType = controlCaps.ControlType
                            originalValue, originalAuto = getControlValue(cameraInfo.CameraID, controlType)
                            newValue = int((originalValue + controlCaps.MaxValue) / 2)
                            setControlValue(cameraInfo.CameraID, controlType, newValue, originalAuto)
                            value, auto = getControlValue(cameraInfo.CameraID, controlType)
                            self.assertEqual(value, newValue)
                            self.assertEqual(auto, originalAuto)
                            # Reset to original value
                            setControlValue(cameraInfo.CameraID, controlType, originalValue, originalAuto)

                except ValueError as e:
                    self.fail(f"setControlValue raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_getROIFormat(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    width, height, binning, imgType = getROIFormat(cameraInfo.CameraID)
                    self.assertIsInstance(width, int)
                    self.assertGreaterEqual(width, 0)
                    self.assertIsInstance(height, int)
                    self.assertGreaterEqual(height, 0)
                    self.assertIsInstance(binning, int)
                    self.assertIn(binning, [1, 2])
                    self.assertIsInstance(imgType, int)
                    self.assertGreaterEqual(imgType, -1)
                    self.assertLessEqual(imgType, 3)
                except ValueError as e:
                    self.fail(f"getROIFormat raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)
        
        def test_setROIFormat(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    originalWidth, originalHeight, originalBinning, originalImgType = getROIFormat(cameraInfo.CameraID)
                    
                    # Test setting new ROI format
                    newWidth   = 640 if originalWidth   >= 640 else originalWidth
                    newHeight  = 480 if originalHeight  >= 480 else originalHeight
                    newBinning = 1   if originalBinning == 2   else 2
                    newImgType = 0   if originalImgType != 0   else 1
                    
                    setROIFormat(cameraInfo.CameraID, newWidth, newHeight, newBinning, newImgType)
                    width, height, binning, imgType = getROIFormat(cameraInfo.CameraID)
                    
                    self.assertEqual(width, newWidth)
                    self.assertEqual(height, newHeight)
                    self.assertEqual(binning, newBinning)
                    self.assertEqual(imgType, newImgType)
                    
                    # Reset to original ROI format
                    setROIFormat(cameraInfo.CameraID, originalWidth, originalHeight, originalBinning, originalImgType)
                except ValueError as e:
                    self.fail(f"setROIFormat raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_getStartPos(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    startX, startY = getStartPos(cameraInfo.CameraID)
                    self.assertIsInstance(startX, int)
                    self.assertIsInstance(startY, int)
                    self.assertGreaterEqual(startX, 0)
                    self.assertGreaterEqual(startY, 0)
                except ValueError as e:
                    self.fail(f"getStartPos raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)
        
        def test_setStartPos(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    originalStartX, originalStartY = getStartPos(cameraInfo.CameraID)
                    width, height, binning, imgType = getROIFormat(cameraInfo.CameraID)
                    
                    # Test setting new start position
                    newStartX = 0
                    newStartY = 0

                    # We should avoid to be out of bounds
                    if (originalStartX == newStartX) and (originalStartY == newStartY):
                        newStartX = int((originalStartX + cameraInfo.MaxWidth - width) / 2)
                        newStartY = int((originalStartY + cameraInfo.MaxHeight - height) / 2)
                    else:
                        continue

                    setStartPos(cameraInfo.CameraID, newStartX, newStartY)
                    startX, startY = getStartPos(cameraInfo.CameraID)
                    
                    self.assertEqual(startX, newStartX)
                    self.assertEqual(startY, newStartY)
                    
                    # Reset to original start position
                    setStartPos(cameraInfo.CameraID, originalStartX, originalStartY)
                except ValueError as e:
                    self.fail(f"setStartPos raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_getDroppedFrames(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    droppedFrames = getDroppedFrames(cameraInfo.CameraID)
                    self.assertIsInstance(droppedFrames, int)
                    self.assertGreaterEqual(droppedFrames, 0)
                except ValueError as e:
                    self.fail(f"getDroppedFrames raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_darkSubstract(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)

                    # Create a temporary BMP file with RGB8 raw format and camera dimensions
                    width, height, binning, imgType = getROIFormat(cameraInfo.CameraID)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".bmp") as tempBmp:
                        bmpHeader  = b'BM' + (54 + width * height * 3).to_bytes(4, 'little') + b'\x00\x00\x00\x00' + b'\x36\x00\x00\x00' + b'\x28\x00\x00\x00'
                        bmpHeader += width.to_bytes(4, 'little') + height.to_bytes(4, 'little') + b'\x01\x00\x18\x00' + b'\x00\x00\x00\x00' + (width * height * 3).to_bytes(4, 'little')
                        bmpHeader += b'\x13\x0B\x00\x00' + b'\x13\x0B\x00\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00'
                        tempBmp.write(bmpHeader)
                        tempBmp.write(b'\x00' * (width * height * 3))
                        tempBmpPath = tempBmp.name

                    enableDarkSubtract(cameraInfo.CameraID, tempBmpPath)
                    disableDarkSubtract(cameraInfo.CameraID)

                except ValueError as e:
                    self.fail(f"test_DarkSubtract raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)
                    if os.path.exists(tempBmpPath):
                        os.remove(tempBmpPath)

        def test_startVideoCapture(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    startVideoCapture(cameraInfo.CameraID)
                except ValueError as e:
                    self.fail(f"startVideoCapture raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_stopVideoCapture(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    startVideoCapture(cameraInfo.CameraID)
                    stopVideoCapture(cameraInfo.CameraID)
                except ValueError as e:
                    self.fail(f"stopVideoCapture raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_getVideoData(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    startVideoCapture(cameraInfo.CameraID)
            
                    width, height, binning, imgType = getROIFormat(cameraInfo.CameraID)
                    bufferSize = width * height * 3 # Assuming RGB24 format for testing
            
                    maxAttempts = 1000 # Avoiding endless loop
                    for attempt in range(maxAttempts):
                        try:
                            # Multiple attempts are needed to get the video data
                            buffer = getVideoData(cameraInfo.CameraID, bufferSize, 1)
                            self.assertIsInstance(buffer, bytes)
                            self.assertEqual(len(buffer), bufferSize)
                            break # Exiting the loop if successful
                        except ValueError as e:
                            if attempt >= maxAttempts:
                                self.fail(f"getVideoData raised error after {maxAttempts} attempts: {e}")
                            else:
                                # Retrying
                                continue
            
                    self.assertIsInstance(buffer, bytes)
                    self.assertEqual(len(buffer), bufferSize)
            
                except ValueError as e:
                    self.fail(f"getVideoData raised error unexpectedly: {e}")
                finally:
                    stopVideoCapture(cameraInfo.CameraID)
                    closeCamera(cameraInfo.CameraID)

        def test_startStopExposure(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                
                    try: # Test start exposure
                        startExposure(cameraInfo.CameraID, False)
                    except ValueError as e:
                        self.fail(f"startExposure raised error unexpectedly: {e}")
                
                    try: # Test stop exposure
                        stopExposure(cameraInfo.CameraID)
                    except ValueError as e:
                        self.fail(f"stopExposure raised error unexpectedly: {e}")

                except ValueError as e:
                    self.fail(f"test_startStopExposure raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)

        def test_getAndSetID(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)

                try: # Test getID
                    originalID = getID(cameraInfo.CameraID)
                except ValueError as e:
                    self.fail(f"getID raised error unexpectedly: {e}")
                else:
                    newID = ID((ctypes.c_ubyte * 8)(1, 2, 3, 4, 5, 6, 7, 8))
                    try: # Test setID
                        openCamera(cameraInfo.CameraID)
                        initCamera(cameraInfo.CameraID)
                        setID(cameraInfo.CameraID, newID)
                        self.assertNotEqual(getID(cameraInfo.CameraID), originalID)
                    except ValueError as e:
                        self.fail(f"setID raised error unexpectedly: {e}")
                    finally:
                        # Restore the original ID to avoid side effects
                        setID(cameraInfo.CameraID, originalID)
                        self.assertEqual(getID(cameraInfo.CameraID), originalID)
                        closeCamera(cameraInfo.CameraID)

        def test_pulseGuide(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)

                # Only test cameras with ST4 port
                if not cameraInfo.ST4Port:
                    continue

                openCamera(cameraInfo.CameraID)
                initCamera(cameraInfo.CameraID)
                for direction in range(4):
                    try: # Test pulseGuideOn
                        pulseGuideOn(cameraInfo.CameraID, direction)
                    except ValueError as e:
                        self.fail(f"pulseGuideOn raised error unexpectedly: {e}")
                    else:
                        try: # Test pulseGuideOff
                            pulseGuideOff(cameraInfo.CameraID)
                        except ValueError as e:
                            self.fail(f"pulseGuideOff raised error unexpectedly: {e}")

                closeCamera(cameraInfo.CameraID)
        
        def test_getAndSetCameraMode(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)

                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                    for newCameraMode in range(7): # 7 camera modes are available
                        try: # Test setCameraMode
                            setCameraMode(cameraInfo.CameraID, newCameraMode)
                        except ValueError as e:
                            self.fail(f"setCameraMode raised error unexpectedly: {e}")
                        else: # Test getCameraMode
                            try:
                                cameraMode = getCameraMode(cameraInfo.CameraID)
                                self.assertEqual(cameraMode, newCameraMode)
                            except ValueError as e:
                                self.fail(f"getCameraMode raised error unexpectedly: {e}")
                
                except ValueError as e:
                    self.fail(f"test_getAndSetCameraMode raised error unexpectedly: {e}")
                finally:
                    closeCamera(cameraInfo.CameraID)
                    

if __name__ == '__main__':
    unittest.main()
