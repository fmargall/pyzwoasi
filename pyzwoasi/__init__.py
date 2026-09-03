# First part, before loading wrappers
# is to check win-driver installation
import platform, subprocess, warnings
import os, glob

def _checkWindowsDriverViaPnPUtil():
    try:
        result = subprocess.run(
            ["pnputil", "/enum-drivers"],
            capture_output=True,
            text=True,
            timeout=3
        )
    except Exception:
        # PnPUtil not available
        return None

    output = result.stdout.lower()

    if "zwo" in output:
        return True

    return False

def _checkWindowsDriverViaInfParsing():
    inf_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "INF")
    patterns = ["*ASICAMUSB3*.inf", "*ZWO*.inf", "*ASI*.inf"]

    for pat in patterns:
        for file in glob.glob(os.path.join(inf_dir, pat)):
            return True
    return False

def _checkWindowsDriver():
    if platform.system() != "Windows":
        return # Only Windows needs it

    status = _checkWindowsDriverViaPnPUtil()
    if status is True:
        return # Driver installed correctly
    if status is None:
        # PnPUtil not available, Windows version maybe too old
        status = _checkWindowsDriverViaInfParsing()
        if status is True:
            return

    warnings.warn(
        "ZWO ASI driver does not appear to be installed on this system.\n"
        "Windows will not detect any ASI cameras without needed driver.\n"
        "Please install it from: https://www.zwoastro.com/downloads/",
        RuntimeWarning
    )

    
# Check during import
_checkWindowsDriver()

from .pyzwoasi import (
    ASIError, ASIErrorCode, ASIExposureStatus, ASIImageType,
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