import os
import logging
import time
import json
from threading import Thread, Event, Lock

import cv2
import numpy as np
from PySide6.QtCore import QSize, Slot, QObject, Signal
from PySide6.QtWidgets import QFrame, QComboBox, QLabel
from PySide6.QtGui import QPixmap, QColor, QResizeEvent, QShowEvent, QHideEvent

from .form.study_form import Ui_Frame
from .utils import numpy_to_pixmap
from .. import hand_lang
from ..image import cv2_imread, cv2_putText

logging.basicConfig(level=logging.DEBUG)

class StudyWindow(QFrame, Ui_Frame):
    def __init__(self, parernt, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]):
        super(StudyWindow, self).__init__(parernt)
        self.setupUi(self)
        self.img_label_list = [self.screen_img_label, self.shape_img_label, self.study_img_label, self.direction_img_label]
        self.mirror_mode = True
        self.cameras = cameras

    def __del__(self):
        self.dispose_data()

    def init(self) -> None:
        self.init_handler()
        self.init_display()

    def init_handler(self) -> None:
        self.char_child_combo.currentIndexChanged.connect(self.char_combo_change_handler)
        self.char_parent_combo.currentIndexChanged.connect(self.char_combo_change_handler)
        self.reset_button.clicked.connect(self.reset_button_clicked_handler)

    def load_img_info(self) -> tuple:
        cur_dir = os.path.dirname(__file__)
        img_dir = os.path.join(cur_dir, "imgs")
        file_path = os.path.join(img_dir, "desc.json")
        with open(file_path, "rb") as f:
            file_data = f.read()

        json_data = json.loads(file_data)

        childs = json_data["child"]
        parents = json_data["parent"]

        def load_helper(json_data : dict) -> dict:
            result_dict = dict()
            for key, value in json_data.items():
                img_path = os.path.join(img_dir, value)
                img = cv2_imread(img_path)
                img = numpy_to_pixmap(img)
                result_dict[key] = img

            return result_dict

        child_img_dict = load_helper(childs)
        parent_img_dict = load_helper(parents)
        return child_img_dict, parent_img_dict

    def init_display(self) -> None:            
        child, parent = self.load_img_info()
        self.CHAR_CHILD_COMBO_DICT : dict = child
        self.CHAR_PARENT_COMBO_DICT : dict = parent

        self.char_child_combo.addItems(list(self.CHAR_CHILD_COMBO_DICT.keys()))
        self.char_parent_combo.addItems(list(self.CHAR_PARENT_COMBO_DICT.keys()))

        for img_label in self.img_label_list:
            rect = img_label.rect()
            width = rect.width()
            height = rect.height()

            pixmap = QPixmap(QSize(width, height))
            pixmap.fill(QColor(255, 255, 255))
            img_label.setPixmap(pixmap)
            img_label.setScaledContents(True)

    def init_data(self) -> None:
        self.set_answer("ㄱ")
        self.last_changed_combobox = self.char_child_combo

    def dispose_data(self) -> None:
        pass

    def showEvent(self, event: QShowEvent) -> None:
        self.init_data()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.dispose_data()
        return super().hideEvent(event)

    @Slot(int, QPixmap, str)
    def draw_signal_handler(self, code : int, pixmap : QPixmap, answer_char : str, answer_direction : str) -> None:
        self.screen_img_label.setPixmap(pixmap)
        if answer_char:
            self.draw_char_img(self.shape_img_label, answer_char, 10)

        if answer_direction:
            self.draw_char_img(self.direction_img_label, answer_direction, 10)

    def draw_char_img(self, target_img_label : QLabel, char : str, font_scale = 20) -> None:
        label_size = target_img_label.size().toTuple()
        img = np.ndarray((*label_size[::-1], 3), np.uint8)
        img.fill(255)
        img = cv2_putText(img, char, (0, 0), font_scale, (0, 0, 0), 4, center=True)

        pixmap = numpy_to_pixmap(img)
        target_img_label.setPixmap(pixmap)

    @Slot(int)
    def char_combo_change_handler(self, idx : int) -> None:
        if self.sender() == self.char_child_combo:
            self.last_changed_combobox = self.char_child_combo
        elif self.sender() == self.char_parent_combo:
            self.last_changed_combobox = self.char_parent_combo

        char = self.last_changed_combobox.currentText()
        self.draw_char_img(self.study_img_label, char)
        self.set_answer(char)

    @Slot()
    def reset_button_clicked_handler(self) -> None:
        cur_idx = self.last_changed_combobox.currentIndex()
        self.char_combo_change_handler(cur_idx)

    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.study_img_label.width()
        height = width
        pixmap = self.study_img_label.pixmap()
        pixmap = pixmap.scaled(width, height)
        self.study_img_label.setPixmap(pixmap)

        return super().resizeEvent(event)

    def set_mirror_mode(self, mirror_mode : bool) -> None:
        self.mirror_mode = mirror_mode

    def get_mirror_mode(self) -> bool:
        return self.mirror_mode

    def set_answer(self, answer : str) -> None:
        pass