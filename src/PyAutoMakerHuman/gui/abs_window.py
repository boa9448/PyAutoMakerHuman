from abc import abstractmethod, ABCMeta
import os

import cv2
import numpy as np

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QHideEvent, QShowEvent, QPixmap, QColor

class ABSWindow(ABCMeta, type(QFrame)):
    def __init__(self, parent):
        super(ABSWindow, self).__init__(parent)

        self._mirror_mode = True
        self._work_thread = None

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

    def showEvent(self, event: QShowEvent) -> None:
        self.init_data()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.dispose_data()
        return super().hideEvent(event)

    @property
    def mirror_mode(self) -> bool:
        return self._mirror_mode

    @mirror_mode.setter
    def mirror_mode(self, value : bool) -> None:
        self._mirror_mode = value
        if self._work_thread:
            self._work_thread.mirror_mode = value