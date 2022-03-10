import os
import sys
import random
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
    classe_dirs = glob(os.path.join(target_dir, "*"))

    validate_dir = os.path.join(target_dir, "validate")
    os.mkdir(validate_dir)

    train_dir = os.path.join(target_dir, "train")
    os.mkdir(train_dir)

    for dir_name in classe_dirs:
        if not os.path.isdir(dir_name):
            continue
        
        class_name = dir_name.split(os.path.sep)[-1]

        train_dir_name = os.path.join(train_dir, class_name)
        validate_dir_name = os.path.join(validate_dir, class_name)
        print(train_dir_name, validate_dir_name)

        imgs = glob(os.path.join(dir_name, "*.jpg"))
        random.shuffle(imgs)
        imgs_len = len(imgs)
        train_count = int(imgs_len * 0.7)

        train_imgs = imgs[:train_count]
        validate_imgs = imgs[train_count:]

        print(f"train : {len(train_imgs)}")
        print(f"validate : {len(validate_imgs)}")
        
        for target_dir, imgs in zip([train_dir_name, validate_dir_name], [train_imgs, validate_imgs]):
            os.mkdir(target_dir)
            for img in imgs:
                file_name = os.path.split(img)[-1]
                new_path = os.path.join(target_dir, file_name)
                os.rename(img, new_path)

if __name__ == "__main__":
    main()