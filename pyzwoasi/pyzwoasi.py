import ctypes
import enum
import platform
import os


# Chosing and reading correct dll
system = platform.system()
arch = platform.architecture()[0]
if   system == 'Windows':
    dllPath = os.path.join(os.path.dirname(__file__), 'lib', system, 'x64' if arch == '64bit' else 'x86', 'ASICamera2.dll')
elif system == 'Linux':
    dllPath = os.path.join(os.path.dirname(__file__), 'lib', system, 'x64' if arch == '64bit' else 'x86', 'libASICamera2.so.1.40')
elif system == 'Darwin':
    machine = platform.machine().lower()
    is_arm = machine.startswith('arm') or machine.startswith('aarch64')
    macos_base = os.path.join(os.path.dirname(__file__), 'lib', 'MacOS')
    dllPath = os.path.join(macos_base, 'arm64', 'libASICamera2.dylib.1.40') if is_arm else os.path.join(macos_base, 'x86_64', 'libASICamera2.dylib.1.40')
else:
    raise ValueError(f"Unsupported system: {system}")
lib = ctypes.cdll.LoadLibrary(dllPath)

# Defining custom exception type for dll errors
class ASIError(Exception):
    def __init__(self, mssg, errorCode):
        super().__init__(mssg, errorCode, ASIErrorCode(errorCode).name)

# Defining ASI error codes
class ASIErrorCode(enum.IntEnum):
    ASI_SUCCESS                      = 0
    ASI_ERROR_INVALID_INDEX          = enum.auto() # no camera connected or index value out of boundary
    ASI_ERROR_INVALID_ID             = enum.auto() # invalid ID
    ASI_ERROR_INVALID_CONTROL_TYPE   = enum.auto() # invalid control type
    ASI_ERROR_CAMERA_CLOSED          = enum.auto() # camera didn't open
    ASI_ERROR_CAMERA_REMOVED         = enum.auto() # failed to find the camera, maybe the camera has been removed
    ASI_ERROR_INVALID_PATH           = enum.auto() # cannot find the path of the file
    ASI_ERROR_INVALID_FILEFORMAT     = enum.auto()
    ASI_ERROR_INVALID_SIZE           = enum.auto() # wrong video format size
    ASI_ERROR_INVALID_IMGTYPE        = enum.auto() # unsupported image formate
    ASI_ERROR_OUT_OF_BOUNDARY        = enum.auto() # the startpos is out of boundary
    ASI_ERROR_TIMEOUT                = enum.auto() # timeout
    ASI_ERROR_INVALID_SEQUENCE       = enum.auto() # stop capture first
    ASI_ERROR_BUFFER_TOO_SMALL       = enum.auto() # buffer size is not big enough
    ASI_ERROR_VIDEO_MODE_ACTIVE      = enum.auto()
    ASI_ERROR_EXPOSURE_IN_PROGRESS   = enum.auto()
    ASI_ERROR_GENERAL_ERROR          = enum.auto() # general error, eg: value is out of valid range
    ASI_ERROR_INVALID_MODE           = enum.auto() # the current mode is wrong
    ASI_ERROR_GPS_NOT_SUPPORTED      = enum.auto() # this camera do not support GPS
    ASI_ERROR_GPS_VER_ERR            = enum.auto() # the FPGA GPS ver is too low
    ASI_ERROR_GPS_FPGA_ERR           = enum.auto() # failed to read or write data to FPGA
    ASI_ERROR_GPS_PARAM_OUT_OF_RANGE = enum.auto() # start line or end line out of range, should make them between 0 ~ MaxHeight - 1
    ASI_ERROR_GPS_DATA_INVALID       = enum.auto() # GPS has not yet found the satellite or FPGA cannot read GPS data

# Defining ASI image types
class ASIImageType(enum.IntEnum):
    ASI_IMG_RAW8   = 0           #      RAW image,  8 bits per pixel
    ASI_IMG_RGB24  = enum.auto() #      RGB image, 24 bits per pixel
    ASI_IMG_RAW16  = enum.auto() #      RAW image, 16 bits per pixel
    ASI_IMG_Y8     = enum.auto() # Y (mono) image,  8 bits per pixel
    ASI_IMG_END    = enum.auto() #   End of image type

# Defining ASI Exposure Status
class ASIExposureStatus(enum.IntEnum):
    ASI_EXP_IDLE    = 0           # Idle state, exposure can be started
    ASI_EXP_WORKING = enum.auto() # Exposure in progress
    ASI_EXP_SUCCESS = enum.auto() # Exposure over, waiting for download
    ASI_EXP_FAILED  = enum.auto() # Exposure failed should be restarted

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
        ("ControlType"    , ctypes.c_int),        # Used to get value and set value of the control
        ("Unused"         , ctypes.c_char * 32)
    ]

# Defining struct _ASI_DATE_TIME
class DateTime(ctypes.Structure):
    _fields_ = [
        ("Year"   , ctypes.c_int),
        ("Month"  , ctypes.c_int),
        ("Day"    , ctypes.c_int),
        ("Hour"   , ctypes.c_int),
        ("Minute" , ctypes.c_int),
        ("Second" , ctypes.c_int),
        ("Msecond", ctypes.c_int),
        ("Usecond", ctypes.c_int),
        ("Unused" , ctypes.c_char * 64) 
    ]

# Defining struct _ASI_GPS_DATA
class GPSData(ctypes.Structure):
    _fields_ = [
        ("DateTime"    , DateTime),
        ("Latitude"    , ctypes.c_double), # Latitude in degrees , positive for North, negative for South
        ("Longitude"   , ctypes.c_double), # Longitude in degrees, positive for East , negative for West
        ("Altitude"    , ctypes.c_int),    # Altitude (minimum unit is 0.1 m) (maximum number is 99999)
        ("SatelliteNum", ctypes.c_int),    # Maximum number is 99
        ("Unused"      , ctypes.c_char * 64)
    ]

# Defining struct _ASI_ID
class ID(ctypes.Structure):
    _fields_ = [
        ("ID", ctypes.c_ubyte * 8) # 8-byte array
    ]

# Defining struct _ASI_SN
class SN(ctypes.Structure):
    _fields_ = [
        ("SN", ctypes.c_ubyte * 8) # 8-byte array
    ]

# Defining struct _ASI_SUPPORTED_MODE
class SupportedMode(ctypes.Structure):
    _fields_ = [
        ("SupportedMode", ctypes.c_int * 16)
    ]

# Defining int ASIGetNumOfConnectedCameras()
lib.ASIGetNumOfConnectedCameras.restype = ctypes.c_int
def getNumOfConnectedCameras():
    """
    @brief Gets number of connected ASI cameras

    @note This should be the first API to be called

    @return Number of connected ASI cameras
    """
    return lib.ASIGetNumOfConnectedCameras()

# Defining int ASIGetProductIDs(int* pPIDs)
lib.ASIGetNumOfConnectedCameras.restype = ctypes.c_int
lib.ASIGetProductIDs.argtypes = [ctypes.POINTER(ctypes.c_int)]
def getProductIDs():
    """
    @brief Gets product IDs of connected ASI cameras

    @note This API will be deprecated. Please use CameraCheck instead

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
        raise ASIError(f"Failed to get camera property. Error code: {errorCode}", errorCode)
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
        raise ASIError(f"Failed to get camera property by ID. Error code: {errorCode}", errorCode)
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
        raise ASIError(f"Failed to open camera. Error code: {errorCode}", errorCode)

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
        raise ASIError(f"Failed to initialize camera. Error code: {errorCode}", errorCode)

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
        raise ASIError(f"Failed to close camera. Error code: {errorCode}", errorCode)

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
        raise ASIError(f"Failed to get number of controls for cameraID {cameraID}. Error code: {errorCode}", errorCode)
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
        raise ASIError(f"Failed to get number of controls for cameraID {cameraID}. Error code: {errorCode}", errorCode)
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
        raise ASIError(f"Failed to get control value for cameraID {cameraID}. Error code: {errorCode}", errorCode)
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
        raise ASIError(f"Failed to set control value for cameraID {cameraID}. Error code: {errorCode}", errorCode)

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
        raise ASIError(f"Failed to get ROI format for cameraID {cameraID}. Error code: {errorCode}", errorCode)
    return width.value, height.value, binning.value, ASIImageType(imgType.value)

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
        raise ASIError(f"Failed to set ROI format for cameraID {cameraID}. Error code: {errorCode}", errorCode)

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
        raise ASIError(f"Failed to get start position for cameraID {cameraID}. Error code: {errorCode}", errorCode)
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
        raise ASIError(f"Failed to set start position for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASI_ERROR_CODE ASIGetDroppedFrames(int iCameraID,int *piDropFrames)
lib.ASIGetDroppedFrames.restype = ctypes.c_int
lib.ASIGetDroppedFrames.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
def getDroppedFrames(cameraID):
    """
    @brief Gets the number of dropped frames

    @note Drop frames happen when USB is traffic or harddisk write speed is slow
           it will reset to 0 after stop capture

    @param cameraID ID of the camera

    @return Number of dropped frames
    """
    droppedFrames = ctypes.c_int()
    errorCode = lib.ASIGetDroppedFrames(cameraID, ctypes.byref(droppedFrames))
    if errorCode != 0:
        raise ASIError(f"Failed to get dropped frames for cameraID {cameraID}. Error code: {errorCode}", errorCode)
    return droppedFrames.value

# Defining ASI_ERROR_CODE ASIEnableDarkSubtract(int iCameraID, char *pcBMPPath)
lib.ASIEnableDarkSubtract.restype = ctypes.c_int
lib.ASIEnableDarkSubtract.argtypes = [ctypes.c_int, ctypes.c_char_p]
def enableDarkSubtract(cameraID, bmpPath):
    """
    @brief Enables the dark subtract function from a dark BMP file

    @note Used when there is hot pixel or when long exposure is needed.
          Dark file should be made from the "dark subtract" function of
          the "video capture filter" directshow page.
          Dark file's size should be the same of camera's max width and
          height and should be RGB8 raw format. It will stay on even if 
          the ROI settings are modified.

    @param cameraID ID of the camera
    @param bmpPath  Path to the BMP file used for dark substraction
    """
    errorCode = lib.ASIEnableDarkSubtract(cameraID, bmpPath.encode('utf-8'))
    if errorCode != 0:
        raise ASIError(f"Failed to enable dark subtract for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASI_ERROR_CODE ASIDisableDarkSubtract(int iCameraID)
lib.ASIDisableDarkSubtract.restype = ctypes.c_int
lib.ASIDisableDarkSubtract.argtypes = [ctypes.c_int]
def disableDarkSubtract(cameraID):
    """
    @brief Disables the dark subtract function

    @note Should be called at start if no dark function is used,
           because the function is remembered on Windows platform

    @param cameraID ID of the camera
    """
    errorCode = lib.ASIDisableDarkSubtract(cameraID)
    if errorCode != 0:
        raise ASIError(f"Failed to disable dark subtract for cameraID {cameraID}. Error code: {errorCode}", errorCode)

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
        raise ASIError(f"Failed to start video capture for cameraID {cameraID}. Error code: {errorCode}", errorCode)

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
        raise ASIError(f"Failed to stop video capture for cameraID {cameraID}. Error code: {errorCode}", errorCode)

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
                      8 bit mono: width * height
                      16bit mono: width * height * 2
                      24bit RGB : width * height * 3
    @param waitms     Time to wait for the data in milliseconds, -1 for
                      infinite.  Recommended value is set to exposure *
                      2 + 500 ms

    @return Buffer containing the video data
    """
    buffer = (ctypes.c_ubyte * bufferSize)()
    errorCode = lib.ASIGetVideoData(cameraID, buffer, bufferSize, waitms)
    if errorCode != 0:
        raise ASIError(f"Failed to get video data for cameraID {cameraID}. Error code: {errorCode}", errorCode)
    return bytes(buffer)

# Defining ASI_ERROR_CODE ASIGetVideoDataGPS(int iCameraID, unsigned char* pBuffer, long lBuffSize, int iWaitms, ASI_GPS_DATA *gpsData)
lib.ASIGetVideoDataGPS.restype = ctypes.c_int
lib.ASIGetVideoDataGPS.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_long, ctypes.c_int, ctypes.POINTER(GPSData)]
# =============== TO BE DONE ===============

# Defining ASI_ERROR_CODE ASIPulseGuideOn(int iCameraID, ASI_GUIDE_DIRECTION direction)
lib.ASIPulseGuideOn.restype = ctypes.c_int
lib.ASIPulseGuideOn.argtypes = [ctypes.c_int, ctypes.c_int]
def pulseGuideOn(cameraID, direction):
    """
    @brief Pulsing guide on the ST4 port set to on

    @note This function only works on the module which has ST4 port

    @param cameraID  ID of the camera
    @param direction Direction of the guider. Should be set to:
                      - 0 for North    - 1 for South
                      - 2 for East     - 3 for West
    """
    errorCode = lib.ASIPulseGuideOn(cameraID, direction)
    if errorCode != 0:
        raise ASIError(f"Failed to pulse guide on for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASI_ERROR_CODE ASIPulseGuideOff(int iCameraID, ASI_GUIDE_DIRECTION direction)
lib.ASIPulseGuideOff.restype = ctypes.c_int
lib.ASIPulseGuideOff.argtypes = [ctypes.c_int, ctypes.c_int]
def pulseGuideOff(cameraID, direction):
    """
    @brief Pulsing guide on the ST4 port set to off

    @note This function only works on the module which has ST4 port

    @param cameraID  ID of the camera
    @param direction Direction of the guider. Should be set to:
                      - 0 for North    - 1 for South
                      - 2 for East     - 3 for West
    """
    errorCode = lib.ASIPulseGuideOff(cameraID, direction)
    if errorCode != 0:
        raise ASIError(f"Failed to pulse guide off for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASI_ERROR_CODE ASIStartExposure(int iCameraID, ASI_BOOL bIsDark)
lib.ASIStartExposure.restype = ctypes.c_int
lib.ASIStartExposure.argtypes = [ctypes.c_int, ctypes.c_int]
def startExposure(cameraID, isDark):
    """
    @brief Starts exposure

    @note Usually used when long exposure required

    @param cameraID ID of the camera
    @param isDark   Boolean indicating dark frame if there is mechanical
                    shutter on the camera. Useles otherwise
    """
    errorCode = lib.ASIStartExposure(cameraID, 1 if isDark else 0)
    if errorCode != 0:
        raise ASIError(f"Failed to start exposure for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASI_ERROR_CODE ASIStopExposure(int iCameraID)
lib.ASIStopExposure.restype = ctypes.c_int
lib.ASIStopExposure.argtypes = [ctypes.c_int]
def stopExposure(cameraID):
    """
    @brief Stops long exposure which is on

    @param cameraID ID of the camera
    """
    errorCode = lib.ASIStopExposure(cameraID)
    if errorCode != 0:
        raise ASIError(f"Failed to stop exposure for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASI_ERROR_CODE ASIGetExpStatus(int iCameraID, ASI_EXPOSURE_STATUS *pExpStatus)
lib.ASIGetExpStatus.restype = ctypes.c_int
lib.ASIGetExpStatus.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
def getExpStatus(cameraID):
    """
    @brief Get snap status

    @note After snap is started, the status should be checked continuously

    @param cameraID ID of the camera

    @return Current snap status, among the following values:
             - 0: [ASI_SUCCESS] Operation is successful,
             - 1: [ASI_ERROR_CAMERA_CLOSED] Camera is closed,
             - 2: [ASI_ERROR_INVALID_ID] No camera with this ID is connected
    """
    expStatus = ctypes.c_int()
    errorCode = lib.ASIGetExpStatus(cameraID, ctypes.byref(expStatus))
    if errorCode != 0:
        raise ASIError(f"Failed to get exposure status for cameraID {cameraID}. Error code: {errorCode}", errorCode)
    return ASIExposureStatus(expStatus.value)

# Defining ASI_ERROR_CODE ASIGetDataAfterExp(int iCameraID, unsigned char* pBuffer, long lBuffSize)
lib.ASIGetDataAfterExp.restype = ctypes.c_int
lib.ASIGetDataAfterExp.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_long]
def getDataAfterExp(cameraID, bufferSize):
    """
    @brief Get data after exposure

    @note Make sure that the buffer size is big enough
          to hold an image, otherwise API will crash.
    
    @param cameraID   ID of the camera
    @param bufferSize Buffer to store the data. Its size, in bytes:
                      8bit mono : width * height
                      16bit mono: width * height * 2
                      RGB24     : width * height * 3

    @return Buffer containing the data after exposure
    """
    buffer = (ctypes.c_ubyte * bufferSize)()
    errorCode = lib.ASIGetDataAfterExp(cameraID, buffer, bufferSize)
    if errorCode != 0:
        raise ASIError(f"Failed to get data after exposure for cameraID {cameraID}. Error code: {errorCode}", errorCode)
    return bytes(buffer)

# Defining ASI_ERROR_CODE ASIGetDataAfterExpGPS(int iCameraID, unsigned char* pBuffer, long lBuffSize, ASI_GPS_DATA *gpsData)
lib.ASIGetDataAfterExpGPS.restype = ctypes.c_int
lib.ASIGetDataAfterExpGPS.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_long, ctypes.POINTER(GPSData)]
# ================= TO BE DONE =================

# Defining ASI_ERROR_CODE ASIGetID(int iCameraID, ASI_ID* pID)
lib.ASIGetID.restype = ctypes.c_int
lib.ASIGetID.argtypes = [ctypes.c_int, ctypes.POINTER(ID)]
def getID(cameraID):
    """
    @brief Gets the ID of the camera

    @note Only available for USB 3.0 cameras

    @param cameraID ID of the camera

    @return Structure containing the ID of the camera
    """
    cameraIDStruct = ID()
    errorCode = lib.ASIGetID(cameraID, ctypes.byref(cameraIDStruct))
    if errorCode != 0:
        raise ASIError(f"Failed to get ID for cameraID {cameraID}. Error code: {errorCode}", errorCode)
    return cameraIDStruct

# Defining ASI_ERROR_CODE ASISetID(int iCameraID, ASI_ID ID)
lib.ASISetID.restype = ctypes.c_int
lib.ASISetID.argtypes = [ctypes.c_int, ID]
def setID(cameraID, newCameraID):
    """
    @brief Writes camera ID to flash.

    @note Only available for USB 3.0 cameras

    @param cameraID    ID of the camera
    @param newCameraID New ID to set for the camera
    """
    errorCode = lib.ASISetID(cameraID, newCameraID)
    if errorCode != 0:
        raise ASIError(f"Failed to set ID for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASI_ERROR_CODE ASIGetGainOffset(int iCameraID, int *pOffset_HighestDR, int *pOffset_UnityGain, int *pGain_LowestRN, int *pOffset_LowestRN)
lib.ASIGetGainOffset.restype = ctypes.c_int
lib.ASIGetGainOffset.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
def getGainOffset(cameraID):
    """
    @brief Gets the gain and offset pre-setting parameters values for the camera

    @param cameraID ID of the camera

    @return Tuple containing:
             - offsetHighestDR: Offset for the highest dynamic range
             - offsetUnityGain: Offset for the unity gain
             - gainLowestRN   : Gain for the lowest read noise
             - offsetLowestRN : Offset for the lowest read noise
    """
    offsetHighestDR = ctypes.c_int()
    offsetUnityGain = ctypes.c_int()
    gainLowestRN    = ctypes.c_int()
    offsetLowestRN  = ctypes.c_int()

    errorCode = lib.ASIGetGainOffset(cameraID, 
                                     ctypes.byref(offsetHighestDR), 
                                     ctypes.byref(offsetUnityGain), 
                                     ctypes.byref(gainLowestRN)   , 
                                     ctypes.byref(offsetLowestRN) )
    if errorCode != 0:
        raise ASIError(f"Failed to get gain/offset for cameraID {cameraID}. Error code: {errorCode}", errorCode)

    return (offsetHighestDR.value, offsetUnityGain.value, gainLowestRN.value, offsetLowestRN.value)

# Defining ASI_ERROR_CODE ASIGetLMHGainOffset(int iCameraID, int* pLGain, int* pMGain, int* pHGain, int* pHOffset)
lib.ASIGetLMHGainOffset.restype = ctypes.c_int
lib.ASIGetLMHGainOffset.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
def getLMHGainOffset(cameraID):
    """
    @brief Gets the frequently-used gain and offset pre-setting parameters values for the camera

    @param cameraID ID of the camera

    @return Tuple containing:
             - lGain  : Low gain value
             - mGain  : Medium gain value
             - hGain  : High gain value (gain at the lowest read noise)
             - hOffset: High offset value
    """
    lGain   = ctypes.c_int()
    mGain   = ctypes.c_int()
    hGain   = ctypes.c_int()
    hOffset = ctypes.c_int()
    errorCode = lib.ASIGetLMHGainOffset(cameraID, 
                                        ctypes.byref(lGain), 
                                        ctypes.byref(mGain), 
                                        ctypes.byref(hGain), 
                                        ctypes.byref(hOffset))
    if errorCode != 0:
        raise ASIError(f"Failed to get LMH gain/offset for cameraID {cameraID}. Error code: {errorCode}", errorCode)
    
    return (lGain.value, mGain.value, hGain.value, hOffset.value)

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
lib.ASIGetCameraSupportMode.argtypes = [ctypes.c_int, ctypes.POINTER(SupportedMode)]
def getCameraSupportMode(cameraID):
    """
    @brief Gets the supported mode of the camera

    @param cameraID ID of the camera

    @return int corresponding to the supported mode:
             - 0 for normal              - 1 for trigger soft edge
             - 2 for trigger rise edge   - 3 for trigger fall edge
             - 4 for trigger soft level  - 5 for trigger high level
             - 6 for trigger low level
    """
    supportedMode = SupportedMode()
    errorCode = lib.ASIGetCameraSupportMode(cameraID, ctypes.byref(supportedMode))
    if errorCode != 0:
        raise ASIError(f"Failed to get camera support mode for cameraID {cameraID}. Error code: {errorCode}", errorCode)
    return supportedMode

# Defining ASI_ERROR_CODE ASIGetCameraMode(int iCameraID, ASI_CAMERA_MODE* mode)
lib.ASIGetCameraMode.restype = ctypes.c_int
lib.ASIGetCameraMode.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
def getCameraMode(cameraID):
    """
    @brief Gets the current camera mode

    @note Should be called only when IsTriggerCam in CameraInfo is true

    @param cameraID ID of the camera

    @return int corresponding to the camera mode:
             - 0 for normal              - 1 for trigger soft edge
             - 2 for trigger rise edge   - 3 for trigger fall edge
             - 4 for trigger soft level  - 5 for trigger high level
             - 6 for trigger low level
    """
    cameraMode = ctypes.c_int()
    errorCode = lib.ASIGetCameraMode(cameraID, ctypes.byref(cameraMode))
    if errorCode != 0:
        raise ASIError(f"Failed to get camera mode for cameraID {cameraID}. Error code: {errorCode}", errorCode)
    return cameraMode.value

# Defining ASI_ERROR_CODE ASISetCameraMode(int iCameraID, ASI_CAMERA_MODE mode)
lib.ASISetCameraMode.restype = ctypes.c_int
lib.ASISetCameraMode.argtypes = [ctypes.c_int, ctypes.c_int]
def setCameraMode(cameraID, cameraMode):
    """
    @brief Sets the camera mode

    @note Should be called only when IsTriggerCam in CameraInfo is true

    @param cameraID   ID of the camera
    @param cameraMode int corresponding to the camera mode to set:
                       - 0 for normal              - 1 for trigger soft edge
                       - 2 for trigger rise edge   - 3 for trigger fall edge
                       - 4 for trigger soft level  - 5 for trigger high level
                       - 6 for trigger low level
    """
    errorCode = lib.ASISetCameraMode(cameraID, cameraMode)
    if errorCode != 0:
        raise ASIError(f"Failed to set camera mode for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASI_ERROR_CODE ASISendSoftTrigger(int iCameraID, ASI_BOOL bStart)
lib.ASISendSoftTrigger.restype = ctypes.c_int
lib.ASISendSoftTrigger.argtypes = [ctypes.c_int, ctypes.c_int]
def sendSoftTrigger(cameraID, start):
    """
    @brief Sends a softTrigger to the camera

    @param cameraID ID of the camera
    @param start    Boolean indicating if the trigger should start
    """
    errorCode = lib.ASISendSoftTrigger(cameraID, 1 if start else 0)
    if errorCode != 0:
        raise ASIError(f"Failed to send soft trigger for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASIGetSerialNumber(int iCameraID, ASI_SN* pSN)
lib.ASIGetSerialNumber.restype = ctypes.c_int
lib.ASIGetSerialNumber.argtypes = [ctypes.c_int, ctypes.POINTER(SN)]
def getSerialNumber(cameraID):
    """
    @brief Gets the serial number of the camera

    @param cameraID ID of the camera

    @return Hexadecimal string of the serial number of the camera
    """
    serialNumber = SN()
    errorCode = lib.ASIGetSerialNumber(cameraID, ctypes.byref(serialNumber))

    if errorCode != 0:
        raise ASIError(f"Failed to get serial number of cameraID {cameraID}. Error code: {errorCode}", errorCode)

    return ''.join(f"{b:02X}" for b in serialNumber.SN)

# Defining ASI_ERROR_CODE ASISetTriggerOutputIOConf(int iCameraID, ASI_TRIG_OUTPUT_PIN pin, ASI_BOOL bPinHigh, long lDelay, long lDuration)
lib.ASISetTriggerOutputIOConf.restype = ctypes.c_int
lib.ASISetTriggerOutputIOConf.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_long, ctypes.c_long]
def setTriggerOutputIOConf(cameraID, pin, bPinHigh, delay, duration):
    """
    @brief Sets the trigger output IO pin configuration

    @param cameraID ID of the camera
    @param pin      Trigger output pin to set the configuration of. This should be one of the
                    following:
                     -  0 for pin A output only
                     -  1 for pin B output only
                     - -1 for none
    @param bPinHigh Boolean indicating if the pin should output a high level as a valid signal
    @param delay    Delay in microseconds between trigger and output. From 0 to 2000*1000*1000
    @param duration Duration in microseconds of the valid output level. Once again goes from 0
                    to 2000*1000*1000.
    """
    errorCode = lib.ASISetTriggerOutputIOConf(cameraID, pin, 1 if bPinHigh else 0, delay, duration)
    if errorCode != 0:
        raise ASIError(f"Failed to set trigger output IO configuration for cameraID {cameraID}. Error code: {errorCode}", errorCode)

# Defining ASI_ERROR_CODE ASIGetTriggerOutputIOConf(int iCameraID, ASI_TRIG_OUTPUT_PIN pin, ASI_BOOL *bPinHigh, long *lDelay, long *lDuration)
lib.ASIGetTriggerOutputIOConf.restype = ctypes.c_int
lib.ASIGetTriggerOutputIOConf.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)]
def getTriggerOutputIOConf(cameraID, pin):
    """
    @brief Gets the trigger output IO pin configuration

    @param cameraID ID of the camera
    @param pin      Trigger output pin to get the configuration of, should be one of the following:
                    -  0 for pin A output only
                    -  1 for pin B output only
                    - -1 for none
    
    @return Tuple containing:
             - bPinHigh: True if the pin outputs a high level as a valid signal, False otherwise
             - delay   : Delay in microseconds between trigger and output
             - duration: Duration in microseconds of the valid output level

    @note Should be called only when IsTriggerCam in CameraInfo is true.
    """
    bPinHigh  = ctypes.c_int()
    lDelay    = ctypes.c_long()
    lDuration = ctypes.c_long()

    errorCode = lib.ASIGetTriggerOutputIOConf(cameraID, pin,
                                              ctypes.byref(bPinHigh),
                                              ctypes.byref(lDelay),
                                              ctypes.byref(lDuration))

    if errorCode != 0:
        raise ASIError(f"Failed to get trigger output IO configuration for cameraID {cameraID}. Error code: {errorCode}", errorCode)

    return (bPinHigh.value == 1, lDelay.value, lDuration.value)

# Defining ASI_ERROR_CODE ASIGPSGetData(int iCameraID, ASI_GPS_DATA* startLineGPSData, ASI_GPS_DATA* endLineGPSData)
lib.ASIGPSGetData.restype = ctypes.c_int
lib.ASIGPSGetData.argtypes = [ctypes.c_int, ctypes.POINTER(GPSData), ctypes.POINTER(GPSData)]
# ============= TO BE DONE =============