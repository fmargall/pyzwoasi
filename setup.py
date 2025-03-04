import os, platform, re

from setuptools import setup, find_packages


def getVersion():
    versionNs = {}
    with open("pyzwoasi/__version__.py") as f:
        return re.search(r'__version__ = "(.*?)"', f.read()).group(1)


def getDllFiles():
    system = platform.system()
    arch = platform.architecture()[0]
    if system == 'Windows':
        if arch == '64bit':
            dllPath = 'pyzwoasi/lib/Windows/x64/ASICamera2.dll'
        else:
            dllPath = 'pyzwoasi/lib/Windows/x86/ASICamera2.dll'
    elif system == 'Linux':
        if arch == '64bit':
            dllPath = 'pyzwoasi/lib/Linux/x64/libASICamera2.so.1.37'
        else:
            dllPath = 'pyzwoasi/lib/Linux/x86/libASICamera2.so.1.37'
    else:
        raise ValueError(f"Unsupported system: {system}")

    return [(os.path.join('lib', system, arch), [dllPath])]


setup(
    name='pyzwoasi',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    version=getVersion(),
    packages=find_packages(),
    data_files=getDllFiles(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
	    'Development Status :: 3 - Alpha',
	    'License :: OSI Approved :: MIT License',
	    'Operating System :: Microsoft :: Windows',
    ],
    long_description=open('README.md', encoding='utf-8').read(),
)