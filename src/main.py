import ctypes
import platform
import os


# Chosing and reading correct dll
arch = platform.architecture()[0]
dllPath = os.path.join(os.path.dirname(__file__), 'lib', 'x64' if arch == '64bit' else 'x86', 'ASICamera2.dll')
lib = ctypes.cdll.LoadLibrary(dllPath)


# Defining struct _ASI_CAMERA_INFO
class CameraInfo(ctypes.Structure):
    _fields_ = [
        ("Name"                , ctypes.c_char * 64), # The name of the camera
        ("CameraID"            , ctypes.c_int),       # Used to control everything of the camera in other functions. Starts from 0
        ("MaxHeight"           , ctypes.c_long),      # Max height of the camera
        ("MaxWidth"            , ctypes.c_long),      # Max width of the camera
        
        ("IsColorCam"          , ctypes.c_int),
        ("BayerPattern"        , ctypes.c_int),
        
        ("SupportedBins"       , ctypes.c_int * 16),  # 1 is supported by every camera, 0 is end of supported binning method
        ("SupportedVideoFormat", ctypes.c_int * 8),   # Contents with the support output format type.IMG_END is the end of supported video format
        ("PixelSize"           , ctypes.c_double),    # Pixel size of the camera, unit is um.
        ("MechanicalShutter"   , ctypes.c_int),
        ("ST4Port"             , ctypes.c_int),
        ("IsCoolerCam"         , ctypes.c_int),
        ("IsUSB3Host"          , ctypes.c_int),
        ("IsUSB3Camera"        , ctypes.c_int),
        ("ElecPerADU"          , ctypes.c_float),
        ("BitDepth"            , ctypes.c_int),
        ("IsTriggerCam"        , ctypes.c_int),
        ("Unused"              , ctypes.c_char * 16)
    ]

# Defining struct _ASI_CONTROL_CAPS
class ControlCaps(ctypes.Structure):
    _fields_ = [
        ("Name"           , ctypes.c_char * 64),  # Name of control (like Exposure, Gain, etc.)
        ("Description"    , ctypes.c_char * 128), # Description of this control
        ("MaxValue"       , ctypes.c_long),
        ("MinValue"       , ctypes.c_long),
        ("DefaultValue"   , ctypes.c_long),
        ("IsAutoSupported", ctypes.c_int),        # Support auto is 1, don't support 0
        ("IsWritable"     , ctypes.c_int),        # Some control like temperature can only be read by some cameras 
        ("ControlType"    , ctypes.c_int),        #  used to get value and set value of the control
        ("Unused"         , ctypes.c_char * 32)
    ]

# Defining ASI_ID typedef
class ID(ctypes.Structure):
    _fields_ = [
        ("ID", ctypes.c_ubyte * 8) # 8-byte array
    ]

# Defining ASI_SN typedef
class SN(ctypes.Structure):
    _fields_ = [
        ("SN", ctypes.c_ubyte * 8) # 8-byte array
    ]

# Defining int ASIGetNumOfConnectedCameras()
lib.ASIGetNumOfConnectedCameras.restype = ctypes.c_int
def getNumOfConnectedCameras():
    """
    @brief Gets number of connected ASI cameras

    @notes This should be the first API to be called

    @return Number of connected ASI cameras
    """
    return lib.ASIGetNumOfConnectedCameras()

# Defining int ASIGetProductIDs(int* pPIDs)
lib.ASIGetNumOfConnectedCameras.restype = ctypes.c_int
lib.ASIGetProductIDs.argtypes = [ctypes.POINTER(ctypes.c_int)]
def getProductIDs():
    """
    @brief Gets product IDs of connected ASI cameras

    @notes This API will be deprecated. Please use CameraCheck instead

    @return List of product IDs of connected ASI cameras
    """
    # Is called once to get the length of the array
    length = lib.ASIGetProductIDs(None)
    if length < 0:
        raise ValueError("Length of product IDs array is negative")
    if length == 0:
        return []

    # Creating table to contain IDs
    pPIDs = (ctypes.c_int * length)()
    lib.ASIGetProductIDs(pPIDs)

    # Converts table to Python list
    productIDs = list(pPIDs)
    if any(productID < 0 for productID in productIDs):
        raise ValueError("List of product IDs cannot contain negative numbers")

    return productIDs

# Defining ASI_BOOL ASICameraCheck(int iVID, int iPID)
lib.ASICameraCheck.restype = ctypes.c_bool
lib.ASICameraCheck.argtypes = [ctypes.c_int, ctypes.c_int]
def cameraCheck(vendorID, productID):
    """
    @brief Checks if the device is an ASI camera

    @param vendorID  Vendor ID of the device (0x03X3 for ASI cameras)
    @param productID Product ID of the device

    @return True if the device is an ASI camera, False otherwise
    """
    result = lib.ASICameraCheck(vendorID, productID)
    if result not in (0, 1):
        raise ValueError("Result of camera check is not a boolean")
    return result == 1

# Defining ASI_ERROR_CODE ASIGetCameraProperty(ASI_CAMERA_INFO *pASICameraInfo, int iCameraIndex)
lib.ASIGetCameraProperty.restype = ctypes.c_int
lib.ASIGetCameraProperty.argtypes = [ctypes.POINTER(CameraInfo), ctypes.c_int]
def getCameraProperty(cameraIndex):
    """
    @brief Gets information about the camera

    @note Can be done without opening the camera

    @param cameraIndex Index of the camera, 0 being the first

    @return Information about the camera, with type CameraInfo
    """
    cameraInfo = CameraInfo()
    errorCode = lib.ASIGetCameraProperty(cameraInfo, cameraIndex)
    if errorCode != 0:
        raise ValueError(f"Failed to get camera property. Error code: {errorCode}")
    return cameraInfo

# Defining ASI_ERROR_CODE ASIGetCameraPropertyByID(int iCameraID, ASI_CAMERA_INFO *pASICameraInfo)
lib.ASIGetCameraPropertyByID.restype = ctypes.c_int
lib.ASIGetCameraPropertyByID.argtypes = [ctypes.c_int, ctypes.POINTER(CameraInfo)]
def getCameraPropertyByID(cameraID):
    """
    @brief Gets information about the camera

    @note Camera needs to be open first

    @param cameraID ID of the camera

    @return Information about the camera, with type CameraInfo
    """
    cameraInfo = CameraInfo()
    errorCode = lib.ASIGetCameraPropertyByID(cameraID, cameraInfo)
    if errorCode != 0:  
           raise ValueError(f"Failed to get camera property by ID. Error code: {errorCode}")
    return cameraInfo

# Defining ASI_ERROR_CODE ASIOpenCamera(int iCameraID)
lib.ASIOpenCamera.restype = ctypes.c_int
lib.ASIOpenCamera.argtypes = [ctypes.c_int]
def openCamera(cameraID):
    """
    @brief Opens camera before any operation

    @param cameraID ID of the camera
    """
    errorCode = lib.ASIOpenCamera(cameraID)
    if errorCode != 0:
        raise ValueError(f"Failed to open camera. Error code: {errorCode}")

# Defining ASI_ERROR_CODE ASIInitCamera(int iCameraID)
lib.ASIInitCamera.restype = ctypes.c_int
lib.ASIInitCamera.argtypes = [ctypes.c_int]
def initCamera(cameraID):
    """
    @brief Initializes camera before any operation

    @note this may take some time to finish
    
    @param cameraID ID of the camera
    """
    errorCode = lib.ASIInitCamera(cameraID)
    if errorCode != 0:
        raise ValueError(f"Failed to initialize camera. Error code: {errorCode}")

# Defining ASI_ERROR_CODE ASICloseCamera(int iCameraID)
lib.ASICloseCamera.restype = ctypes.c_int
lib.ASICloseCamera.argtypes = [ctypes.c_int]
def closeCamera(cameraID):
    """
    @brief Closes camera to free all the resources
    
    @param cameraID ID of the camera
    """
    errorCode = lib.ASICloseCamera(cameraID)
    if errorCode != 0:
        raise ValueError(f"Failed to close camera. Error code: {errorCode}")

# Defining ASI_ERROR_CODE ASIGetNumOfControls(int iCameraID, int * piNumberOfControls)
lib.ASIGetNumOfControls.restype = ctypes.c_int
lib.ASIGetNumOfControls.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
def getNumOfControls(cameraID):
    """
    @brief Gets number of controls available for this camera

    @note The camera needs to be opened first

    @param cameraID can be obtained using getCameraProperty

    @return number of controls
    """
    pNumOfControls = (ctypes.c_int)() # Pointer used to numOfControls
    errorCode = lib.ASIGetNumOfControls(cameraID, pNumOfControls)
    if errorCode != 0:
        raise ValueError(f"Failed to get number of controls for cameraID {cameraID}. Error code: {errorCode}")
    if pNumOfControls.value < 0:
        raise ValueError(f"Number of controls of cameraID {cameraID} cannot be negative ({pNumOfControls})")
    return pNumOfControls.value

# Defining ASI_ERROR_CODE ASIGetControlCaps(int iCameraID, int iControlIndex, ASI_CONTROL_CAPS * pControlCaps)
lib.ASIGetControlCaps.restype = ctypes.c_int
lib.ASIGetControlCaps.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ControlCaps)]
def getControlCaps(cameraID, controlIndex):
    """
    @brief Gets controls property available for this camera

    @param cameraID     can be obtained using getCameraProperty
    @param controlIndex index of control, NOT control type

    @return Structure containing the property of the control
    """
    controlCaps = ControlCaps()
    errorCode = lib.ASIGetControlCaps(cameraID, controlIndex, controlCaps)
    if errorCode != 0:
        raise ValueError(f"Failed to get number of controls for cameraID {cameraID}. Error code: {errorCode}")
    return controlCaps

# Defining ASI_ERROR_CODE ASIGetControlValue(int iCameraID, ASI_CONTROL_TYPE ControlType, long *plValue, ASI_BOOL *pbAuto)
lib.ASIGetControlValue.restype = ctypes.c_int
lib.ASIGetControlValue.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_int)]
def getControlValue(cameraID, controlType):
    """
    @brief Gets the value of a specific control of the camera

    @param cameraID    ID of the camera
    @param controlType Type of the control to get the value of

    @return Tuple containing value of the control 
                             auto status
    """
    value      = ctypes.c_long()
    autoStatus = ctypes.c_int()
    errorCode = lib.ASIGetControlValue(cameraID, controlType, ctypes.byref(value), ctypes.byref(autoStatus))
    if errorCode != 0:
        raise ValueError(f"Failed to get control value for cameraID {cameraID}. Error code: {errorCode}")
    return value.value, autoStatus.value == 1

# Defining ASI_ERROR_CODE ASISetControlValue(int iCameraID, ASI_CONTROL_TYPE  ControlType, long lValue, ASI_BOOL bAuto)
lib.ASISetControlValue.restype = ctypes.c_int
lib.ASISetControlValue.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_long, ctypes.c_int]
def setControlValue(cameraID, controlType, value, auto):
    """
    @brief Sets the value of a specific control of the camera

    @note It will clamp the value to the minimum or the maximum if it is out of range

    @param cameraID    ID of the camera
    @param controlType Type of the control to set the value of
    @param value       Value to set for the control
    @param auto        Boolean indicating if the control should be set to auto
    """
    errorCode = lib.ASISetControlValue(cameraID, controlType, value, auto)
    if errorCode != 0:
        raise ValueError(f"Failed to set control value for cameraID {cameraID}. Error code: {errorCode}")

# Defining ASI_ERROR_CODE ASIGetROIFormat(int iCameraID, int *piWidth, int *piHeight, int *piBin, ASI_IMG_TYPE *pImg_type)
lib.ASIGetROIFormat.restype = ctypes.c_int
lib.ASIGetROIFormat.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
def getROIFormat(cameraID):
    """
    @brief Gets the current ROI format settings of the camera

    @note Capture must be stopped before calling it

    @param cameraID ID of the camera

    @return Tuple containing width
                             height
                             binning
                             image type
    """
    width   = ctypes.c_int()
    height  = ctypes.c_int()
    binning = ctypes.c_int()
    imgType = ctypes.c_int()
    errorCode = lib.ASIGetROIFormat(cameraID, ctypes.byref(width), ctypes.byref(height), ctypes.byref(binning), ctypes.byref(imgType))
    if errorCode != 0:
        raise ValueError(f"Failed to get ROI format for cameraID {cameraID}. Error code: {errorCode}")
    return width.value, height.value, binning.value, imgType.value

# Defining ASI_ERROR_CODE ASISetROIFormat(int iCameraID, int iWidth, int iHeight, int iBin, ASI_IMG_TYPE Img_type)
lib.ASISetROIFormat.restype = ctypes.c_int
lib.ASISetROIFormat.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
def setROIFormat(cameraID, width, height, binning, imgType):
    """
    @brief Sets the ROI format settings of the camera before capture

    @note Capture must be stopped before calling it

    @param cameraID ID of the camera
    @param width    Width of the ROI area. Make sure width % 8 == 0 
    @param height   Height of the ROI area. Make sure height % 2 == 0
                    Further, for USB2.0 camera ASI120, make sure that width * height % 1024 == 0 
    @param binning  Binning method (1 or 2)
    @param imgType  Output format (0: RAW8, 1: RGB24, 2: RAW16, 3: Y8, -1: IMG_END)
    """
    errorCode = lib.ASISetROIFormat(cameraID, width, height, binning, imgType)
    if errorCode != 0:
        raise ValueError(f"Failed to set ROI format for cameraID {cameraID}. Error code: {errorCode}")

# Defining ASI_ERROR_CODE ASIGetStartPos(int iCameraID, int *piStartX, int *piStartY)
lib.ASIGetStartPos.restype = ctypes.c_int
lib.ASIGetStartPos.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
def getStartPos(cameraID):
    """
    @brief Gets the start position of the current ROI area

    @param cameraID ID of the camera

    @return Tuple containing startX
                             startY
    """
    startX = ctypes.c_int()
    startY = ctypes.c_int()
    errorCode = lib.ASIGetStartPos(cameraID, ctypes.byref(startX), ctypes.byref(startY))
    if errorCode != 0:
        raise ValueError(f"Failed to get start position for cameraID {cameraID}. Error code: {errorCode}")
    return startX.value, startY.value

# Defining ASI_ERROR_CODE ASISetStartPos(int iCameraID, int iStartX, int iStartY)
lib.ASISetStartPos.restype = ctypes.c_int
lib.ASISetStartPos.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
def setStartPos(cameraID, startX, startY):
    """
    @brief Sets the start position of the ROI area

    @param cameraID ID of the camera
    @param startX   Start X position
    @param startY   Start Y position
    """
    errorCode = lib.ASISetStartPos(cameraID, startX, startY)
    if errorCode != 0:
        raise ValueError(f"Failed to set start position for cameraID {cameraID}. Error code: {errorCode}")

# Defining ASI_ERROR_CODE ASIGetDroppedFrames(int iCameraID,int *piDropFrames)
lib.ASIGetDroppedFrames.restype = ctypes.c_int
lib.ASIGetDroppedFrames.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
def getDroppedFrames(cameraID):
    """
    @brief Gets the number of dropped frames

    @notes Drop frames happen when USB is traffic or harddisk write speed is slow
           it will reset to 0 after stop capture

    @param cameraID ID of the camera

    @return Number of dropped frames
    """
    droppedFrames = ctypes.c_int()
    errorCode = lib.ASIGetDroppedFrames(cameraID, ctypes.byref(droppedFrames))
    if errorCode != 0:
        raise ValueError(f"Failed to get dropped frames for cameraID {cameraID}. Error code: {errorCode}")
    return droppedFrames.value

# Defining ASI_ERROR_CODE ASIEnableDarkSubtract(int iCameraID, char *pcBMPPath)
lib.ASIEnableDarkSubtract.restype = ctypes.c_int
# ================= TO BE DONE =================

# Defining ASI_ERROR_CODE ASIDisableDarkSubtract(int iCameraID)
lib.ASIDisableDarkSubtract.restype = ctypes.c_int
lib.ASIDisableDarkSubtract.argtypes = [ctypes.c_int]
def disableDarkSubtract(cameraID):
    """
    @brief Disables the dark subtract function

    @notes Should be called at start if no dark function is used,
           because the function is remembered on Windows platform

    @param cameraID ID of the camera
    """
    errorCode = lib.ASIDisableDarkSubtract(cameraID)
    if errorCode != 0:
        raise ValueError(f"Failed to disable dark subtract for cameraID {cameraID}. Error code: {errorCode}")

# Defining ASI_ERROR_CODE ASIStartVideoCapture(int iCameraID)
lib.ASIStartVideoCapture.restype = ctypes.c_int
lib.ASIStartVideoCapture.argtypes = [ctypes.c_int]
def startVideoCapture(cameraID):
    """
    @brief Starts video capture

    @param cameraID ID of the camera
    """
    errorCode = lib.ASIStartVideoCapture(cameraID)
    if errorCode != 0:
        raise ValueError(f"Failed to start video capture for cameraID {cameraID}. Error code: {errorCode}")

# Defining ASI_ERROR_CODE ASIStopVideoCapture(int iCameraID)
lib.ASIStopVideoCapture.restype = ctypes.c_int
lib.ASIStopVideoCapture.argtypes = [ctypes.c_int]
def stopVideoCapture(cameraID):
    """
    @brief Stops video capture

    @param cameraID ID of the camera
    """
    errorCode = lib.ASIStopVideoCapture(cameraID)
    if errorCode != 0:
        raise ValueError(f"Failed to stop video capture for cameraID {cameraID}. Error code: {errorCode}")

# Defining ASI_ERROR_CODE ASIGetVideoData(int iCameraID, unsigned char* pBuffer, long lBuffSize, int iWaitms)
lib.ASIGetVideoData.restype = ctypes.c_int
lib.ASIGetVideoData.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_long, ctypes.c_int]
def getVideoData(cameraID, bufferSize, waitms):
    """
    @brief Gets video data from the camera buffer

    @note This API should be called as fast as possible, the buffer being
          very small, otherwiste frame will be discarded. The best method
          is to maintain one buffer loop and call this API in a different
          thread.
          Make sure that the buffer size is big enough to hold one image,
          otherwiste this API will crash.

    @param cameraID   ID of the camera
    @param bufferSize Buffer to store the video data. Its size, in bytes:
                      8bit mono : width * height
                      16bit mono: width * height * 2
                      RGB24     : width * height * 3
    @param waitms     Time to wait for the data in milliseconds, -1 for
                      infinite.  Recommended value is set to exposure *
                      2 + 500 ms

    @return Buffer containing the video data
    """
    buffer = (ctypes.c_ubyte * bufferSize)()
    errorCode = lib.ASIGetVideoData(cameraID, buffer, bufferSize, waitms)
    if errorCode != 0:
        raise ValueError(f"Failed to get video data for cameraID {cameraID}. Error code: {errorCode}")
    return bytes(buffer)

# Defining ASI_ERROR_CODE ASIGetVideoDataGPS(int iCameraID, unsigned char* pBuffer, long lBuffSize, int iWaitms, ASI_GPS_DATA *gpsData)
lib.ASIGetVideoDataGPS.restype = ctypes.c_int
# =============== TO BE DONE ===============

# Defining ASI_ERROR_CODE ASIPulseGuideOn(int iCameraID, ASI_GUIDE_DIRECTION direction)
lib.ASIPulseGuideOn.restype = ctypes.c_int
# ============== TO BE DONE ==============

# Defining ASI_ERROR_CODE ASIPulseGuideOff(int iCameraID, ASI_GUIDE_DIRECTION direction)
lib.ASIPulseGuideOff.restype = ctypes.c_int
# ============== TO BE DONE ==============

# Defining ASI_ERROR_CODE ASIStartExposure(int iCameraID, ASI_BOOL bIsDark)
lib.ASIStartExposure.restype = ctypes.c_int
# ============== TO BE DONE ==============

# Defining ASI_ERROR_CODE ASIStopExposure(int iCameraID)
lib.ASIStopExposure.restype = ctypes.c_int
# ============== TO BE DONE ==============

# Defining ASI_ERROR_CODE ASIGetExpStatus(int iCameraID, ASI_EXPOSURE_STATUS *pExpStatus)
lib.ASIGetExpStatus.restype = ctypes.c_int
# ============== TO BE DONE ==============

# Defining ASI_ERROR_CODE ASIGetDataAfterExp(int iCameraID, unsigned char* pBuffer, long lBuffSize)
lib.ASIGetDataAfterExp.restype = ctypes.c_int
# ================ TO BE DONE ================

# Defining ASI_ERROR_CODE ASIGetDataAfterExpGPS(int iCameraID, unsigned char* pBuffer, long lBuffSize, ASI_GPS_DATA *gpsData)
lib.ASIGetDataAfterExpGPS.restype = ctypes.c_int
# ================= TO BE DONE =================

# Defining ASI_ERROR_CODE ASIGetID(int iCameraID, ASI_ID* pID)
lib.ASIGetID.restype = ctypes.c_int
lib.ASIGetID.argtypes = [ctypes.c_int, ctypes.POINTER(ID)]
# ====================== TO BE DONE ======================

# Defining ASI_ERROR_CODE ASISetID(int iCameraID, ASI_ID ID)
lib.ASISetID.restype = ctypes.c_int
lib.ASISetID.argtypes = [ctypes.c_int, ID]
# ============== TO BE DONE ==============

# Defining ASI_ERROR_CODE ASIGetGainOffset(int iCameraID, int *pOffset_HighestDR, int *pOffset_UnityGain, int *pGain_LowestRN, int *pOffset_LowestRN)
lib.ASIGetGainOffset.restype = ctypes.c_int
# ============== TO BE DONE ==============

# Defining ASI_ERROR_CODE ASIGetLMHGainOffset(int iCameraID, int* pLGain, int* pMGain, int* pHGain, int* pHOffset)
lib.ASIGetLMHGainOffset.restype = ctypes.c_int
# ================ TO BE DONE ================

# Defining char* ASIGetSDKVersion()
lib.ASIGetSDKVersion.restype = ctypes.c_char_p
lib.ASIGetSDKVersion.argtypes = []
def getSDKVersion():
    """
    @brief Gets the version of the SDK

    @return string containing SDK version with the format "1, 37, 0, 0"
    """
    return lib.ASIGetSDKVersion().decode('utf-8')


# Defining ASI_ERROR_CODE ASIGetCameraSupportMode(int iCameraID, ASI_SUPPORTED_MODE* pSupportedMode)
lib.ASIGetCameraSupportMode.restype = ctypes.c_int
# ================== TO BE DONE ==================

# Defining ASI_ERROR_CODE ASIGetCameraMode(int iCameraID, ASI_CAMERA_MODE* mode)
lib.ASIGetCameraMode.restype = ctypes.c_int
# =============== TO BE DONE ===============

# Defining ASI_ERROR_CODE ASISetCameraMode(int iCameraID, ASI_CAMERA_MODE mode)
lib.ASISetCameraMode.restype = ctypes.c_int
# =============== TO BE DONE ===============

# Defining ASI_ERROR_CODE ASISendSoftTrigger(int iCameraID, ASI_BOOL bStart)
lib.ASISendSoftTrigger.restype = ctypes.c_int
# ================ TO BE DONE ================

# Defining ASIGetSerialNumber(int iCameraID, ASI_SN* pSN)
lib.ASIGetSerialNumber.argtypes = [ctypes.c_int, ctypes.POINTER(SN)]
lib.ASIGetSerialNumber.restype = ctypes.c_int
def getSerialNumber(cameraID):
    """
    @brief Gets the serial number of the camera

    @param cameraID ID of the camera

    @return Hexadecimal string of the serial number of the camera
    """
    serialNumber = SN()
    errorCode = lib.ASIGetSerialNumber(cameraID, ctypes.byref(serialNumber))

    if errorCode != 0:
        raise ValueError(f"Failed to get serial number of cameraID {cameraID}. Error code: {errorCode}")

    return ''.join(f"{b:02X}" for b in serialNumber.SN)

# Defining ASI_ERROR_CODE ASISetTriggerOutputIOConf(int iCameraID, ASI_TRIG_OUTPUT_PIN pin, ASI_BOOL bPinHigh, long lDelay, long lDuration)
lib.ASISetTriggerOutputIOConf.restype = ctypes.c_int
# =================== TO BE DONE ===================

# Defining ASI_ERROR_CODE ASIGetTriggerOutputIOConf(int iCameraID, ASI_TRIG_OUTPUT_PIN pin, ASI_BOOL *bPinHigh, long *lDelay, long *lDuration)
lib.ASIGetTriggerOutputIOConf.restype = ctypes.c_int
# =================== TO BE DONE ===================

# Defining ASI_ERROR_CODE ASIGPSGetData(int iCameraID, ASI_GPS_DATA* startLineGPSData, ASI_GPS_DATA* endLineGPSData)
lib.ASIGPSGetData.restype = ctypes.c_int
# ============= TO BE DONE =============