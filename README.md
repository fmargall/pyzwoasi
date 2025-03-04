# PyZWOASI

<p align="center">
  <a href="https://www.zwoastro.com/software/">
    <img src="https://img.shields.io/badge/Supported_ASI_SDK_Version-1.37-blue" alt="Supported ASI SDK version : 1.37">
  </a>
</p>

PyZWOASI is a Python binding for the ZWO ASI SDK. No other Python packages or dependencies are required. 

## Installation

The safest and simplest way to install `pyzwoasi` is to use its repository from PyPI using `pip` : 

```
python -m pip install --upgrade pip
python -m pip install pyzwoasi
```

The installer will take in charge the machine configuration and choose the right compiled library file from ZWO. You will not have useless `.dll` files on your machine, only the needed ones.

## Roadmap
- [x] Add Linux support
- [ ] Add MacOS support
- [ ] Add Android support
- [ ] Add more precise error handling
- [ ] Add missing functions from the ZWO ASI SDK

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact
François Margall - fr.margall@proton.me
