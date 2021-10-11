#수정 해야함, 그냥 카피떴음

import setuptools
import os
import sys
import site
from os.path import dirname
from glob import glob

with open("README.md", "rt", encoding="utf-8") as fh:
    long_description = fh.read()

data_files_path = ""

if sys.platform == "nt":
    data_files_path = os.path.join("lib", "site-packages")

#라즈베리파이와 일반 데스크톱 리눅스를 지원할 수 있도록 나눌것
elif sys.platform == "linux":
    version = "python{}.{}".format(sys.version_info[0], sys.version_info[1])
    data_files_path = os.path.join(site.USER_BASE, "lib", version, "site-packages")

setuptools.setup(
    name="PyAutoMakerHuman",
    version="1.1.0",
    author="WDW",
    author_email="boa3465@gmail.com",
    description="얼굴, 포즈, 손의 랜드마크를 쉽게 가져오기위한 모듈",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boa9448/PyAutoMakerHuman",
    project_urls={
        "Bug Tracker": "https://github.com/boa9448/PyAutoMakerHuman/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ],
    packages=["PyAutoMakerHuman"],
    data_files=[(os.path.sep.join([data_files_path, "PyAutoMakerHuman", "models"])
                 , [file for file in glob("PyAutoMakerHuman\\models\\*.*")])],

    install_requires = ["imutils", "scikit-learn", "waitress", "flask", "requests"
    , "mediapipe; platform_system == 'Windows'", "mediapipe-rpi4; platform_system == 'Linux'"
    , "tensorflow; platform_system == 'Windows'", "PySide6"],
    python_requires=">=3.6",
)

