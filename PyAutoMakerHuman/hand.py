import os
import fnmatch
import imutils
import numpy as np
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class HandResult:
    def __init__(self, img_size, result):
        self.img_size = img_size
        self.width = img_size[0]
        self.height = img_size[1]
        self.result = result

    def __del__(self):
        pass

    def __iter__(self):
        data_list = [("count", self.count())
                    , ("score", self.score())
                    , ("boxes", self.get_box_list())
                    , ("landmarks_list", self.get_landmark_list())]

        for data in data_list:
            yield data

    def count(self):
        if not self.result.multi_hand_landmarks:
            return 0

        return len(self.result.multi_hand_landmarks)

    def score(self):
        if self.count() == 0:
            return None

        return [hand.classification[0].score for hand in self.result.multi_handedness]

    def label(self):
        if self.count() == 0:
            return None

        return [hand.classification[0].label for hand in self.result.multi_handedness]

    def index(self):
        if self.count() == 0:
            return None

        return [hand.classification[0].index for hand in self.result.multi_handedness]

    def get_box_list(self, bRelative : bool = False):
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

    def get_landmark_list(self, bRelative : bool = False):
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
                    (int(mark[0] * width), int(mark[1] * height)) for mark in result
                ]

        return result_list

    def get_box_landmark_list(self, bRelative : bool = False):
        pass


    def draw(self, img : np.ndarray):
        if self.count() == 0:
            return

        box_list = self.get_box_list()
        for box in box_list:
            cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (255, 0, 0), 2)

        for hand_landmarks in self.result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                    img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    def to_dict(self):
        return dict(self.__iter__())

class HandUtil:
    def __init__(self, static_image_mode = True, max_num_hands = 2,
                min_detection_confidence = 0.5):

        self.detector = mp_hands.Hands(static_image_mode = static_image_mode,
                                        max_num_hands = max_num_hands,
                                        min_detection_confidence = min_detection_confidence)

    def __del__(self):
        self.detector.close()

    def detect(self, img):
        result = self.detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        height, width, _ = img.shape
        return HandResult((width, height), result)

    def extract(self, img):
        result = self.detect(img)
        boxes = result.get_box_list()

        vec_list = []
        for box in boxes:
            x, y, w, h = box
            hand = img[y:y+h, x:x+w]
            (hH, hW) = hand.shape[:2]
            
            vec_list.append((box, vec.flatten()))

        return vec_list

    def extract_dataset(self, dataset_path):
        pass


if __name__ == "__main__":
    pass