import unittest

from src.main import CameraInfo, ControlCaps
from src.main import cameraCheck, closeCamera, getCameraProperty, getCameraPropertyByID, getControlCaps, getNumOfConnectedCameras, getNumOfControls, getProductIDs, getSDKVersion, getSerialNumber, initCamera, openCamera

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
                self.assertIsInstance(cameraInfo.SupportedBins       , (list, tuple))
                self.assertIsInstance(cameraInfo.SupportedVideoFormat, (list, tuple))
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
            productIDs = getProductIDs()
            for productID in productIDs:
                cameraInfo = getCameraPropertyByID(productID)
                self.assertIsInstance(cameraInfo                     , CameraInfo)
                self.assertIsInstance(cameraInfo.Name                , bytes)
                self.assertIsInstance(cameraInfo.CameraID            , int)
                self.assertIsInstance(cameraInfo.MaxHeight           , int)
                self.assertIsInstance(cameraInfo.MaxWidth            , int)
                self.assertIsInstance(cameraInfo.IsColorCam          , int)
                self.assertIsInstance(cameraInfo.BayerPattern        , int)
                self.assertIsInstance(cameraInfo.SupportedBins       , (list, tuple))
                self.assertIsInstance(cameraInfo.SupportedVideoFormat, (list, tuple))
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

        def test_openCamera(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                except ValueError as e:
                    self.fail(f"openCamera raised error unexpectedly: {e}")

        def test_initCamera(self):
            numCameras = getNumOfConnectedCameras()
            for i in range(numCameras):
                cameraInfo = getCameraProperty(i)
                try:
                    openCamera(cameraInfo.CameraID)
                    initCamera(cameraInfo.CameraID)
                except ValueError as e:
                    self.fail(f"initCamera raised error unexpectedly: {e}")

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
                    numOfControls = getNumOfControls(cameraInfo.cameraID)
                    self.assertIsInstance(numOfControls, int)
                    self.assertGreaterEqual(numOfControls, 0)
                except ValueError as e:
                    self.fail(f"getNumOfControls raised error unexpectedly: {e}")

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

        def test_getSDKVersion(self):
            sdkVersion = getSDKVersion()
            self.assertIsInstance(sdkVersion, str)
            self.assertEqual(sdkVersion, "1, 37, 0, 0") # Current version of the SDK

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


if __name__ == '__main__':
    unittest.main()
