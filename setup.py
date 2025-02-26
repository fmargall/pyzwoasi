import os, platform

from setuptools import setup, find_packages


def getDataFiles():
    arch = platform.architecture()[0]
    if arch == '64bit':
        dllPath = 'src/lib/x64/ASICamera2.dll'
    else:
        dllPath = 'src/lib/x86/ASICamera2.dll'
    return [(os.path.join('lib', arch), [dllPath])]

setup(
    name='pyzwoasi',
    version='0.1.0-prealpha',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    data_files=get_data_files(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Private :: Do Not Upload',
	    'Development Status :: 3 - Alpha',
	    'License :: OSI Approved :: MIT License',
	    'Operating System :: Microsoft :: Windows',
    ],
)