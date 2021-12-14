import os
import math
from glob import glob

import imutils
import numpy as np
import cv2
import mediapipe as mp
from image import cv2_imread
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

HAND_DISTANCE_NONE = 0
HAND_DISTANCE_UP = 1
HAND_DISTANCE_DOWN = 2
HAND_DISTANCE_LEFT = 3
HAND_DISTANCE_RIGHT = 4

class HandResult:
    def __init__(self, img_shape : tuple, result):
        self.height :int = img_shape[0]
        self.width : int = img_shape[1]
        self.channel : int = img_shape[2]

        self.results = result

    def __del__(self):
        pass

    def count(self) -> int:
        """발견된 손의 갯수를 리턴하는 함수
        """
        if self.results.multi_handedness is None:
            return 0

        return len(self.results.multi_handedness)

    def scores(self) -> list:
        """발견된 손의 스코어를 리턴하는 함수
        """
        if self.results.multi_handedness is None:
            return list()

        hand_score = [(info.classification[0].label, info.classification[0].score)
                        for info in self.results.multi_handedness]
        return hand_score

    def labels(self) -> list:
        """발견된 손의 라벨을 리턴하는 함수
        """

        if self.results.multi_handedness is None:
            return list()

        hand_labels = [info.classification[0].label
                        for info in self.results.multi_handedness]

        return hand_labels

    def get_landmarks(self) -> list:
        """발견된 손의 랜드마크를 리턴하는 함수
        """
        if self.count() == 0:
            return list()


        landmarks = []
        for label, hand_landmark in zip(self.labels(), self.results.multi_hand_landmarks):
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
        for label, hand_landmark in zip(self.labels(), self.results.multi_hand_landmarks):
            norm_landmarks = list(hand_landmark.landmark)

            landmarks.append((label, [[int(landmark.x * self.width), int(landmark.y * self.height), landmark.z]
                                for landmark in norm_landmarks]))

        return landmarks

    def get_boxes(self) -> list:
        """발견된 손의 박스 좌표를 리턴하는 함수
        x, y, w, h
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

    def get_degree(self) -> list:
        def get_degree_(start, end):
            start_x, start_y = start
            end_x, end_y = end
            dx = end_x - start_x
            dy = end_y - start_y
            degree = math.atan2(dy, dx) * (180.0 / math.pi) + 90
            degree = degree + 360 if degree < 0 else degree

            return int(degree)

        landmarks = self.get_landmark_from_box()
        if not landmarks:
            return list()
            #return HAND_DISTANCE_NONE

        #손목, 손바닥과 중지가 만나는 지점
        #추후에 정확한 이름으로 수정
        degrees = [get_degree_(landmark[0][:2], landmark[9][:2]) for _, landmark in landmarks]
        return degrees

    def get_direction(self) -> list:
        directions = []
        degrees = self.get_degree()

        for deg in degrees:
            if deg > 315 and deg <= 360 or deg > 0 and deg <= 45:
                directions.append(HAND_DISTANCE_UP)
            elif deg > 45 and deg <= 135:
                directions.append(HAND_DISTANCE_RIGHT)
            elif deg > 135 and deg <= 225:
                directions.append(HAND_DISTANCE_DOWN)
            else:
                directions.append(HAND_DISTANCE_LEFT)

        return directions

    def test_landmark_draw(self, img : np.ndarray) -> np.ndarray:
        if self.results.multi_hand_landmarks:
            img = img.copy()
            
            for hand_landmarks in self.results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        return img
        



class HandUtil:
    def __init__(self, static_image_mode = True, max_num_hands = 2,
                min_detection_confidence = 0.5):

        self.logger = print
        self.detector = mp_hands.Hands(static_image_mode = static_image_mode,
                                        max_num_hands = max_num_hands,
                                        min_detection_confidence = min_detection_confidence)

    def __del__(self):
        self.detector.close()

    def set_logger(self, logger) -> None:
        self.logger = logger

    def log(self, log_message : str):
        self.logger(log_message)

    def detect(self, img : np.ndarray) -> HandResult:
        result = self.detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return HandResult(img.shape, result)

    def extract(self, img : np.ndarray) -> list:
        result = self.detect(img)
        if result.count() == 0:
            return None

        boxes = result.get_boxes()
        landmarks = result.get_landmark_from_box()
        return [(label, box, np.asarray(landmark).flatten()) for (_, box), (label, landmark) in zip(boxes, landmarks)]

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
            data_list.append(np.asarray(data[0][2]).flatten()) #맨 처음 등록된 1개의 정보만, 라벨, 박스 정보는 제외

        self.log("done")
        return {"name" : name_list, "data" : data_list}

    def extract(self, img : np.ndarray) -> list:
        result = self.detect(img)
        if result.count() == 0:
            return None

        landmarks = result.get_landmark_from_box()
        return [(label, box, np.asarray(landmark).flatten()) for (_, box), (label, landmark) in zip(boxes, landmarks)]


if __name__ == "__main__":
    cur_dir = os.path.dirname(__file__)
    dataset_dir = os.path.join(cur_dir, "..", "..", "dataset")
    dataset_dir = os.path.abspath(dataset_dir)

    hand = HandUtil()
    dataset = hand.extract_dataset(dataset_dir)
    print(dataset)

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        try:
            success, frame = cap.read()
            if not success:
                continue
            
            frame = cv2.flip(frame, 1)
            result = hand.detect(frame)
            degree = result.get_degree()
            directions = result.get_direction()
            boxes = result.get_boxes()
            landmarks = result.get_landmark_from_box()
            for (_, box), (_, landmark) in zip(boxes, landmarks):
                start, end = landmark[0][:2], landmark[9][:2]
                x, y, w, h = box
                x = 0 if x < 0 else x
                y = 0 if y < 0 else y

                start_x, start_y = int(start[0] * w), int(start[1] * h)
                end_x, end_y = int(end[0] *w), int(end[1] * h)
                frame_box = frame[y : y + h, x : x + w]

                start = (start_x, start_y)
                end = (end_x, end_y)
                cv2.line(frame_box, start, end, (0, 255, 0), 3)
                cv2.imshow("box", frame_box)
                cv2.waitKey(1)
            cv2.putText(frame, f"degree : {degree} directions : {directions}", (0, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.imshow("view", frame)
            cv2.waitKey(1)

        except KeyboardInterrupt as e:
            break

    cap.release()
    cv2.destroyAllWindows()