import os
import sys
import json
from glob import glob
from typing import Any

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

def get_key(target_item : str) -> str or None:
    for key, value in file_rename_dict.items():
        if target_item == value:
            return key

    return None

def change_eng_name(file_path : str) -> str:
    paths = file_path.split(os.path.sep)
    name, ext = paths[-1].split(os.path.extsep)

    new_name = file_rename_dict.get(name)
    if new_name:
        new_path = os.path.join(*paths[:-1], new_name)
        os.rename(file_path, new_path)
        return new_path

    return file_path

class ResultFile:
    def __init__(self, file_path : str) -> None:
        self._file = open(file_path, "wt", encoding="utf-8")
        if self._file.closed:
            raise RuntimeError("파일을 열 수 없습니다")
    
    def __del__(self) -> None:
        print(f"{self._file.name} done")
        self._file.close()

    def __call__(self, file_name :str, frame_idx : int, label : str, proba : float) -> Any:
        line = f"{file_name}, {frame_idx}, {label}, {proba}\n"
        print(line)
        self._file.write(line)


def main():

    working_dir = get_working_dir()
    if not working_dir:
        return

    util = HandTrainer()
    util.load(os.path.join(models_dir, "model"))


    target_dirs = glob(os.path.join(working_dir, "*"))
    for target_dir in target_dirs:
        print("=" * 50)
        videos = glob(os.path.join(target_dir, "*.mp4"))
        videos = [change_eng_name(path) for path in videos]

        result_file = ResultFile(os.path.join(target_dir, "result.csv"))
        for video in videos:
            org_name = video.split(os.path.sep)[-1]
            han_name = get_key(org_name)
            if not han_name:
                raise RuntimeError(f"{org_name} 비디오 이름 확인하셈")
            cap = cv2.VideoCapture(video)
            if not cap.isOpened():
                raise RuntimeError(f"[{video}]를 여는데 실패했습니다")

            frame_idx = 0
            while True:
                success, frame = cap.read()
                if not success:
                    break

                result = util.predict(frame)
                if result:
                    hand_result : HandResult = result[0]
                    predict_result = result[1]
                    
                    boxes = hand_result.get_boxes()
                    for (hand_label, box), (name, proba) in zip(boxes, predict_result):
                        x, y, w, h = box
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        frame =cv2_putText(frame, f"{hand_label}_{name} __ {proba:0.2f}", (x, y - 15), 3, (0, 0, 255), 2)
                        result_file(han_name, frame_idx, name, proba)

                frame_idx += 1

            result_file._file.flush()
            cap.release()

if __name__ == "__main__":
    main()