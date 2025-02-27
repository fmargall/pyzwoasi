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
    version='0.1.0-alpha',
    packages=find_packages(),
    data_files=getDataFiles(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
	    'Development Status :: 3 - Alpha',
	    'License :: OSI Approved :: MIT License',
	    'Operating System :: Microsoft :: Windows',
    ],
    long_description=open('README.md', encoding='utf-8').read(),
)