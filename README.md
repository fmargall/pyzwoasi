# PyZWOASI

<p align="center">
  <a href="https://www.zwoastro.com/software/">
    <img src="https://img.shields.io/badge/Supported_ASI_SDK_Version-1.37-blue" alt="Supported ASI SDK version : 1.37">
  </a> <br>
  <a href="https://www.microsoft.com/windows/">
    <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows compatible">
  </a> 
  &ensp;
  <a href="https://www.kernel.org/">
    <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux compatible">
  </a>
  &ensp;
  <a href="https://www.apple.com/macos/">
    <img src="https://img.shields.io/badge/MacOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="MacOS compatible">
  </a>
</p>

PyZWOASI is a Python binding for the ZWO ASI SDK. No other Python packages or dependencies are required. Windows and Linux compatible.

## Installation

The safest and simplest way to install `pyzwoasi` is to use its repository from PyPI using `pip` : 

```
python -m pip install --upgrade pip
python -m pip install pyzwoasi
```

The installer will take in charge the machine configuration and choose the right compiled library file from ZWO. You will not have useless `.dll` files on your machine, only the needed ones.

## Roadmap

<p align="center">
    <img src=https://geps.dev/progress/60 alt="60%"><br>
    <sup>Current number of supported ASI SDK v1.37 features: 26/43
</p>

- [x] Add Linux support
- [x] Add MacOS support
- [ ] Add Android support
- [ ] Add more precise error handling
- [ ] Add missing functions from the ZWO ASI SDK

If you have any wishes, suggestions, comments or advice, please feel free to [create an issue](https://github.com/fmargall/pyzwoasi/issues) or contact me directly.

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact
François Margall - fr.margall@proton.me
