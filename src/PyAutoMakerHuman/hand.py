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
    def __init__(self, img_size : tuple, result):
        self.img_size = img_size
        self.width : int = img_size[0]
        self.height : int = img_size[1]
        self.result = result

    def __del__(self):
        pass

    def __iter__(self):
        data_list = []
        count = self.count()
        if count == 0:
            return

        labels = self.labels()
        scores = self.scores()
        boxes = self.get_box_list()
        landmark_list = self.get_box_landmark_list()

        for label, score, box, landmark in zip(labels, scores, boxes, landmark_list):
            data_list.append({
                "label" : label
                , "score" : score
                , "box" : box
                , "landmark" : landmark
            })

        for data in data_list:
            yield data

    def count(self) -> int:
        if not self.result.multi_hand_landmarks:
            return 0

        return len(self.result.multi_hand_landmarks)

    def scores(self) -> list:
        if self.count() == 0:
            return None

        return [hand.classification[0].score for hand in self.result.multi_handedness]

    def labels(self) -> list:
        if self.count() == 0:
            return None

        return [hand.classification[0].label for hand in self.result.multi_handedness]

    def indices(self):
        if self.count() == 0:
            return None

        return [hand.classification[0].index for hand in self.result.multi_handedness]

    def get_box_list(self, bRelative : bool = False) -> list:
        if self.count() == 0:
            return None

        box_list = []
        landmark_list = self.get_landmark_list(bRelative)
        for landmark in landmark_list:
            minX = min(landmark, key = lambda x : x[0])[0]
            minY = min(landmark, key = lambda x : x[1])[1]
            maxX = max(landmark, key = lambda x : x[0])[0]
            maxY = max(landmark, key = lambda x : x[1])[1]
            box = [minX, minY, maxX - minX, maxY - minY]
            box_list.append(box)

        return box_list

    def get_landmark_list(self, bRelative : bool = False) -> list:
        """
        랜드마크의 리트스를 리턴하는 함수
        bRelative가 True라면 정규화된 좌표를 리턴함
        """

        result_list = []
        if self.count() == 0:
            return None

        
        for hand_landmark in self.result.multi_hand_landmarks:
            landmark_list = list(hand_landmark.landmark)

            result_list.append([(landmark.x, landmark.y, landmark.z) for landmark in landmark_list])


        if not bRelative:
            width, height = self.img_size
            for idx in range(len(result_list)):
                result = result_list[idx]
                result_list[idx] = [
                    (int(mark[0] * width), int(mark[1] * height), int(mark[2] * 10000)) for mark in result
                ]

        return result_list

    def get_box_landmark_list(self, bRelative : bool = False):
        box_list = self.get_box_list(False)
        landmark_list = self.get_landmark_list(False)

        new_landmark_list = []

        for box, landmark in zip(box_list, landmark_list):
            new_landmark = map(lambda landmark : (landmark[0] - box[0], landmark[1] - box[1], landmark[2]), landmark)
            new_landmark_list.append(list(new_landmark))

        if bRelative:
            idx = 0
            for box, landmark in zip(box_list, new_landmark_list):
                new_landmark = map(lambda landmark : (landmark[0] / box[2], landmark[1] / box[3], landmark[2] / 10000), landmark)
                new_landmark_list[idx] = tuple(new_landmark)
                idx += 1

        return new_landmark_list


    def draw(self, img : np.ndarray):
        if self.count() == 0:
            return

        box_list = self.get_box_list()
        for box in box_list:
            cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (255, 0, 0), 2)

        for hand_landmarks in self.result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                    img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

class HandUtil:
    def __init__(self, static_image_mode = True, max_num_hands = 2,
                min_detection_confidence = 0.5):

        self.logger = None
        self.detector = mp_hands.Hands(static_image_mode = static_image_mode,
                                        max_num_hands = max_num_hands,
                                        min_detection_confidence = min_detection_confidence)

    def __del__(self):
        self.detector.close()

    def set_logger(self, logger):
        self.logger = logger

    def log(self, log : str, color : tuple = (255, 255, 255)) -> None:
        if self.logger is None:
            print(log)
            return

        self.logger(log, color)

    def detect(self, img):
        result = self.detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        height, width, _ = img.shape
        return HandResult((width, height), result)

    def extract(self, img):
        result = self.detect(img)
        if result.count() == 0:
            return None

        box_list = result.get_box_list(False)
        landmark_list = result.get_box_landmark_list(True)
        return [(box, np.asarray(landmark).flatten()) for box, landmark in zip(box_list, landmark_list)]

    def extract_dataset(self, dataset_path : str or list, exit_event : Event = Event()) -> dict:
        file_list = []
        
        def get_file_list() -> list:
            return glob(os.path.join(dataset_path, "**", "*.*"), recursive = True)

        file_list = get_file_list() if type(dataset_path) == str else dataset_path
        self.log(f"[INFO] file count : {len(file_list)}")

        name_list = []
        data_list = []
        for idx, file in enumerate(file_list):
            if exit_event.is_set():
                self.log("[INFO] exit event set")
                return dict()

            self.log(f"[INFO] process... {idx + 1}/{len(file_list)}")
            name = file.split(os.path.sep)[-2]

            img = cv2_imread(file)
            img = imutils.resize(img, width=600)
            data = self.extract(img)
            if not data:
                continue

            name_list.append(name)
            data_list.append(np.asarray(data[0][1]).flatten()) #맨 처음 등록된 1개의 정보만, 박스 정보는 제외

        self.log("done")
        return {"name" : name_list, "data" : data_list}


if __name__ == "__main__":
    pass