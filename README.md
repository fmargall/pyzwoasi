![Header](./docs/pyzwoasi-header.png)

# PyZWOASI &middot; <img src="https://github.com/fmargall/pyzwoasi/actions/workflows/deployment.yml/badge.svg" alt="Build status"> <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"> <a href="https://github.com/qoomon/starlines"> <img src="https://starlines.qoo.monster/assets/fmargall/pyzwoasi" align="right" alt="Starline counter"/> </a>

PyZWOASI is a Python binding for the ZWO ASI SDK. It is developped to be easy-to-use and functional, and, if I can make it, up-to-date.

<p align="center">
  <a href="https://www.zwoastro.com/software/">
    <img src="https://img.shields.io/badge/Supported_ASI_SDK_Version-1.37-blue" alt="Supported ASI SDK version : 1.37">
  </a>
</p>

Currently compatible with Windows, Linux and MacOS.

<p align="center">
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

## Installation

The safest and simplest way to install `pyzwoasi` is to use its repository from PyPI using `pip` : 

```
python -m pip install --upgrade pip
python -m pip install pyzwoasi
```

The installer will take in charge the machine configuration and choose the right compiled library file from ZWO. You will not have useless `.dll` files on your machine, only the needed ones.

## Roadmap

<p align="center">
    <img src=https://geps.dev/progress/90 alt="90%"><br>
    <sup>Current number of supported ASI SDK v1.37 features: 39/43
</p>

- [x] Add Linux support
- [x] Add MacOS support
- [ ] Add Android support
- [x] Add more precise error handling
- [ ] Add missing functions from the ZWO ASI SDK
  - [ ] Add function `ASIGetVideoDataGPS`
  - [ ] Add function `ASIGetDataAfterExpGPS`
  - [ ] Add function `ASISetTriggerOutputIOConf`
  - [ ] Add function `ASIGPSGetData`

If you have any wishes, suggestions, comments or advice, please feel free to [create an issue](https://github.com/fmargall/pyzwoasi/issues) or contact me directly.

### Code quality

This Python project will also be a test of different codings metrics and tools to ensure its quality and security. This part is more a personal challenge and journey into new metrics and Python tools.

- [ ] Computing code coverage using `coverage`
- [ ] Static code analysis using `pylint`
- [ ] Style guide enforcement using `black` or `flake8`
- [ ] Writing a Git best practices charter for the project (atomic commits and explicits like `feat:`, `fix:`, `refactor:` and so on. More about this about [here](https://medium.com/@noriller/docs-conventional-commits-feat-fix-refactor-which-is-which-531614fcb65a) and [here](https://www.conventionalcommits.org/en/v1.0.0/))
- [ ] Writing a security charter, using `bandit` and `safety` to ensure the code is secure
- [ ] Making large documentation using `sphinx`, `readthedocs` and proposing metrics with `docstr-coverage`
- [ ] Profiling the code with `cProfile` and `line_profiler`
- [ ] Various other code metrics with `radon` and `mccabe`
- [ ] Adding build status badges and SonarQube badges
- [ ] and lots of other things proposed by [other repos](https://github.com/dwyl/repo-badges)

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contributors

<a href="https://github.com/fmargall/pyzwoasi/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fmargall/pyzwoasi" />
</a>

## Contact
François Margall - fr.margall@proton.me
