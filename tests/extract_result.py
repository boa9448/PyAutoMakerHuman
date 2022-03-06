import os
import sys
import json
from glob import glob

import cv2
import numpy as np

from PySide6.QtWidgets import QApplication, QFileDialog

import env
from PyAutoMakerHuman import models_dir
from PyAutoMakerHuman.hand import HandResult
from PyAutoMakerHuman.hand_train import HandTrainer
from PyAutoMakerHuman.image import cv2_putText

file_rename_dict = {
    "ㄱ" : "giyeok.mp4"
    , "ㄴ" : "nieun.mp4"
    , "ㄷ" : "digeut.mp4"
    , "ㄹ" : "rieul.mp4"
    , "ㅁ" : "mieum.mp4"
    , "ㅂ" : "bieup.mp4"
    , "ㅅ" : "shiot.mp4"
    , "ㅇ" : "ieung.mp4"
    , "ㅈ" : "jieut.mp4"
    , "ㅊ" : "chieut.mp4"
    , "ㅋ" : "kiuek.mp4"
    , "ㅌ" : "tieut.mp4"
    , "ㅍ" : "pieup.mp4"
    , "ㅎ" : "hieut.mp4"
    , "ㅏ" : "a.mp4"
    , "ㅑ" : "ya.mp4"
    , "ㅓ" : "eo.mp4"
    , "ㅕ" : "yeo.mp4"
    , "ㅗ" : "o.mp4"
    , "ㅛ" : "yo.mp4"
    , "ㅜ" : "u.mp4"
    , "ㅠ" : "yu.mp4"
    , "ㅡ" : "eu.mp4"
    , "ㅣ" : "i.mp4"
    , "ㅐ" : "ae.mp4"
    , "ㅒ" : "yae.mp4"
    , "ㅔ" : "e.mp4"
    , "ㅖ" : "ye.mp4"
    , "ㅢ" : "ui.mp4"
    , "ㅚ" : "oe.mp4"
    , "ㅟ" : "wi.mp4"
    , "ㅘ" : "wa.mp4"
    , "ㅙ" : "wae.mp4"
    , "ㅝ" : "wo.mp4"
    , "ㅞ" : "we.mp4"
}

def get_working_dir() -> str:
    app = QApplication(sys.argv)
    window = QFileDialog(caption="영상이 있는 폴더 위치 선택")
    window.setFileMode(window.Directory)
    if window.exec():
        return window.selectedFiles()[0]


def main():

    working_dir = get_working_dir()
    if not working_dir:
        return

    util = HandTrainer()
    util.load(os.path.join(models_dir, "model"))


    target_dirs = glob(os.path.join(working_dir, "*"))
    for target_dir in target_dirs:
        print("=" * 50)
        vidios = glob(os.path.join(target_dir, "*.mp4"))
        for vidio in vidios:
            paths = vidio.split(os.path.sep)
            name, ext = paths[-1].split(".")
            new_name = file_rename_dict.get(name)
            if new_name:
                new_name = os.path.join(*paths[:-1], new_name)
                os.rename(vidio, new_name)

            cap = cv2.VideoCapture(vidio)
            if not cap.isOpened():
                raise RuntimeError(f"[{vidio}]를 여는데 실패했습니다")
            cap.release()

if __name__ == "__main__":
    main()