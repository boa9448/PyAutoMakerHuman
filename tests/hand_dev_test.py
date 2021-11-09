import os
import sys

root_dir = os.path.abspath(os.path.join(__file__, ".."))
root_dir = os.path.split(root_dir)[0]

img_dir = os.path.join(root_dir, "tests", "imgs")
root_dir = os.path.join(root_dir, "src", "PyAutoMakerHuman")

sys.path.append(root_dir)

import cv2
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

        hand_score = [{info.classification[0].label : info.classification[0].score}
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

            landmarks.append({label : [[landmark.x, landmark.y, landmark.z]
                                for landmark in norm_landmarks]})

        return landmarks


    def get_abs_landmarks(self) -> list:
        """발견된 손의 랜드마크의 절대좌표를 리턴하는 함수
        """
        if self.count() == 0:
            return list()


        landmarks = []
        for label, hand_landmark in zip(self.labels(), self.result.multi_hand_landmarks):
            norm_landmarks = list(hand_landmark.landmark)

            landmarks.append({label : [[int(landmark.x * self.width), int(landmark.y * self.height), landmark.z]
                                for landmark in norm_landmarks]})

        return landmarks



hand_result = HandResult((hand_img.shape), hand_proc_result)
hand_result.get_landmarks()