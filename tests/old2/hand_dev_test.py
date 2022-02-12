import env

import cv2
import numpy as np
from PyAutoMakerHuman import hand

hand_img = cv2.imread(os.path.join(env.test_img_dir, "2_hand.jpg"))
no_hand_img = cv2.imread(os.path.join(env.test_img_dir, "person.jpg"))

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

            landmarks.append((label, [(landmark.x, landmark.y, landmark.z)
                                    for landmark in norm_landmarks]))

        return landmarks

    def landmarks_to_abs_landmarks(self, landmarks : list) -> list:
        abs_landmarks = []
        for landmark in landmarks:
            abs_landmarks.append((landmark[0], [(int(x * self.width), int(y * self.height), z)
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

            landmarks.append((label, [(int(landmark.x * self.width), int(landmark.y * self.height), landmark.z)
                                for landmark in norm_landmarks]))

        return landmarks

    def get_boxes(self) -> list:
        """발견된 손의 박스 좌표를 리턴하는 함수
        """
        boxes = []

        landmarks = self.get_abs_landmarks()
        for label, landmark in landmarks:
            minX = min(landmark, key = lambda x : x[0])[0]
            minY = min(landmark, key = lambda x : x[1])[1]
            maxX = max(landmark, key = lambda x : x[0])[0]
            maxY = max(landmark, key = lambda x : x[1])[1]
            box = (minX, minY, maxX - minX, maxY - minY)
            boxes.append((label, box))

        return boxes

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

def test_box_draw(img : np.ndarray, box_list : list) -> None:
    img = img.copy()
    for label, box in box_list:
        x, y, w, h = box
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, label, (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)

    cv2.imshow("view", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

def test_landmark_from_box_draw(img : np.ndarray, boxes : list, landmarks : list) -> None:
    img = img.copy()
    
    for box, landmark in zip(boxes, landmarks):
        box_label, box = box
        landmark_label, landmark = landmark

        x, y, w, h = box
        box_img = img[y : y + h, x : x + w]

        for mark in landmark:
            x, y, z = mark
            center_x = int(x * w)
            center_y = int(y * h)
            cv2.circle(box_img, (center_x, center_y), 2, (255, 0, 0), 2)

        cv2.imshow(f"box {box_label}", box_img)
        cv2.waitKey()
        cv2.destroyAllWindows()
    

hand_result = HandResult((hand_img.shape), hand_proc_result)
#hand_img = no_hand_img
#hand_result = HandResult((hand_img.shape), no_hand_proc_result)

landmarks = hand_result.get_landmarks()
test_draw(hand_img, landmarks)

landmarks = hand_result.get_landmarks()
landmarks = hand_result.landmarks_to_abs_landmarks(landmarks)
test_abs_draw(hand_img, landmarks)

landmarks = hand_result.get_abs_landmarks()
test_abs_draw(hand_img, landmarks)

box_list = hand_result.get_boxes()
test_box_draw(hand_img, box_list)

landmarks_from_box = hand_result.get_landmark_from_box()
test_landmark_from_box_draw(hand_img, box_list, landmarks_from_box)