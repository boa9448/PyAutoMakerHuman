import cv2
import numpy as np

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QHideEvent, QShowEvent, QPixmap

from . import proc
from .form.test_form import Ui_Frame

class TestWindow(QFrame, Ui_Frame):
    def __init__(self, parent, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]):
        super(TestWindow, self).__init__(parent)
        self.setupUi(self)

        self._cameras = cameras
        self.test_thread : proc.WorkThread = None
        self._mirror_mode = True
        self._questions = "게두링"

    def init_data(self) -> None:
        self.test_thread = proc.WorkThread(self._cameras, proc.RUN_TEST
                                            , front_draw_handler = self.front_draw_handler
                                            , process_handler = self.process_handler)

        self.test_thread.mirror_mode = self.mirror_mode
        self.test_thread.questions = self._questions
        self.test_thread.start()

    def dispose_data(self) -> None:
        if self.test_thread:
            self.test_thread.join()
            self.test_thread = None

    def init_handler(self) -> None:
        self.start_button.clicked.connect(self.start_button_handler)

    def init_display(self) -> None:
        pass

    def init(self) -> None:
        self.init_handler()
        self.init_display()

    @Slot()
    def start_button_handler(self) -> None:
        if self.test_thread:
            self.dispose_data()
            button_text = "시작"
        else:
            self.init_data()
            button_text = "중지"

        self.start_button.setText(button_text)

    @Slot(QPixmap)
    def front_draw_handler(self, pixmap : QPixmap) -> None:
        self.screen_img_label.setPixmap(pixmap)

    @Slot(int)
    def process_handler(self, remaining_time : int) -> None:
        pass

    def showEvent(self, event: QShowEvent) -> None:
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
        if self.test_thread:
            self.test_thread.mirror_mode = value

    