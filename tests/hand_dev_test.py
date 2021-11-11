import os
import sys

root_dir = os.path.abspath(os.path.join(__file__, ".."))
root_dir = os.path.split(root_dir)[0]

img_dir = os.path.join(root_dir, "tests", "imgs")
root_dir = os.path.join(root_dir, "src", "PyAutoMakerHuman")

sys.path.append(root_dir)

import cv2
import numpy as np
import hand

hand_img = cv2.imread(os.path.join(img_dir, "2_hand.jpg"))
no_hand_img = cv2.imread(os.path.join(img_dir, "person.jpg"))

proc = hand.HandUtil()
hand_proc_result = proc.detector.process(cv2.cvtColor(hand_img, cv2.COLOR_BGR2RGB))
no_hand_proc_result = proc.detector.process(cv2.cvtColor(no_hand_img, cv2.COLOR_BGR2RGB))

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
        landmarks = self.get_landmarks()
        pass


def test_draw(img : np.ndarray, landmarks : list) -> None:
    img = img.copy()
    h, w, _ = img.shape

    for landmark in landmarks:
        for x, y, _ in landmark[-1]:
            x = int(x * w)
            y = int(y * h)
            
            cv2.circle(img, (x, y), 2, (0, 255, 0), 2)
        
    cv2.imshow("view", img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def test_abs_draw(img : np.ndarray, landmarks : list) -> None:
    img = img.copy()
    for landmark in landmarks:
        for x, y, _ in landmark[-1]:
            cv2.circle(img, (x, y), 2, (0, 255, 0), 2)
        
    cv2.imshow("view", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    

hand_result = HandResult((hand_img.shape), hand_proc_result)

landmarks = hand_result.get_landmarks()
test_draw(hand_img, landmarks)

landmarks = hand_result.get_landmarks()
landmarks = hand_result.landmarks_to_abs_landmarks(landmarks)
test_abs_draw(hand_img, landmarks)

landmarks = hand_result.get_abs_landmarks()
test_abs_draw(hand_img, landmarks)
