import os
from glob import glob

import cv2
import numpy as np
import imutils

cur_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(cur_dir, ".."))
dataset_dir = os.path.join(parent_dir, "dataset", "not_mirror")
folder_list = glob(os.path.join(dataset_dir, "*"))

flip_except_classese = ["ㅓ", "ㅕ", "ㅔ", "ㅖ"]


def cv2_imread(filename : str, flags : int = cv2.IMREAD_COLOR) -> np.ndarray:
    raw = np.fromfile(filename, np.uint8)
    img = cv2.imdecode(raw, flags)

    return img


def cv2_imwrite(filename : str, img : np.ndarray, params : list = None):
    ext = os.path.splitext(filename)[1]
    ret, raw_img = cv2.imencode(ext, img, params)
    if ret:
        with open(filename, "w+b") as f:
            raw_img.tofile(f)


for folder in folder_list:
    class_name = folder.split(os.path.sep)[-1]
    if class_name in flip_except_classese:
        continue

    img_path_list = glob(os.path.join(folder, "*.*"))
    for img_path in img_path_list:
        img = cv2_imread(img_path)
        img = cv2.flip(img, 1)
        cv2_imwrite(img_path, img)