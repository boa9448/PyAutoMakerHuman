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

    def count(self):
        if not self.result.multi_hand_landmarks:
            return 0

        return len(self.result.multi_hand_landmarks)

    def scores(self):
        if self.count() == 0:
            return None

        return [hand.classification[0].score for hand in self.result.multi_handedness]

    def labels(self):
        if self.count() == 0:
            return None

        return [hand.classification[0].label for hand in self.result.multi_handedness]

    def indices(self):
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

    def set_logger(self, logger):
        self.logger = logger

    def log(self, log : str, color : tuple = (255, 255, 255)):
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

    def extract_dataset(self, dataset_path):
        ext_list = ["*.jpg", "*.png", "*.JPG", "*.PNG"]
        file_list = []
        
        for ext in ext_list:
            for root, dirs, files in os.walk(dataset_path):
                if not files:
                    continue

                for file in fnmatch.filter(files, ext):
                    file_list.append(os.path.join(root, file))

        self.log(f"[INFO] file count : {len(file_list)}")

        name_list = []
        data_list = []
        for idx, file in enumerate(file_list):
            self.log(f"[INFO] process... {idx + 1}/{len(file_list)}")
            name = file.split(os.path.sep)[-2]

            img = cv2.imread(file)
            img = imutils.resize(img, width=600)
            data = self.extract(img)
            if not data:
                continue

            name_list.append(name)
            data_list.append(np.asarray(data[0][1]).flatten()) #맨 처음 등록된 1개의 정보만, 박스 정보는 제외

        self.log("done")
        return {"name" : name_list, "data" : data_list}


if __name__ == "__main__":
    no_img = cv2.imread("C:\\test.jpg")
    two_img = cv2.imread("C:\\2_hand.jpg")
    hand = HandUtil()
    
    no_result = hand.detect(no_img)
    two_result = hand.detect(two_img)

    print(f"no hand count : {no_result.count()}")
    print(f"two hand count : {two_result.count()}")

    print(f"no hand scores : {no_result.scores()}")
    print(f"two hand scores : {two_result.scores()}")