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

from . import proc
from .form.study_form import Ui_Frame
from .utils import draw_pixmap, numpy_to_pixmap, draw_char_img
from .. import hand_lang
from ..image import cv2_imread

logging.basicConfig(level=logging.DEBUG)

class StudyWindow(QFrame, Ui_Frame):
    QUESTION_DEFAUL = "ㄱ"

    def __init__(self, parent, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]):
        super(StudyWindow, self).__init__(parent)
        self.setupUi(self)
        self._img_label_list = [self.screen_img_label, self.answer_img_label, self.example_img_label
                                , self.study_img_label, self.direction_img_label]

        self.last_changed_combobox = self.char_child_combo
        self.study_thread = None
        self._mirror_mode = True
        self._questions = self.QUESTION_DEFAUL
        self._cameras = cameras

    def __del__(self):
        self.dispose_data()

    def init(self) -> None:
        self.init_display()
        self.init_handler()

    def load_shape_img_info(self) -> tuple:
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

    def load_arrow_imgs(self) -> tuple[QPixmap, QPixmap]:
        cur_dir = os.path.dirname(__file__)
        img_dir = os.path.join(cur_dir, "imgs")
        ccw_path = os.path.join(img_dir, "CCW.png")
        cw_path = os.path.join(img_dir, "CW.png")

        ccw_img = cv2.cvtColor(cv2_imread(ccw_path), cv2.COLOR_BGRA2BGR)
        cw_img = cv2.cvtColor(cv2_imread(cw_path), cv2.COLOR_BGRA2BGR)

        ccw_pixmap = numpy_to_pixmap(ccw_img)
        cw_pixmap = numpy_to_pixmap(cw_img)

        return ccw_pixmap, cw_pixmap

    def init_display(self) -> None:            
        child, parent = self.load_shape_img_info()
        self.CHAR_CHILD_COMBO_DICT : dict = child
        self.CHAR_PARENT_COMBO_DICT : dict = parent

        pixmaps = self.load_arrow_imgs()
        self.ccw_pixmap = pixmaps[0]
        self.cw_pixmap = pixmaps[1]

        self.char_child_combo.addItems(list(self.CHAR_CHILD_COMBO_DICT.keys()))
        self.char_parent_combo.addItems(list(self.CHAR_PARENT_COMBO_DICT.keys()))

        for img_label in self._img_label_list:
            rect = img_label.rect()
            width = rect.width()
            height = rect.height()

            pixmap = QPixmap(QSize(width, height))
            pixmap.fill(QColor(255, 255, 255))
            img_label.setPixmap(pixmap)
            img_label.setScaledContents(True)

    def init_handler(self) -> None:
        self.char_child_combo.currentIndexChanged.connect(self.char_combo_change_handler)
        self.char_parent_combo.currentIndexChanged.connect(self.char_combo_change_handler)
        self.reset_button.clicked.connect(self.reset_button_clicked_handler)
        self.reset_button.click()

    def init_data(self) -> None:
        self.study_thread = proc.WorkThread(self._cameras, proc.RUN_STUDY
                                            , front_draw_handler = self.front_draw_handler
                                            , answer_handler = self.answer_handler
                                            , direction_hander = self.direction_hander)
                                            
        self.study_thread.mirror_mode = self.mirror_mode
        self.study_thread.questions = self._questions
        self.study_thread.start()

    def dispose_data(self) -> None:
        if self.study_thread:
            self.study_thread.join()

    def showEvent(self, event: QShowEvent) -> None:
        self.init_data()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.dispose_data()
        return super().hideEvent(event)

    @Slot(QPixmap)
    def front_draw_handler(self, pixmap) -> None:
        self.screen_img_label.setPixmap(pixmap)

    @Slot(int)
    def answer_handler(self, code : int) -> None:
        char_dict = {proc.ANSWER_FAIL : "X", proc.ANSWER_PROCESSING : "△", proc.ANSWER_SUCCESS : "O"}
        char = char_dict.get(code, "")
        draw_char_img(self.answer_img_label, char, 10)

    @Slot(int)
    def direction_hander(self, code : int) -> None:
        shape_dict = {proc.DIRECTION_NONE : "O", proc.DIRECTION_LEFT : "왼", proc.DIRECTION_RIGHT : "오"}
        shape = shape_dict.get(code, "")
        if code == proc.DIRECTION_NONE:
            draw_char_img(self.direction_img_label, "O", 10)
        elif code == proc.DIRECTION_LEFT:
            draw_pixmap(self.direction_img_label, self.ccw_pixmap)
        elif code == proc.DIRECTION_RIGHT:
            draw_pixmap(self.direction_img_label, self.cw_pixmap)
        

    @Slot(int)
    def char_combo_change_handler(self, idx : int) -> None:
        if self.sender() == self.char_child_combo:
            self.last_changed_combobox = self.char_child_combo
        elif self.sender() == self.char_parent_combo:
            self.last_changed_combobox = self.char_parent_combo

        char = self.last_changed_combobox.currentText()
        draw_char_img(self.study_img_label, char)

        target_dict = dict()
        if self.last_changed_combobox == self.char_child_combo:
            target_dict = self.CHAR_CHILD_COMBO_DICT
        elif self.last_changed_combobox == self.char_parent_combo:
            target_dict = self.CHAR_PARENT_COMBO_DICT
        
        img = target_dict.get(char)
        if img:
            self.example_img_label.setPixmap(img)

        if self.study_thread:
            self.study_thread.questions = char
            
        self._questions = char

    @Slot()
    def reset_button_clicked_handler(self) -> None:
        cur_idx = self.last_changed_combobox.currentIndex()
        self.char_combo_change_handler(cur_idx)
        if self.study_thread:
            self.study_thread.reset()

    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.study_img_label.width()
        height = width
        pixmap = self.study_img_label.pixmap()
        pixmap = pixmap.scaled(width, height)
        self.study_img_label.setPixmap(pixmap)

        return super().resizeEvent(event)

    @property
    def mirror_mode(self) -> bool:
        return self._mirror_mode

    @mirror_mode.setter
    def mirror_mode(self, value : bool) -> None:
        self._mirror_mode = value
        if self.study_thread:
            self.study_thread.mirror_mode = value

    