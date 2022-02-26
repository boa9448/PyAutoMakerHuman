import setuptools

with open("README.md", "rt", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyAutoMakerHuman",
    version="1.2.1",
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
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"PyAutoMakerHuman": ["models/*", "gui/datas/*"]},

    install_requires = ["opencv-contrib-python", "imutils", "scikit-learn"
                        ,"requests", "mediapipe", "PySide6", "qt-material"],
    python_requires=">=3.8",
)

