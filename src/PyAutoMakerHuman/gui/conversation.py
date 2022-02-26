import os

import cv2
import numpy as np

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QHideEvent, QShowEvent, QPixmap, QColor


from .abs_window import ABSWindow
from .form.conversation_form import Ui_Frame


class ConversationWindow(ABSWindow , Ui_Frame):
    def __init__(self, parent, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]):
        super(ConversationWindow, self).__init__(parent)
        self.setupUi(self)

    def init(self) -> None:
        self.init_display()
        self.init_handler()

    def init_display(self) -> None:            
        pass

    def init_handler(self) -> None:
        pass

    def init_data(self) -> None:
        pass

    def dispose_data(self) -> None:
        pass