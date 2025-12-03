from .pyzwoasi import (
    ASIError, ASIErrorCode, ASIExposureStatus,
    CameraInfo, ControlCaps, DateTime, GPSData, ID, SN,
    getNumOfConnectedCameras,
    getProductIDs,
    cameraCheck,
    getCameraProperty,
    getCameraPropertyByID,
    openCamera,
    initCamera,
    closeCamera,
    getNumOfControls,
    getControlCaps,
    getControlValue,
    setControlValue,
    getROIFormat,
    setROIFormat,
    getStartPos,
    setStartPos,
    getDroppedFrames,
    disableDarkSubtract,
    startVideoCapture,
    stopVideoCapture,
    getVideoData,
    startExposure,
    stopExposure,
    getExpStatus,
    getDataAfterExp,
    getID,
    setID,
    getGainOffset,
    getLMHGainOffset,
    getSDKVersion,
    getCameraSupportMode,
    getCameraMode,
    getSerialNumber,
    getTriggerOutputIOConf,
    getTriggerOutputIOConf
)

# High-level convenience class
from .camera import ZWOCamera

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("pyzwoasi")
except PackageNotFoundError:
    __version__ = "?.?.?"