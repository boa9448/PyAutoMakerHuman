import os
import fnmatch
from glob import glob

import imutils
import numpy as np
import cv2
import mediapipe as mp
from threading import Event
from image import cv2_imread
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class HandResult:
    def __init__(self, img_shape : tuple, result):
        self.height :int = img_shape[0]
        self.width : int = img_shape[1]
        self.channel : int = img_shape[2]

        self.result = result

    def __del__(self):
        pass

    def count(self) -> int:
        """발견된 손의 갯수를 리턴하는 함수
        """
        if self.result.multi_handedness is None:
            return 0

        return len(self.result.multi_handedness)

    def scores(self) -> list:
        """발견된 손의 스코어를 리턴하는 함수
        """
        if self.result.multi_handedness is None:
            return list()

        hand_score = [(info.classification[0].label, info.classification[0].score)
                        for info in self.result.multi_handedness]
        return hand_score

    def labels(self) -> list:
        """발견된 손의 라벨을 리턴하는 함수
        """

        if self.result.multi_handedness is None:
            return list()

        hand_labels = [info.classification[0].label
                        for info in self.result.multi_handedness]

        return hand_labels

    def get_landmarks(self) -> list:
        """발견된 손의 랜드마크를 리턴하는 함수
        """
        if self.count() == 0:
            return list()


        landmarks = []
        for label, hand_landmark in zip(self.labels(), self.result.multi_hand_landmarks):
            norm_landmarks = list(hand_landmark.landmark)

            landmarks.append((label, [[landmark.x, landmark.y, landmark.z]
                                    for landmark in norm_landmarks]))

        return landmarks

    def landmarks_to_abs_landmarks(self, landmarks : list) -> list:
        abs_landmarks = []
        for landmark in landmarks:
            abs_landmarks.append((landmark[0], [[int(x * self.width), int(y * self.height), z]
                                                for x, y, z in landmark[-1]]))

        return abs_landmarks

    def get_abs_landmarks(self) -> list:
        """발견된 손의 랜드마크의 절대좌표를 리턴하는 함수
        """
        if self.count() == 0:
            return list()


        landmarks = []
        for label, hand_landmark in zip(self.labels(), self.result.multi_hand_landmarks):
            norm_landmarks = list(hand_landmark.landmark)

            landmarks.append((label, [[int(landmark.x * self.width), int(landmark.y * self.height), landmark.z]
                                for landmark in norm_landmarks]))

        return landmarks

    def get_boxes(self) -> list:
        """발견된 손의 박스 좌표를 리턴하는 함수
        """
        box_list = []

        landmarks = self.get_abs_landmarks()
        for label, landmark in landmarks:
            minX = min(landmark, key = lambda x : x[0])[0]
            minY = min(landmark, key = lambda x : x[1])[1]
            maxX = max(landmark, key = lambda x : x[0])[0]
            maxY = max(landmark, key = lambda x : x[1])[1]
            box = [minX, minY, maxX - minX, maxY - minY]
            box_list.append((label, box))

        return box_list

    def get_landmark_from_box(self) -> list:
        """박스를 기준으로 랜드마크의 정규좌표를 리턴하는 함수
        """
        boxes = self.get_boxes()
        landmarks= self.get_abs_landmarks()

        new_landmarks = []
        for box, landmark in zip(boxes, landmarks):
            box_label, box = box
            start_x, start_y, box_width, box_height = box
            landmark_label, landmark = landmark
            new_landmarks.append((landmark_label, [((x - start_x) / box_width, (y - start_y) / box_height, z)
                                                     for x, y, z in landmark]))

        return new_landmarks


class HandUtil:
    def __init__(self, static_image_mode = True, max_num_hands = 2,
                min_detection_confidence = 0.5):

        self.logger = None
        self.detector = mp_hands.Hands(static_image_mode = static_image_mode,
                                        max_num_hands = max_num_hands,
                                        min_detection_confidence = min_detection_confidence)

    def __del__(self):
        self.detector.close()

    def log(self, log_message : str):
        print(log_message)

    def detect(self, img : np.ndarray) -> HandResult:
        result = self.detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return HandResult(img.shape, result)

    def extract(self, img : np.ndarray) -> list:
        result = self.detect(img)
        if result.count() == 0:
            return None

        landmarks = result.get_landmark_from_box()
        return [(label, np.asarray(landmark).flatten()) for label, landmark in landmarks]

    def extract_dataset(self, dataset_path : str or list) -> dict:
        file_list = []
        
        def get_file_list() -> list:
            return glob(os.path.join(dataset_path, "**", "*.*"), recursive = True)

        file_list = get_file_list() if type(dataset_path) == str else dataset_path
        self.log(f"[INFO] file count : {len(file_list)}")

        name_list = []
        data_list = []
        for idx, file in enumerate(file_list):
            self.log(f"[INFO] process... {idx + 1}/{len(file_list)}")
            name = file.split(os.path.sep)[-2]

            img = cv2_imread(file)
            img = imutils.resize(img, width=600)
            data = self.extract(img)
            if not data:
                continue

            name_list.append(name)
            data_list.append(np.asarray(data[0][1]).flatten()) #맨 처음 등록된 1개의 정보만, 라벨 정보는 제외

        self.log("done")
        return {"name" : name_list, "data" : data_list}


if __name__ == "__main__":
    cur_dir = os.path.dirname(__file__)
    dataset_dir = os.path.join(cur_dir, "..", "..", "dataset")
    dataset_dir = os.path.abspath(dataset_dir)

    hand = HandUtil()
    dataset = hand.extract_dataset(dataset_dir)
    print(dataset)