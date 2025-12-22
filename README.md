![Header](./docs/pyzwoasi-header.png)

# PyZWOASI &middot; <img src="https://github.com/fmargall/pyzwoasi/actions/workflows/deployment.yml/badge.svg" alt="Build status"> <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"> <a href="https://github.com/qoomon/starlines"> <img src="https://starlines.qoo.monster/assets/fmargall/pyzwoasi" align="right" alt="Starline counter"/> </a>

## Overview

PyZWOASI is a lightweight, cross-platform Python binding for the ZWO ASI SDK, allowing you to control and stream data from all ZWO ASI USB cameras directly from Python.

The project provides:

- A low-level ctypes wrapper exposing all original SDK functions
- Full support for exposure, ROI, binning, video capture, etc.
- Cross-platform DLL/SO/Dylib loading (Windows / Linux / macOS)
- Example scripts for live view

It is designed to be simple to use for beginners, while remaining powerful enough for advanced users who require direct access to the underlying SDK.

## Features

- [x] Easy-to-use Python interface class for ZWO ASI cameras `ZWOCamera`
- [x] Live-view with real-time frame display using `OpenCV` 
- [ ] Direct access to all ZWO ASI SDK functions (40 / 43)
   - [ ] Add function `ASIGetVideoDataGPS`
   - [ ] Add function `ASIGetDataAfterExpGPS`
   - [ ] Add function `ASIGPSGetData`
- [x] Cross-platform support (Windows, Linux, MacOS)

## Installation

> [!WARNING]
> - Windows: install the ZWO USB driver from [ZWO website > Software > Desktop App > Windows > Camera Driver](https://www.zwoastro.com/software/) before using the module.
> - macOS: libusb is required. Install via Homebrew: `brew install libusb`.
> - Linux: libusb is typically already available via your distribution packages.

### (Recommended) Using pip

The safest and easiest way to install up-to-date PyZWOASI is to use its repository from PyPI using `pip` :
```bash
pip install pyzwoasi
```

The installer will take in charge the machine configuration and choose the right compiled library files from ZWO. This means that you will not have useless `.dll` files on your machine, only the needed ones.

> [!NOTE]
> Only installation from `pip` is currently supported. Installation from `conda` or other package managers is not available at the moment but will come. If you do not want to use `pip`, please follow the instructions below to install from source.

### (Alternative) From source

If you want to be part of the development or simply if you want to install the module directly from the sources, you can also clone the repository and run pip from there:
```bash
git clone https://github.com/fmargall/pyzwoasi.git
cd pyzwoasi
pip install -e .
```

## Quick start

### First shot

```python
import pyzwoasi
from pyzwoasi import ZWOCamera

numOfConnectedCameras = pyzwoasi.getNumOfConnectedCameras()
if (numOfConnectedCameras == 0):
    print("No camera connected")
    exit()

for cameraIndex in range(numOfConnectedCameras):
    with ZWOCamera(cameraIndex) as camera:
        imageData = camera.shot(exposureTime_us = 1000) 
```

### Live view

```python
import pyzwoasi
from pyzwoasi import ZWOCamera

numOfConnectedCameras = pyzwoasi.getNumOfConnectedCameras()
if (numOfConnectedCameras == 0):
    print("No camera connected")
    exit()

for cameraIndex in range(numOfConnectedCameras):
    with ZWOCamera(cameraIndex) as camera:
        camera.liveView()
```

## Advanced usage

### High-level access (ZWOCamera class)

The `ZWOCamera` class provides a high-level interface to interact with ZWO ASI cameras. It encapsulates common operations such as connecting to the camera, capturing images, and starting live view sessions.

### Low-level access (Direct SDK function calls)

For advanced applications or scientific control, you can call the original ASI SDK functions directly. This is identical to the official C API, just wrapped for Python.

## Frequently Asked Questions (FAQ)

<details>
<summary>Why is my camera not detected?</summary>
If you are on Windows, make sure you have installed the ZWO ASI Camera driver, as explained in the Installation section of this README. On macOS, ensure `libusb` is installed (`brew install libusb`). If this is the case or if you are on Linux or MacOS, most of the time the problem comes from a bad USB port or cable. Please try to change USB port and/or cable, especially if you are using a USB cable extension, try to remove it.
</details>

## Contributing

Contributions are welcome! Whether you fix a bug, improve documentation, add support for new SDK functions, or propose new high-level APIs, feel free to open an issue or submit a pull request. 
Please follow the existing coding style and keep the project cross-platform.

### Contributors

<a href="https://github.com/fmargall/pyzwoasi/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fmargall/pyzwoasi" />
</a>


### Contact

François Margall - fr.margall@proton.me

## License

PyZWOASI is distributed under the MIT License. See `LICENSE.txt` for more information.