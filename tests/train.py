import os
import sys
from glob import glob
import logging
logging.basicConfig(level=logging.DEBUG)


import cv2
from PySide6.QtWidgets import QApplication, QFileDialog


import env
from PyAutoMakerHuman.hand import HandResult
from PyAutoMakerHuman.hand_train import HandTrainer
from PyAutoMakerHuman.image import cv2_putText, cv2_imwrite


def get_working_dir() -> str:
    app = QApplication(sys.argv)
    window = QFileDialog(caption="영상이 있는 폴더 위치 선택")
    window.setFileMode(window.Directory)
    if window.exec():
        return window.selectedFiles()[0].replace("/", os.path.sep)
    

def main():
    target_dir = get_working_dir()

    org_dir = os.path.join(target_dir, "original")
    mirror_dir = os.path.join(target_dir, "mirror")

    for data_dir, save_dir in [(org_dir, "model"), (mirror_dir, "mirror_model")]:
        train_dir = os.path.join(data_dir, "train")
        util = HandTrainer()
        util.train(train_dir)
        util.save(save_dir)

    print("done")
    

if __name__ == "__main__":
    main()
