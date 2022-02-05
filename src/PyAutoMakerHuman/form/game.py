import logging
from threading import Thread, Event, Lock

import cv2
import numpy as np
from PySide6.QtCore import QSize, Slot, QObject, Signal
from PySide6.QtWidgets import QFrame, QComboBox, QLabel
from PySide6.QtGui import QPixmap, QColor, QResizeEvent, QShowEvent, QHideEvent

from .game_form import Ui_Frame
from .utils import numpy_to_pixmap
from .. import hand_lang
from ..image import cv2_putText

DRAW_SIGNAL_FAIL = 0
DRAW_SIGNAL_FRONT = 1

logging.basicConfig(level=logging.DEBUG)

class DrawSignal(QObject):
    sig = Signal(int, QPixmap)

    def send_front(self, pixmap : QPixmap):
        self.sig.emit(DRAW_SIGNAL_FRONT, pixmap)

class GameThread(Thread):
    def __init__(self, front_camera : cv2.VideoCapture, side_camera : cv2.VideoCapture
                , draw_signal : DrawSignal, mirror_mode : bool = True):
        super().__init__()
        self.mirror_mode = mirror_mode
        self.answer = str()
        self.front_camera = front_camera
        self.side_camera = side_camera
        self.draw_signal = draw_signal
        self.exit_event = Event()

    def run(self) -> None:
        logging.debug("[+] 게임 스레드 시작")
        lang = hand_lang.HandLang()
        while not self.exit_event.is_set():
            success, frame = self.front_camera.read()
            if not success:
                continue

            if self.mirror_mode:
                frame = cv2.flip(frame, 1)

            results = lang.predict(frame)
            if results:
                result = max(results, key = lambda x : x[-1])
                hand_label, box, name, proba = result
                x, y, w, h = box
                color = (0, 255, 0) if name == self.answer else (0, 0, 255)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                frame = cv2_putText(frame, name, (x, y - 50), 4, (0, 255, 255), 2)

            pixmap = numpy_to_pixmap(frame)
            self.draw_signal.send_front(pixmap)
        
        logging.debug("[+] 게임 스레드 종료")

    def set_mirror_mode(self, mirror_mode : bool) -> None:
        self.mirror_mode = mirror_mode

    def set_answer(self, answer : str) -> None:
        self.answer = answer

    def exit(self) -> None:
        self.exit_event.set()

    def join(self, timeout = None) -> None:
        self.exit()
        return super().join(timeout)


class GameWindow(QFrame, Ui_Frame):
    CHAR_CHILD_COMBO_ITEMS = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅍ", "ㅎ"
                                , "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ", "ㄳ", "ㄵ", "ㄶ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅄ"]
    CHAR_PARENT_COMBO_ITEMS = ["ㅏ", "ㅐ", "ㅑ" , "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ"
                                , "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]

    def __init__(self, parent = None):
        super(GameWindow, self).__init__(parent)
        self.setupUi(self)
        self.img_label_list = [self.screen_img_label, self.shape_img_label, self.study_img_label, self.direction_img_label]
        self.mirror_mode = True
        self.cameras = parent.get_cameras()
        self.show()

    def __del__(self):
        self.dispose_data()

    def init(self) -> None:
        self.init_handler()
        self.init_display()

    def init_handler(self) -> None:
        self.char_child_combo.currentIndexChanged.connect(self.char_combo_change_handler)
        self.char_parent_combo.currentIndexChanged.connect(self.char_combo_change_handler)

    def init_display(self) -> None:
        self.char_child_combo.addItems(self.CHAR_CHILD_COMBO_ITEMS)
        self.char_parent_combo.addItems(self.CHAR_PARENT_COMBO_ITEMS)

        for img_label in self.img_label_list:
            rect = img_label.rect()
            width = rect.width()
            height = rect.height()

            pixmap = QPixmap(QSize(width, height))
            pixmap.fill(QColor(255, 255, 255))
            img_label.setPixmap(pixmap)
            img_label.setScaledContents(True)

    def init_data(self) -> None:
        self.draw_signal = DrawSignal()
        self.draw_signal.sig.connect(self.draw_signal_handler)
        self.game_thraed = GameThread(*self.cameras , self.draw_signal, self.mirror_mode)
        self.game_thraed.start()

    def dispose_data(self) -> None:
        self.game_thraed.join()

    def showEvent(self, event: QShowEvent) -> None:
        self.init_data()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.dispose_data()
        return super().hideEvent(event)

    @Slot(int, QPixmap)
    def draw_signal_handler(self, code : int, pixmap : QPixmap) -> None:
        self.screen_img_label.setPixmap(pixmap)

    def draw_char_img(self, target_img_label : QLabel, char : str) -> None:
        label_size = target_img_label.size().toTuple()
        img = np.ndarray((*label_size, 3), np.uint8)
        img.fill(255)
        img = cv2_putText(img, char, (0, 0), 20, (0, 0, 0), 4, center=True)

        pixmap = numpy_to_pixmap(img)
        target_img_label.setPixmap(pixmap)

    @Slot(int)
    def char_combo_change_handler(self, idx : int) -> None:
        if self.sender() == self.char_child_combo:
            target_list = self.CHAR_CHILD_COMBO_ITEMS
        else:
            target_list = self.CHAR_PARENT_COMBO_ITEMS

        char = target_list[idx]
        self.draw_char_img(self.study_img_label, char)
        self.set_answer(char)

    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.study_img_label.width()
        height = width
        pixmap = self.study_img_label.pixmap()
        pixmap = pixmap.scaled(width, height)
        self.study_img_label.setPixmap(pixmap)

        return super().resizeEvent(event)

    def set_mirror_mode(self, mirror_mode : bool) -> None:
        self.mirror_mode = mirror_mode
        self.game_thraed.set_mirror_mode(mirror_mode)

    def get_mirror_mode(self) -> bool:
        return self.mirror_mode

    def set_answer(self, answer : str) -> None:
        if getattr(self, "game_thread", None):
            self.game_thraed.set_answer(answer)