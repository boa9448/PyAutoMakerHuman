import time
import logging
from threading import Thread, Event, Lock
from typing import Callable

import cv2
import numpy as np
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QPixmap

from ..hand import HandResult

from .. import model_dir
from ..hand_train import HandTrainer
from .exception import FrameException
from .utils import numpy_to_pixmap


logging.basicConfig(level = logging.DEBUG)

STUDY_COMBINATION_CHAR_DICT = {
    "ㄲ" : "ㄱㄱ"
    , "ㄸ" : "ㄷㄷ"
    , "ㅃ" : "ㅂㅂ"
    , "ㅆ" : "ㅅㅅ"
    , "ㅉ" : "ㅈㅈ"
    , "ㅘ" : "ㅗㅏ"
    , "ㅙ" : "ㅗㅐ"
    , "ㅝ" : "ㅜㅓ"
    , "ㅞ" : "ㅜㅔ"
}

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
    RUN_STUDY = 1
    RUN_TEST = 2

    FRAME_READ_TIMEOUT = 2

    PREDICT_TIMEOUT = 2

    COLOR_RED = (0, 0, 255)
    COLOR_GREEN = (0, 255, 0)
    COLOR_ORENGE = (0, 127, 255)

    def __init__(self, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]
                    , front_draw_handler : Callable, answer_handler : Callable, direction_handler : Callable
                    , run_mode : int = RUN_STUDY):
        super().__init__()
        # 이벤트, 락
        self._exit_event = Event()
        self._stop_event = Event()
        self._question_modify_event = Event()
        self._mirror_modify_lock = Lock()
        self._question_modify_lock = Lock()

        # 작동 관련 변수
        self._run_mode = run_mode
        self._mirror_mode = True
        self._questions = list()
        self._classifier = HandTrainer()
        self._classifier.load(model_dir)

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

    def join(self, timeout: float or None = None) -> None:
        self.exit()
        return super().join(timeout)

    def reset(self) -> None:
        self._stop_event.clear()

    def get_frame(self, target_camera : cv2.VideoCapture, mirror_mode : bool = False) -> np.ndarray:
        start_time = time.time()
        while time.time() - start_time < self.FRAME_READ_TIMEOUT:
            success, frame = target_camera.read()
            if success:
                return cv2.flip(frame, 1) if mirror_mode else frame
        
        raise FrameException("프레임을 가져오는데 실패했습니다")

    @property
    def front_frame(self) -> np.ndarray:
        return self.get_frame(self._front_camera, True)

    @property
    def side_frame(self) -> np.ndarray:
        #미러모드 체크는 정면 캠에서만 함
        return self.get_frame(self._side_camera)

    @property
    def mirror_mode(self) -> bool:
        with self._mirror_modify_lock:
            mode = self._mirror_mode

        return mode

    @mirror_mode.setter
    def mirror_mode(self, value : bool) -> None:
        with self._mirror_modify_lock:
            self._mirror_mode = value
            logging.debug(f"[+] mirror mode change : {self._mirror_mode}")

    @property
    def questions(self) -> list:
        with self._question_modify_lock:
            questions = self._questions

        return questions

    @questions.setter
    def questions(self, value : list) -> None:
        with self._question_modify_lock:
            if self._run_mode == self.RUN_STUDY:
                value = list(STUDY_COMBINATION_CHAR_DICT.get(value, value))
            self._questions = list(value)
            self._question_modify_event.set()
            logging.debug(f"[+] question change : {self._questions}")

    def predict(self, target_camera : cv2.VideoCapture, mirror_mode : bool = False) -> tuple[HandResult, tuple]:
        while self._exit_event.is_set() == False and self._question_modify_event.is_set() == False:
            frame = self.get_frame(target_camera, mirror_mode)
            result = self._classifier.predict(frame)
            if result:
                return frame, result
                
            self._front_draw_signal.send(frame)

        return tuple()

    def draw_box(self, img : np.ndarray, box : tuple[int, int, int, int], color : tuple) -> np.ndarray:
        hand_label, (x, y, w, h) = box
        return cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
    
    def draw_boxes(self, img : np.ndarray, boxes : list[tuple], color : tuple) -> np.ndarray:
        for box in boxes:
            img = self.draw_box(img, box, color)

        return img

    def draw_landmark(self, img : np.ndarray, landmarks : list) -> np.ndarray:
        h, w, c = img.shape
        connects = ((0, 1), (1, 2), (2, 3), (3, 4)
                    , (0, 5), (5, 6), (6, 7), (7, 8)
                    , (5, 9), (9, 13), (13, 17)
                    , (9, 10), (10, 11), (11, 12)
                    , (13, 14), (14, 15), (15, 16)
                    , (17, 18), (18, 19), (19, 20), (0, 17))

        for start_pt, end_pt in connects:
            start_x, start_y, _ = landmarks[start_pt]
            end_x, end_y, _ = landmarks[end_pt]

            start_x = int(start_x * w)
            start_y = int(start_y * h)

            end_x = int(end_x * w)
            end_y = int(end_y * h)

            cv2.line(img, (start_x, start_y), (end_x, end_y), (255, 255, 255), 2)

        for x, y, z in landmarks:
            x = int(x * w)
            y = int(y * h)
            cv2.circle(img, (x, y), 6, (255, 0, 0), -1)

        return img

    def draw_landmarks(self, img : np.ndarray, landmarks_list : list) -> np.ndarray:
        for hand_label, landmarks in landmarks_list:
            img = self.draw_landmark(img, landmarks)

        return img

    def study_proc(self):
        break_events = (self._exit_event
                        , self._stop_event
                        , self._question_modify_event)

        while not self._exit_event.is_set():
            if self._stop_event.is_set():
                time.sleep(0.3)
                continue

            questions = self.questions
            self._question_modify_event.clear()

            questions_len = len(questions)
            idx = 0
            while True:
                results = [e.is_set() for e in break_events]
                if True in results:
                    break

                predict_result = self.predict(self._front_camera, True)
                if not predict_result:
                    continue

                frame, result = predict_result
                hand_result, predict_result = result

                #hand_result : HandResult = hand_result
                boxes = hand_result.get_boxes()
                hand_labels = hand_result.get_labels()
                landmarks = hand_result.get_landmarks()
                
                # 정답 체크
            
                frame = self.draw_boxes(frame, boxes, self.COLOR_GREEN)
                frame = self.draw_landmarks(frame, landmarks)
                self._front_draw_signal.send(frame)


    def run(self) -> None:
        if self._run_mode == self.RUN_STUDY:
            self.study_proc()
        elif self._run_mode == self.RUN_TEST:
            pass