import cv2
import numpy as np

from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QHideEvent, QShowEvent, QPixmap, QColor

from . import proc
from .utils import draw_pixmap, load_shape_img_info, load_question_info, numpy_to_pixmap, draw_char_img
from .form.test_form import Ui_Frame

class TestWindow(QFrame, Ui_Frame):
    def __init__(self, parent, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]):
        super(TestWindow, self).__init__(parent)
        self.setupUi(self)

        self._cameras = cameras
        self._test_thread : proc.WorkThread = None
        self._mirror_mode = True
        self._run_status = False
        self._question_list = load_question_info()
        
        child, parent = load_shape_img_info()
        child.update(parent)
        self.CHAR_COMBO_DICT : dict = child

    def init_data(self) -> None:
        self._timer = QTimer()
        self._question_success_count = 0
        self._question_fail_count = 0
        self._test_thread = proc.WorkThread(self._cameras, proc.RUN_TEST
                                            , front_draw_handler = self.front_draw_handler
                                            , process_handler = self.process_handler)

        self._test_thread.mirror_mode = self.mirror_mode
        self._test_thread.stop_work()
        self._test_thread.start()

    def dispose_data(self) -> None:
        self._timer.stop()
        if self._test_thread:
            self._test_thread.join()
            self._test_thread = None

    def init_handler(self) -> None:
        self.start_button.clicked.connect(self.start_button_handler)

    def init_display(self) -> None:
        self.screen_img_label.setScaledContents(True)
        self.char_img_label.setScaledContents(True)
        pixmap = QPixmap(200, 200)
        pixmap.fill(QColor(255, 255, 255))
        draw_pixmap(self.screen_img_label, pixmap)
        draw_pixmap(self.question_img_label, pixmap)
        draw_pixmap(self.char_img_label, pixmap)

        self.success_count_img_label.setText("0개")
        self.fail_count_img_label.setText("0개")

    def init(self) -> None:
        self.init_handler()
        self.init_display()

    @Slot()
    def start_button_handler(self) -> None:
        if self._run_status:
            self._timer.stop()
            self._test_thread.stop_work()
        else:
            self._test_thread.questions = self._question_list
            self._test_thread.start_work()

        self._run_status = not self._run_status
        button_text = "중지" if self._run_status else "시작"
        self.start_button.setText(button_text)

    @Slot(QPixmap)
    def front_draw_handler(self, pixmap : QPixmap) -> None:
        self.screen_img_label.setPixmap(pixmap)

    @Slot()
    def timer_handler(self) -> None:
        remaining_time = self.remaining_spin.value()
        remaining_time -= 1
        if remaining_time < 0:
            remaining_time = 0
            self._test_thread.next_work()
            self._timer.stop()

        self.remaining_spin.setValue(remaining_time)

    @Slot(int, dict)
    def process_handler(self, code : int, data : dict) -> None:
        if code == proc.PROCESS_TIME:
            remaining_time = data["time"]
            self.remaining_spin.setValue(remaining_time)
            self._timer.stop()
            self._timer = QTimer(self)
            self._timer.setInterval(1000)
            self._timer.timeout.connect(self.timer_handler)
            self._timer.start()
        elif code == proc.PROCESS_NEXT_CHAR:
            next_char = data["next_char"]
            self.char_img_label.setPixmap(self.CHAR_COMBO_DICT.get(next_char))
            #draw_char_img(self.char_img_label, next_char)
        elif code == proc.PROCESS_SUCCESS:
            self._question_success_count += 1
            self.success_count_img_label.setText(f"{self._question_success_count}개")
        elif code == proc.PROCESS_FAIL:
            self._question_fail_count += 1
            self.fail_count_img_label.setText(f"{self._question_fail_count}개")
        elif code == proc.PROCESS_LEVEL:
            level = data["level"]
            level_text = "★" * level
            self.level_img_label.setText(level_text)
        elif code == proc.PROCESS_QUESTION:
            question = data["question"]
            #self.question_img_label.setText(question)
            draw_char_img(self.question_img_label, question, 4)
        elif code == proc.PROCESS_DATA:
            draw_char_img(self.question_img_label, "")
            self.success_count_img_label.setText("0개")
            self.fail_count_img_label.setText("0개")

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
        if self._test_thread:
            self._test_thread.mirror_mode = value
    