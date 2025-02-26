import ctypes

lib = ctypes.cdll.LoadLibrary("./lib/x64/ASICamera2.dll")


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
    if pNumOfControls < 0:
        raise ValueError(f"Number of controls of cameraID {cameraID} cannot be negative ({pNumOfControls})")
    return pNumOfControls

# Defining ASI_ERROR_CODE ASIGetControlCaps(int iCameraID, int iControlIndex, ASI_CONTROL_CAPS * pControlCaps)
lib.ASIGetControlCaps.restype = ctypes.c_int
lib.ASIGetControlCaps.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ControlCaps)]
def getControlCaps(cameraID, controlIndex):
    """
    @brief Gets controls property available for this camera

    @param cameraID     can be obtained using getCameraProperty
    @param controlIndex index of control, NOT control type

    @return structure containing the property of the control
    """
    controlCaps = ControlCaps()
    errorCode = lib.ASIGetControlCaps(cameraID, controlIndex, controlCaps)
    if errorCode != 0:
        raise ValueError(f"Failed to get number of controls for cameraID {cameraID}. Error code: {errorCode}")
    return controlCaps

# Defining ASI_ERROR_CODE ASIGetControlValue(int  iCameraID, ASI_CONTROL_TYPE  ControlType, long *plValue, ASI_BOOL *pbAuto)
lib.ASIGetControlValue.restype = ctypes.c_int
lib.ASIGetControlValue.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_int)]
def getControlValue(cameraID, controlType, auto):
    """
    """

# Defining ASI_ERROR_CODE ASISetControlValue(int  iCameraID, ASI_CONTROL_TYPE  ControlType, long lValue, ASI_BOOL bAuto)
lib.ASISetControlValue.restype = ctypes.c_int
lib.ASISetControlValue.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_long, ctypes.c_int]
def setControlValue(cameraID, controlType, value, auto):
    """
    """

# Defining ASI_ERROR_CODE ASIGetROIFormat(int iCameraID, int *piWidth, int *piHeight,  int *piBin, ASI_IMG_TYPE *pImg_type)

# Defining ASI_ERROR_CODE ASISetROIFormat(int iCameraID, int iWidth, int iHeight,  int iBin, ASI_IMG_TYPE Img_type)

# Defining ASI_ERROR_CODE ASIGetStartPos(int iCameraID, int *piStartX, int *piStartY)

# Defining ASI_ERROR_CODE ASISetStartPos(int iCameraID, int iStartX, int iStartY)

# Defining ASI_ERROR_CODE ASIGetDroppedFrames(int iCameraID,int *piDropFrames)

# Defining ASI_ERROR_CODE ASIEnableDarkSubtract(int iCameraID, char *pcBMPPath)

# Defining ASI_ERROR_CODE ASIDisableDarkSubtract(int iCameraID)

# Defining ASI_ERROR_CODE ASIStartVideoCapture(int iCameraID)

# Defining ASI_ERROR_CODE ASIStopVideoCapture(int iCameraID)

# Defining ASI_ERROR_CODE ASIGetVideoData(int iCameraID, unsigned char* pBuffer, long lBuffSize, int iWaitms)

# Defining ASI_ERROR_CODE ASIGetVideoDataGPS(int iCameraID, unsigned char* pBuffer, long lBuffSize, int iWaitms, ASI_GPS_DATA *gpsData)

# Defining ASI_ERROR_CODE ASIPulseGuideOn(int iCameraID, ASI_GUIDE_DIRECTION direction)

# Defining ASI_ERROR_CODE ASIPulseGuideOff(int iCameraID, ASI_GUIDE_DIRECTION direction)

# Defining ASI_ERROR_CODE ASIStartExposure(int iCameraID, ASI_BOOL bIsDark)

# Defining ASI_ERROR_CODE ASIStopExposure(int iCameraID)

# Defining ASI_ERROR_CODE ASIGetExpStatus(int iCameraID, ASI_EXPOSURE_STATUS *pExpStatus)

# Defining ASI_ERROR_CODE ASIGetDataAfterExp(int iCameraID, unsigned char* pBuffer, long lBuffSize)

# Defining ASI_ERROR_CODE ASIGetDataAfterExpGPS(int iCameraID, unsigned char* pBuffer, long lBuffSize, ASI_GPS_DATA *gpsData)

# Defining ASI_ERROR_CODE ASIGetID(int iCameraID, ASI_ID* pID)

# Defining ASI_ERROR_CODE ASISetID(int iCameraID, ASI_ID ID)

# Defining ASI_ERROR_CODE ASIGetGainOffset(int iCameraID, int *pOffset_HighestDR, int *pOffset_UnityGain, int *pGain_LowestRN, int *pOffset_LowestRN)

# Defining ASI_ERROR_CODE ASIGetLMHGainOffset(int iCameraID, int* pLGain, int* pMGain, int* pHGain, int* pHOffset)

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

# Defining ASI_ERROR_CODE ASIGetCameraMode(int iCameraID, ASI_CAMERA_MODE* mode)

# Defining ASI_ERROR_CODE ASISetCameraMode(int iCameraID, ASI_CAMERA_MODE mode)

# Defining ASISendSoftTrigger(int iCameraID, ASI_BOOL bStart)

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

# Defining ASI_ERROR_CODE ASIGetTriggerOutputIOConf(int iCameraID, ASI_TRIG_OUTPUT_PIN pin, ASI_BOOL *bPinHigh, long *lDelay, long *lDuration)

# Defining ASI_ERROR_CODE ASIGPSGetData(int iCameraID, ASI_GPS_DATA* startLineGPSData, ASI_GPS_DATA* endLineGPSData)