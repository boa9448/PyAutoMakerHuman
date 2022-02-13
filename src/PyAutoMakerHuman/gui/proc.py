import time
from threading import Thread, Event, Lock
from typing import Callable

import cv2
import numpy as np
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QPixmap

from .exception import FrameException
from .utils import numpy_to_pixmap

class FrontDrawSignal(QObject):
    sig = Signal(QPixmap)

    def send(self, img : np.ndarray) -> None:
        img = numpy_to_pixmap(img)
        self.sig.emit(img)


ANSWER_FAIL = 0
ANSWER_PROCESSING = 1
ANSWER_SUCCESS = 2
class AnswerSignal(QObject):
    sig = Signal(int)

    def fail(self) -> None:
        self.sig.emit(ANSWER_FAIL)

    def processing(self) -> None:
        self.sig.emit(ANSWER_PROCESSING)

    def success(self) -> None:
        self.sig.emit(ANSWER_SUCCESS)


DIRECTION_NONE = 0
DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
class DirectionSignal(QObject):
    sig = Signal(int)

    def stop(self) -> None:
        self.sig.emit(DIRECTION_NONE)

    def left(self) -> None:
        self.sig.emit(DIRECTION_LEFT)

    def right(self) -> None:
        self.sig.emit(DIRECTION_RIGHT)


class WorkThread(Thread):
    FRAME_READ_TIMEOUT = 2

    def __init__(self, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]
                    , front_draw_handler : Callable, answer_handler : Callable, direction_handler : Callable):
        super().__init__()
        # 이벤트, 락
        self._exit_event = Event()
        self._mirror_modify_lock = Lock()

        # 작동 관련 변수
        self._mirror_mode = True

        # 카메라
        self._front_camera = cameras[0]
        self._side_camera = cameras[1]

        #시그널
        self._front_draw_signal = FrontDrawSignal()
        self._front_draw_signal.sig.connect(front_draw_handler)

        self._answer_signal = AnswerSignal()
        self._answer_signal.sig.connect(answer_handler)

        self._direction_signal = DirectionSignal()
        self._direction_signal.sig.connect(direction_handler)

    def exit(self) -> None:
        self._exit_event.set()

    def join(self, timeout: float or None = ...) -> None:
        self.exit()
        return super().join(timeout)

    def get_frame(self, target_camera : cv2.VideoCapture) -> np.ndarray:
        start_time = time.time()
        while time.time() - start_time > self.FRAME_READ_TIMEOUT:
            success, frame = target_camera.read()
            if success:
                return frame
        
        raise FrameException("프레임을 가져오는데 실패했습니다")

    @property
    def front_frame(self) -> np.ndarray:
        self.get_frame(self._front_camera)

    @property
    def side_frame(self) -> np.ndarray:
        self.get_frame(self._side_camera)

    @property
    def mirror_mode(self) -> bool:
        with self._mirror_modify_lock:
            mode = self._mirror_mode

        return mode

    @mirror_mode.setter
    def mirror_mode(self, value : bool) -> None:
        with self._mirror_modify_lock:
            self._mirror_mode = value

    def run(self) -> None:
        pass