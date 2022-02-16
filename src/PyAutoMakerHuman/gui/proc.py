import time
import logging
from threading import Thread, Event, Lock
from typing import Callable
import math
import asyncio

import cv2
import numpy as np
from PySide6.QtCore import QObject, Slot, Signal, QRect, QPoint
from PySide6.QtGui import QPixmap

from ..image import cv2_putText

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

    CHAR_DIRECTION_RIGHT = 1
    CHAR_DIRECTION_DOWN = 2
    CHAR_DIRECTION_LEFT = 3
    CHAR_DIRECTION_UP = 4

    CHAR_CORRECTION_INFO_DICT = {"ㄱ" : (CHAR_DIRECTION_UP, (8, 5))
                                , "ㄴ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㄷ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㄹ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㅁ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅂ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅅ" : (CHAR_DIRECTION_UP, (9, 0))
                                , "ㅇ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅈ" : (CHAR_DIRECTION_UP, (9, 0))
                                , "ㅊ" : (CHAR_DIRECTION_UP, (9, 0))
                                , "ㅋ" : (CHAR_DIRECTION_UP, (9, 0))
                                , "ㅌ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㅍ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅎ" : (CHAR_DIRECTION_UP, (17, 5))
                                , "ㅏ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅑ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅓ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㅕ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㅗ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅛ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅜ" : (CHAR_DIRECTION_UP, (8, 5))
                                , "ㅠ" : (CHAR_DIRECTION_UP, (8, 5))
                                , "ㅡ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㅣ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅐ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅒ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅔ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㅖ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㅢ" : (CHAR_DIRECTION_LEFT, (0, 9))
                                , "ㅚ" : (CHAR_DIRECTION_UP, (0, 9))
                                , "ㅟ" : (CHAR_DIRECTION_UP, (8, 5)) }

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

        self._pre_target_char = ""
        self._pre_target_char_box = QRect()

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
                return cv2.flip(frame, 1) if self.mirror_mode else frame
        
        raise FrameException("프레임을 가져오는데 실패했습니다")

    @property
    def front_frame(self) -> np.ndarray:
        return self.get_frame(self._front_camera, self.mirror_mode)

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

            #이전 정보 지움
            self._pre_target_char = ""
            self._pre_target_char_box = QRect()

            self._stop_event.clear()

    def draw_box(self, img : np.ndarray, box : tuple[int, int, int, int], color : tuple) -> np.ndarray:
        x, y, w, h = box
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
        for landmarks in landmarks_list:
            img = self.draw_landmark(img, landmarks)

        return img

    def draw_text(self, img : np.ndarray, text : str, org : tuple, color : tuple) -> np.ndarray:
        return cv2_putText(img, text, org, 3, color, 2)

    def draw_line(self, img : np.ndarray, start : tuple, end : tuple, color : tuple) -> np.ndarray:
        return cv2.line(img, start, end, color, 2)

    def predict(self, target_camera : cv2.VideoCapture, mirror_mode : bool = False) -> tuple[np.ndarray, tuple[HandResult, tuple]]:
        while self._exit_event.is_set() == False and self._question_modify_event.is_set() == False:
            frame = self.get_frame(target_camera, mirror_mode)
            result = self._classifier.predict(frame)
            if result:
                return frame, result

            self._front_draw_signal.send(frame)

        return tuple()

    def front_side_predict(self, mirror_mode :bool = False) -> tuple[np.ndarray, tuple[HandResult, tuple]]:
        front_result = self.predict(self._front_camera, mirror_mode)
        side_result = self.predict(self._side_camera, False)

        if (not front_result) or (not side_result):
            return tuple()
        

    def check_char(self, target_char : str) -> bool:
        def get_direction_(base_direction : int, target_degree : int, error_range : tuple[int, int]) -> int:
            range_left, range_right = error_range
            base_degree = base_direction * 90
            left = (base_degree - range_left) % 360
            right = (base_degree + range_right) % 360

            if base_direction == self.CHAR_DIRECTION_UP:
                if (left <= target_degree or target_degree <= right):
                    return DIRECTION_NONE

            else:
                if (left <= target_degree and target_degree <= right):
                    return DIRECTION_NONE

            # (target_degree < left and target_degree > right):
            left_diff = left - target_degree
            right_diff = right - target_degree

            return DIRECTION_RIGHT if abs(right_diff) > abs(left_diff) else DIRECTION_LEFT

        start_time = time.time()
        DURATION_TIME = 1.5
        self._answer_signal.fail()
        while (self._exit_event.is_set() == False
                and self._question_modify_event.is_set() == False):
            
            result = self.predict(self._front_camera, self.mirror_mode)
            if not result:
                start_time = time.time()
                continue

            frame, predict_result = result
            org_frame = frame.copy()
            hand_result, predict_result = predict_result
            # 오른손이 아니라면 다시
            right_info = self.get_right_hand_info(hand_result, predict_result)
            if not right_info:
                start_time = time.time()
                self._front_draw_signal.send(frame)
                continue

            idx, name, proba = right_info
            _, box = hand_result.get_boxes()[idx]

            # 만약 타겟과 추론한 글자가 다르다면
            if target_char != name:
                start_time = time.time()
                self._answer_signal.fail()
                frame = self.draw_box(frame, box, self.COLOR_RED)
                self._front_draw_signal.send(frame)
                continue

            # 만약 타겟과 이전 타겟 글자가 같다면 좌표가 달라야함
            if target_char == self._pre_target_char:
                cur_x, _, cur_w, _ = box
                cur_x = cur_x + int(cur_w / 2)
                x_range= int(cur_w * 0.3)

                pre_x, pre_y = self._pre_target_char_box.center().toTuple()
                diff_x = abs(cur_x - pre_x)
                
                # 만약 이동 반경이 너무 적다면 선 표시
                if diff_x < x_range:
                    start_time = time.time()
                    frame = self.draw_line(frame, (pre_x - x_range, pre_y), (pre_x + x_range, pre_y)
                                            , self.COLOR_ORENGE)

                    self._front_draw_signal.send(frame)
                    continue
            
            # 각도를 체크
            self._answer_signal.processing()
            direction_info, (start_idx, end_idx) = self.CHAR_CORRECTION_INFO_DICT.get(target_char)
            _, landmark = hand_result.get_abs_landmarks()[idx]
            start_landmark, end_landmark = landmark[start_idx][:2], landmark[end_idx][:2]
            target_degree = self.get_degree(start_landmark, end_landmark)
            logging.debug(f"target_degree : {target_degree}")

            direction = get_direction_(direction_info, target_degree, (10, 10))
            logging.debug(f"direction : {direction}")

            # 대상이 되는 라인을 그림
            frame = self.draw_line(frame, start_landmark, end_landmark, self.COLOR_ORENGE)

            # 차이가 0이라면 성공 0이 아니라면 보정
            color = self.COLOR_ORENGE if not direction else self.COLOR_RED
            frame = self.draw_box(frame, box, color)
            frame = self.draw_text(frame, name, (box[0], box[1] - 35), color)
            self._front_draw_signal.send(frame)

            if direction == DIRECTION_NONE:
                self._direction_signal.stop()
            elif direction == DIRECTION_LEFT:
                self._direction_signal.left()
            else:
                self._direction_signal.right()

            # 방향이 DIRECTION_NONE(0)이 아니라면 다시 시도하도록
            if direction:
                start_time = time.time()
                continue

            # 정답 유지시간이 일정 시간 미만이라면 통과시키지 않음
            if time.time() - start_time < DURATION_TIME:
                continue

            frame = self.draw_box(org_frame, box, self.COLOR_GREEN)
            frame = self.draw_text(frame, name, (box[0], box[1] - 35), self.COLOR_GREEN)
            self._front_draw_signal.send(frame)
            self._answer_signal.success()

            # 이전 정보를 기억
            self._pre_target_char = name
            self._pre_target_char_box = QRect(*box)

            self.sleep(2)

            return True

        return False

    def get_degree(self, start : tuple[int, int, int], end : tuple[int, int, int]):
        start_x, start_y = start
        end_x, end_y = end
        dx = end_x - start_x
        dy = end_y - start_y
        degree = math.atan2(dy, dx) * (180.0 / math.pi) + 90
        degree = degree + 360 if degree < 0 else degree

        return int(degree)

    def get_right_hand_info(self, hand_result : HandResult, predict_result : tuple) -> tuple:
        hand_labels = hand_result.get_labels()
        for idx, (hand_label, (name, proba)) in enumerate(zip(hand_labels, predict_result)):
            if hand_label == "Right" if self.mirror_mode else "Left":
                return idx, name, proba

        return tuple()

    def sleep(self, timeout : float) -> None:
        break_events = (self._exit_event
                        , self._stop_event)

        start_time = time.time()
        while time.time() - start_time < timeout:
            results = [event.is_set() for event in break_events]
            if True in results:
                return

        return

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
            question_idx = 0
            while question_idx < questions_len:
                results = [e.is_set() for e in break_events]
                if True in results:
                    break

                target_char = questions[question_idx]
                predict_result = self.check_char(target_char)
                if not predict_result:
                    continue
                
                question_idx += 1

            if not self._question_modify_event.is_set():
                self._stop_event.set()

    def run(self) -> None:
        if self._run_mode == self.RUN_STUDY:
            self.study_proc()
        elif self._run_mode == self.RUN_TEST:
            pass