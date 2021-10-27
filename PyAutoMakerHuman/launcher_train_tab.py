import os
import sys
import time
import random
from threading import Thread, Event
from glob import glob
from typing import List

import cv2
import numpy as np
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from main_form import Ui_Form
# 테스트 개발엔 잠시 주석
import face
import hand
import pose
import train
from custom_signal import LogSignal, CamSignal, WorkDoneSignal
from thread import WorkThread, WorkQThread, WorkPyThread
from image import cv2_imread


class TrainTab:
    parent = None

    def __init__(self, parent):
        TrainTab.parent = parent
        self.init_data()
        self.init_display()

    def __del__(self):
        pass

    def init_data(self) -> None:
        self.log_signal : LogSignal = self.parent.log_signal

        self.train_dataset_add_end_signal = WorkDoneSignal()
        self.train_dataset_add_thread = None

        self.train_done_signal = WorkDoneSignal()

        min_thresh = self.parent.train_thresh_spin_edit.text()
        min_thresh = float(min_thresh) / 100
        self.train_detector = self.parent.init_detector(0, min_thresh)
        self.train_trainer = train.SvmUtil()

    def init_display(self) -> None:
        for model_type in self.parent.TRAIN_TEST_TYPE_DICT:
            self.parent.train_type_combo.addItem(model_type)

            # 잠시 숨김
            self.parent.train_two_hand_checkBox.hide()
