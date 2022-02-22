import os
import json
import time
import math
import functools
import logging
from typing import Any, Callable


import cv2
import numpy as np


from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QImage


from ..image import cv2_imread, cv2_putText


logging.basicConfig(level = logging.DEBUG)

def draw_pixmap(target_img_label : QLabel, pixmap : QPixmap) -> None:
    size = target_img_label.size()
    pixmap = pixmap.scaled(size)
    target_img_label.setPixmap(pixmap)

def draw_char_img(target_img_label : QLabel, char : str, font_scale = 20) -> None:
    label_size = target_img_label.size().toTuple()
    img = np.ndarray((*label_size[::-1], 3), np.uint8)
    img.fill(255)
    img = cv2_putText(img, char, (0, 0), font_scale, (0, 0, 0), 4, center=True)

    pixmap = numpy_to_pixmap(img)
    target_img_label.setPixmap(pixmap)

def numpy_to_pixmap(img : np.ndarray) -> QPixmap:
    h, w, c = img.shape
    if c == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    qimg = QImage(img.data, w, h, 3 * w, QImage.Format_BGR888)
    pixmap = QPixmap(qimg)
    return pixmap

def time_check(func) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        logging.debug(f"{func.__name__} : {time.perf_counter() - start_time:.3f}")
        return result

    return wrapper


def load_shape_img_info() -> tuple:
    cur_dir = os.path.dirname(__file__)
    shape_img_dir = os.path.join(cur_dir, "imgs", "shape_imgs")
    file_path = os.path.join(shape_img_dir, "desc.json")
    with open(file_path, "rb") as f:
        file_data = f.read()

    json_data = json.loads(file_data)

    childs = json_data["child"]
    parents = json_data["parent"]

    def load_helper(json_data : dict) -> dict:
        result_dict = dict()
        for key, value in json_data.items():
            img_path = os.path.join(shape_img_dir, value)
            img = cv2_imread(img_path)
            img = numpy_to_pixmap(img)
            result_dict[key] = img

        return result_dict

    child_img_dict = load_helper(childs)
    parent_img_dict = load_helper(parents)
    return child_img_dict, parent_img_dict


def load_question_info() -> list[dict]:
    cur_dir = os.path.dirname(__file__)
    question_info_path = os.path.join(cur_dir, "question_data.json")
    with open(question_info_path, "rb") as f:
        data = f.read()
        question_list = json.loads(data)

    return question_list


def get_degree(start : tuple[int, int], end : tuple[int, int]):
    start_x, start_y = start
    end_x, end_y = end
    dx = end_x - start_x
    dy = end_y - start_y
    degree = math.atan2(dy, dx) * (180.0 / math.pi) + 90
    degree = degree + 360 if degree < 0 else degree

    return int(degree)