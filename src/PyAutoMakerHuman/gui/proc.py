import os
import time
import logging
from threading import Thread, Event, Lock
from typing import Any, Callable
import random
import json

import cv2
import numpy as np
from PySide6.QtCore import QObject, Slot, Signal, QRect, QPoint, QThread
from PySide6.QtGui import QPixmap

from ..image import cv2_putText
from ..hand import HandResult
from .. import models_dir
from . import datas_dir
from ..hand_train import HandTrainer
from .exception import FrameException, ExitException, StopException, DataModifyExecption, NextExecption
from .utils import numpy_to_pixmap, time_check, get_degree


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


PROCESS_DATA = 1
PROCESS_SUCCESS = 2
PROCESS_FAIL = 3
PROCESS_NEXT_CHAR = 4
PROCESS_TIME = 5
PROCESS_LEVEL = 6
PROCESS_QUESTION = 7
class ProcessSignal(QObject):
    sig = Signal(int, dict)

    def send_data(self, data : dict) -> None:
        self.sig.emit(PROCESS_DATA, data)

    def success(self) -> None:
        self.sig.emit(PROCESS_SUCCESS, dict())

    def fail(self) -> None:
        self.sig.emit(PROCESS_FAIL, dict())

    def set_char(self, char : str) -> None:
        data = {"next_char" : char}
        self.sig.emit(PROCESS_NEXT_CHAR, data)

    def set_time(self, remaining_time : int) -> None:
        data = {"time" : remaining_time}
        self.sig.emit(PROCESS_TIME, data)

    def set_level(self, level : int) -> None:
        data = {"level" : level}
        self.sig.emit(PROCESS_LEVEL, data)

    def set_question(self, question : str) -> None:
        data = {"question" : question}
        self.sig.emit(PROCESS_QUESTION, data)


RUN_STUDY = 1
RUN_TEST = 2

def run_mode_check(ret_val : Any = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            if self._run_mode == RUN_TEST:
                return ret_val
            
            return func(*args, **kwargs)

        return wrapper

    return decorator

class WorkThread(Thread):

    FRAME_READ_TIMEOUT = 2
    PREDICT_TIMEOUT = 2
    PREDICT_THRESH = 0.8

    COLOR_RED = (0, 0, 255)
    COLOR_GREEN = (0, 255, 0)
    COLOR_ORENGE = (0, 127, 255)

    CHAR_DIRECTION_RIGHT = 1
    CHAR_DIRECTION_DOWN = 2
    CHAR_DIRECTION_LEFT = 3
    CHAR_DIRECTION_UP = 4

    CHAR_CORRECTION_INFO_DICT = dict()
    
    CHAR_EXCEPTION_LIST = tuple()

    def __init__(self, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture], run_mode : int, **kwargs):
        super().__init__()
        # 이벤트, 락
        self._exit_event = Event()
        self._stop_event = Event()
        self._next_event = Event()
        self._question_modify_event = Event()
        self._mirror_modify_lock = Lock()
        self._question_modify_lock = Lock()

        # 작동 관련 변수
        self.CHAR_CORRECTION_INFO_DICT = self.load_json()
        self._run_mode = run_mode
        self._mirror_mode = True
        self._questions = list()
        #self._mirror_classifier = HandTrainer()
        #self._mirror_classifier.load(os.path.join(models_dir, "mirror_model"))
        self._classifier = HandTrainer()
        self._classifier.load(os.path.join(models_dir, "model"))

        self._pre_target_char = ""
        self._pre_target_char_box = QRect()

        # 카메라
        self._front_camera = cameras[0]
        self._side_camera = cameras[1]

        if self._run_mode == RUN_STUDY:
            front_draw_handler = kwargs.get("front_draw_handler")
            answer_handler = kwargs.get("answer_handler")
            direction_handler = kwargs.get("direction_handler")

            #시그널
            self._front_draw_signal = FrontDrawSignal()
            self._front_draw_signal.sig.connect(front_draw_handler)

            self._answer_signal = AnswerSignal()
            self._answer_signal.sig.connect(answer_handler)

            self._direction_signal = DirectionSignal()
            self._direction_signal.sig.connect(direction_handler)

        elif self._run_mode == RUN_TEST:
            front_draw_handler = kwargs.get("front_draw_handler")
            process_handler = kwargs.get("process_handler")

            self._front_draw_signal = FrontDrawSignal()
            self._front_draw_signal.sig.connect(front_draw_handler)
            self._process_signal = ProcessSignal()
            self._process_signal.sig.connect(process_handler)

    @staticmethod
    def load_json() -> dict:
        with open(os.path.join(datas_dir, "proc_data.json"), "rb") as f:
            data = f.read()
            return json.loads(data)

    def exit(self) -> None:
        self._exit_event.set()

    def join(self, timeout: float or None = None) -> None:
        self.exit()
        return super().join(timeout)

    def start_work(self) -> None:
        self._stop_event.clear()

    def stop_work(self) -> None:
        self._stop_event.set()

    def next_work(self) -> None:
        self._next_event.set()

    def get_frame(self, target_camera : cv2.VideoCapture, mirror_mode_check : bool = False) -> np.ndarray:
        start_time = time.time()
        while time.time() - start_time < self.FRAME_READ_TIMEOUT:
            success, frame = target_camera.read()
            if success:
                return cv2.flip(frame, 1) if mirror_mode_check and self.mirror_mode else frame
        
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
            self._classifier.load(os.path.join(models_dir, "mirror_model" if value else "model"))
            logging.debug(f"[+] mirror mode change : {self._mirror_mode}")

    @property
    def questions(self) -> list or dict:
        with self._question_modify_lock:
            questions = self._questions

        return questions

    @questions.setter
    def questions(self, value : str or dict) -> None:
        with self._question_modify_lock:
            if self._run_mode == RUN_STUDY:
                value = list(STUDY_COMBINATION_CHAR_DICT.get(value, value))
                self._questions = list(value)
            elif self._run_mode == RUN_TEST:
                self._questions = value

            self._question_modify_event.set()
            logging.debug(f"[+] question change : {self._questions}")

            #이전 정보 지움
            self._pre_target_char = ""
            self._pre_target_char_box = QRect()

            self._question_modify_event.set()

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

    def draw_line(self, img : np.ndarray, start : tuple, end : tuple, color : tuple, thickness : int = 2) -> np.ndarray:
        return cv2.line(img, start, end, color, thickness)

    def front_draw(self, img : np.ndarray) -> None:
        self._front_draw_signal.send(img)

    @run_mode_check
    def answer_fail(self) -> None:
        self._answer_signal.fail()
    
    @run_mode_check
    def answer_processing(self) -> None:
        self._answer_signal.processing()

    @run_mode_check
    def answer_success(self) -> None:
        self._answer_signal.success()

    def is_exit_set(self) -> bool:
        if self._exit_event.is_set():
            raise ExitException()
        
        return False

    def is_events_set(self) -> bool:
        events = [self._exit_event, self._question_modify_event, self._stop_event, self._next_event]
        exceptions = [ExitException, DataModifyExecption, StopException, NextExecption]

        for event, exception in zip(events, exceptions):
            if event.is_set():
                raise exception()

        return False

    @property
    def front_classifier(self) -> HandTrainer:
        return self._classifier

    @property
    def side_classifier(self) -> HandTrainer:
        return self._classifier

    def predict_filter(self, predict_result : tuple) -> tuple:
        def filter_proc(predict_result):
            name, proba = predict_result
            if proba >= self.PREDICT_THRESH:
                return True
            else:
                return False

        return tuple(filter(filter_proc, predict_result))

    def front_predict(self) -> tuple[np.ndarray, tuple[HandResult, tuple]]:
        while self.is_events_set() == False:
            frame = self.front_frame
            result = self.front_classifier.predict(frame)
            if result:
                return frame, result

            self.front_draw(frame)

    def side_predict(self) -> tuple[np.ndarray, tuple[HandResult, tuple]]:
        while self.is_events_set() == False:
            frame = self.side_frame
            result = self.side_classifier.predict(frame)
            if result:
                return frame, result

    @time_check
    def front_side_predict(self, target_char : str) -> tuple[np.ndarray, tuple[HandResult, tuple]]:
        # 정면에서 판단 불가능한 수형
        except_char_list = ["ㅓ", "ㅕ", "ㅔ", "ㅖ"]

        front_result = self.front_predict()
        if not target_char in except_char_list:
            return front_result

        side_result = self.side_predict()
        # 사이드 추론 결과가 이상하거나 비어있다면, 정면캠의 결과를 리턴
        side_frame, (side_hand_result, side_predict_result) = side_result
        for name, proba in side_predict_result:
            if name in except_char_list:
                return side_result
                #return front_result[0], (side_hand_result, side_predict_result)
        
        return front_result

    def until_predict(self, target_char : str) -> tuple[np.ndarray, tuple[HandResult, tuple, tuple]]:
        while self.is_events_set() == False:
            result = self.front_side_predict(target_char)
            if not result:
                continue

            frame, predict_result = result
            org_frame = frame.copy()
            hand_result, predict_result = predict_result
            # 오른손이 아니라면 다시
            right_info = self.get_right_hand_info(hand_result, predict_result, target_char)
            if not right_info:
                self.front_draw(frame)
                continue

            idx, name, proba = right_info
            _, box = hand_result.get_boxes()[idx]
            _, landmarks = hand_result.get_landmarks()[idx]

            # 만약 타겟과 추론한 글자가 다르다면
            if target_char != name:
                self.answer_fail()
                frame = self.draw_box(frame, box, self.COLOR_RED)
                frame = self.draw_landmark(frame, landmarks)
                self.front_draw(frame)
                continue

            return org_frame, (hand_result, predict_result, right_info)
        
    def check_char_pt(self, target_char : str, frame : np.ndarray, box : tuple[int, int, int, int]) -> bool:
        if target_char == self._pre_target_char:
            cur_x, _, cur_w, _ = box
            cur_x = cur_x + int(cur_w / 2)
            _, w, _ = frame.shape
            frame_x_ragne = int(w * 0.3)
            x_range= int(cur_w * 0.3)
            x_range = x_range if x_range < frame_x_ragne else frame_x_ragne

            pre_x, pre_y = self._pre_target_char_box.center().toTuple()
            diff_x = abs(cur_x - pre_x)
            
            # 만약 이동 반경이 너무 적다면 선 표시
            if diff_x < x_range:
                frame = self.draw_line(frame, (pre_x - x_range, pre_y), (pre_x + x_range, pre_y)
                                        , self.COLOR_ORENGE, 6)

                self.front_draw(frame)
                return False

        return True

    @run_mode_check(True)
    def check_direction(self, target_char : str, frame : np.ndarray, hand_result : HandResult, right_info : tuple[int, str, float]) -> bool:
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

        frame = frame.copy()
        idx, name, proba = right_info
        _, box = hand_result.get_boxes()[idx]

        direction_info, (start_idx, end_idx) = self.CHAR_CORRECTION_INFO_DICT.get(target_char)
        _, abs_landmarks = hand_result.get_abs_landmarks()[idx]
        _, landmarks = hand_result.get_landmarks()[idx]
        start_landmark, end_landmark = abs_landmarks[start_idx][:2], abs_landmarks[end_idx][:2]
        target_degree = get_degree(start_landmark, end_landmark)
        logging.debug(f"target_degree : {target_degree}")

        direction = get_direction_(direction_info, target_degree, (10, 10))
        logging.debug(f"direction : {direction}")


        # 차이가 0이라면 성공 0이 아니라면 보정
        color = self.COLOR_ORENGE if not direction else self.COLOR_RED
        frame = self.draw_box(frame, box, color)
        frame = self.draw_landmark(frame, landmarks)
        # 대상이 되는 라인을 그림
        frame = self.draw_line(frame, start_landmark, end_landmark, self.COLOR_ORENGE, 6)
        frame = self.draw_text(frame, name, (box[0], box[1] - 35), color)
        self.front_draw(frame)

        if direction == DIRECTION_NONE:
            self._direction_signal.stop()

        else:
            if self.mirror_mode == False:
                direction = DIRECTION_LEFT if direction == DIRECTION_RIGHT else DIRECTION_RIGHT

            if direction == DIRECTION_LEFT:
                self._direction_signal.left()
            else:
                self._direction_signal.right()

        return False if direction else True

    def get_right_hand_info(self, hand_result : HandResult, predict_result : tuple, target_char : str) -> tuple:
        is_always_enter = False if target_char in self.CHAR_EXCEPTION_LIST else True

        target_hand_label = "Right" if self.mirror_mode else "Left"
        hand_labels = hand_result.get_labels()
        for idx, (hand_label, (name, proba)) in enumerate(zip(hand_labels, predict_result)):
            if is_always_enter or hand_label == target_hand_label:
                return idx, name, proba

        return tuple()

    def display_draw_wrapper(self, frame : np.ndarray, box : tuple, landmarks : list, name : str, color : tuple):
        frame = self.draw_box(frame, box, color)
        frame = self.draw_landmark(frame, landmarks)
        frame = self.draw_text(frame, name, (box[0], box[1] - 35), color)
        self.front_draw(frame)

    def check_char(self, target_char : str) -> bool:
        start_time = float()
        DURATION_TIME = 1.5
        self.answer_fail()
        while self.is_events_set() == False:
            result = self.until_predict(target_char)
            if not start_time:
                start_time = time.time()

            frame, (hand_result, predict_result, right_info) = result
            idx, name, proba = right_info
            _, box = hand_result.get_boxes()[idx]
            _, landmarks = hand_result.get_landmarks()[idx]

            # 여기서부턴 보정의 영역이므로 프로세싱으로 표기
            self.answer_processing()

            if self.check_char_pt(target_char, frame, box) == False:
                start_time = time.time()
                continue
            
            # 각도를 체크
            direction = self.check_direction(target_char, frame, hand_result, right_info)

            # 방향이 방향을 수정해야한다면...
            if not direction:
                start_time = time.time()
                continue

            # 정답 유지시간이 일정 시간 미만이라면 통과시키지 않음
            if time.time() - start_time < DURATION_TIME:
                self.display_draw_wrapper(frame, box, landmarks, name, self.COLOR_ORENGE)
                continue

            self.display_draw_wrapper(frame, box, landmarks, name, self.COLOR_GREEN)
            self.answer_success()

            # 이전 정보를 기억
            self._pre_target_char = name
            self._pre_target_char_box = QRect(*box)

            return True

        return False

    def check_question(self, question_info : dict) -> bool:
        question = question_info["question"]
        answer = question_info["answer"]
        remaining_time = question_info["time"]
        level = question_info["level"]

        self._process_signal.set_question(question)
        self._process_signal.set_time(remaining_time)
        self._process_signal.set_level(level)

        answer_idx = 0
        answer_len = len(answer)
        
        start_time = float()

        # 이전 입력 정보 지움
        self._pre_target_char = ""
        self._pre_target_char_box = QRect()
        DURATION_TIME = 1.5
        while answer_idx < answer_len and self.is_events_set() == False:
            target_char = answer[answer_idx]
            self._process_signal.set_char(target_char)
            result = self.until_predict(target_char)
            if not start_time:
                start_time = time.time()

            frame, (hand_result, predict_result, right_info) = result
            idx, name, proba = right_info
            _, box = hand_result.get_boxes()[idx]
            _, landmarks = hand_result.get_landmarks()[idx]

            if self.check_char_pt(target_char, frame, box) == False:
                start_time = time.time()
                continue
            
            # 정답 유지시간이 일정 시간 미만이라면 통과시키지 않음
            if time.time() - start_time < DURATION_TIME:
                self.display_draw_wrapper(frame, box, landmarks, name, self.COLOR_ORENGE)
                continue

            self.display_draw_wrapper(frame, box, landmarks, name, self.COLOR_GREEN)
            self.sleep(1.5)

            # 이전 정보를 기억
            self._pre_target_char = name
            self._pre_target_char_box = QRect(*box)

            answer_idx += 1
            start_time = float()

        return True


    def sleep(self, timeout : float) -> None:
        start_time = time.time()
        while time.time() - start_time < timeout:
            self.is_events_set()
            time.sleep(0.02)

        return

    def study_proc(self) -> None:
        while not self.is_exit_set():
            
            if self._stop_event.is_set():
                time.sleep(0.3)
                continue
            
            questions = self.questions
            questions_len = len(questions)
            question_idx = 0

            while question_idx < questions_len and self.is_events_set() == False:
                target_char = questions[question_idx]
                predict_result = self.check_char(target_char)
                if not predict_result:
                    continue
                
                question_idx += 1
                self.sleep(1)

            self._pre_target_char = ""
            self._pre_target_char_box = QRect()
            self.stop_work()

    def test_proc(self) -> None:
        while not self.is_events_set():
            frame = self.front_frame
            self.front_draw(frame)

            questions = self.questions
            if not questions:
                continue
            
            random.shuffle(questions)
            questions_len = len(questions)
            questions_idx = 0

            self._process_signal.send_data({"questions" : questions})

            while questions_idx < questions_len and self.is_events_set() == False:
                question_info = questions[questions_idx]
                try:
                    is_success = self.check_question(question_info)
                except NextExecption:
                    self._next_event.clear()
                    is_success = False

                if is_success:
                    self._process_signal.success()
                else:
                    self._process_signal.fail()

                questions_idx += 1

            self.stop_work()

    def run(self) -> None:
        while self._exit_event.is_set() == False:
            try:

                if self._run_mode == RUN_STUDY:
                    self.study_proc()
                elif self._run_mode == RUN_TEST:
                    self.test_proc()

            except ExitException:
                break
            except StopException:
                pass
            except DataModifyExecption:
                self._question_modify_event.clear()