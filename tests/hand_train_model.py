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

mirror_except_list = ["ㅓ", "ㅕ", "ㅔ", "ㅖ"]

def get_working_dir() -> str:
    app = QApplication(sys.argv)
    window = QFileDialog(caption="영상이 있는 폴더 위치 선택")
    window.setFileMode(window.Directory)
    if window.exec():
        return window.selectedFiles()[0].replace("/", os.path.sep)

def get_key(target_item : str) -> str or None:
    for key, value in file_rename_dict.items():
        if target_item == value:
            return key

    return None


def main():
    target_dir = get_working_dir()
    videos = glob(os.path.join(target_dir, "*.mp4"))

    original_dir = os.path.join(target_dir, "origianl")
    os.path.isdir(original_dir) or os.mkdir(original_dir)

    mirror_dir = os.path.join(target_dir, "mirror")
    os.path.isdir(mirror_dir) or os.mkdir(mirror_dir)

    """for video in videos:
        org_name = video.split(os.path.sep)[-1]
        han_name = get_key(org_name)
        if not han_name:
            raise RuntimeError(f"{org_name} 비디오 이름 확인하셈")


        original_frame_dir = os.path.join(original_dir, han_name)
        os.path.isdir(original_frame_dir) or os.mkdir(original_frame_dir)

        mirror_frame_dir = os.path.join(mirror_dir, han_name)
        os.path.isdir(mirror_frame_dir) or os.mkdir(mirror_frame_dir)

        cap = cv2.VideoCapture(video)
        if not cap.isOpened():
            raise RuntimeError(f"{video}를 열 수 없습니다.")

        idx = 0
        while True:
            success, frame = cap.read()
            if not success:
                break

            cv2_imwrite(os.path.join(original_frame_dir, f"{idx}.jpg"), frame)
            if not han_name in mirror_except_list:
                frame = cv2.flip(frame, 1)
            cv2_imwrite(os.path.join(mirror_frame_dir, f"{idx}.jpg"), frame)

            print(f"{han_name} {idx} ... save")
            idx += 1

        cap.release()

    print("프레임을 모두 저장했습니다")"""

    train_dict = [(original_dir, "model"), (mirror_dir, "mirror_model")]
    for dataset, save_path in train_dict:
        util = HandTrainer()
        util.train(dataset)
        util.save(save_path)

    print("done")


if __name__ == "__main__":
    main()