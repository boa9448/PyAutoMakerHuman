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

    def __del__(self):
        pass

    def init_data(self):
        self.log_signal : LogSignal = self.parent.log_signal