import os

import cv2
import numpy as np

from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QHideEvent, QShowEvent, QPixmap, QColor

from .form.conversation_form import Ui_Frame

class ConversationWindow(QFrame, Ui_Frame):
    def __init__(self, parent, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]):
        super(ConversationWindow, self).__init__(parent)
        self.setupUi(self)