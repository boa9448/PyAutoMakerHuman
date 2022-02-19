import cv2
import numpy as np

from PySide6.QtWidgets import QFrame

from .form.test_form import Ui_Frame

class TestWindow(QFrame, Ui_Frame):
    def __init__(self, parernt, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]):
        super(TestWindow, self).__init__()
        self.setupUi(self)

    