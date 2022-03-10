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
from PyAutoMakerHuman.image import cv2_imread, cv2_putText


def get_working_dir() -> str:
    app = QApplication(sys.argv)
    window = QFileDialog(caption="영상이 있는 폴더 위치 선택")
    window.setFileMode(window.Directory)
    if window.exec():
        return window.selectedFiles()[0]

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


    org_dir = os.path.join(working_dir, "original")
    mirror_dir = os.path.join(working_dir, "mirror")

    for target_dir, model_path in [(org_dir, "model"), (mirror_dir, "mirror_model")]:
        util = HandTrainer()
        util.load(model_path)

        result_file = ResultFile(os.path.join(target_dir, "result.csv"))
        img_paths = glob(os.path.join(target_dir, "validate", "**", "*.jpg"), recursive=True)
        for idx, img_path in enumerate(img_paths):
            class_name = img_path.split(os.path.sep)[-2]
            img = cv2_imread(img_path)
            result = util.predict(img)
            if result:
                hand_result : HandResult = result[0]
                predict_result = result[1]
                
                boxes = hand_result.get_boxes()
                for (hand_label, box), (name, proba) in zip(boxes, predict_result):
                    x, y, w, h = box
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    img =cv2_putText(img, f"{hand_label}_{name} __ {proba:0.2f}", (x, y - 15), 3, (0, 0, 255), 2)
                    result_file(class_name, idx, name, proba)

        result_file._file.flush()

if __name__ == "__main__":
    main()