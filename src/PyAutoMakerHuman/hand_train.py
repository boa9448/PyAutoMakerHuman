import os
import time
from glob import glob

import cv2
import numpy as np

import hand
import train
import image

class HandTrainer:
    def __init__(self):
        self.detector = hand.HandUtil()
        self.trainer = train.SvmUtil()
        self.logger = print

    def __del__(self):
        pass

    def set_logger(self, logger) -> None:
        self.logger = logger
        self.detector.set_logger(logger)
        self.trainer.set_logger(logger)

    def log(self, log_message: str) -> None:
        self.logger(log_message)


    def train(self, dataset_path : str) -> None:
        data = self.detector.extract_dataset(dataset_path)
        names, datas = data.values()

        self.trainer.train_svm(datas, names)

    def save(self, save_path : str) -> None:
        self.trainer.save_svm(save_path)
    
    def load(self, load_path : str) -> None:
        self.trainer.load_svm(load_path)

    def detect(self, img : np.ndarray) -> hand.HandUtil:
        return self.detector.detect(img)

    def detect_boxes(self, img : np.ndarray) -> list:
        result = self.detector.detect(img)
        return result.get_boxes()

    def detect_draw(self, img : np.ndarray) -> tuple:
        result = self.detector.detect(img)
        return result.get_boxes(), result.test_landmark_draw(img)

    def predict(self, img : np.ndarray) -> list:
        datas = self.detector.extract(img)
        if datas is None:
            return list()

        results = []
        for hand_label, box, data in datas:
            name, proba = self.trainer.predict([data])
            results.append((hand_label, box, name, proba))

        return results

    def get_camera(self, camera_idx : int or str) -> cv2.VideoCapture:
        class CameraWrapper:
            def __init__(self, camera_idx : int or str):
                self.cap = cv2.VideoCapture(camera_idx)
                if not self.cap.isOpened():
                    raise RuntimeError("카메라를 여는데 실패했습니다")

            def __del__(self):
                self.cap.release()

            def read(self) -> tuple:
                return self.cap.read()

            def opened(self) -> bool:
                return self.cap.isOpened()

        return CameraWrapper(camera_idx)

    def camera_detect_boxes(self, camera_idx : int or str = 0) -> tuple:
        cap = self.get_camera(camera_idx)
        while cap.opened():
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            results = self.detect_boxes(frame)
            yield frame, results

    def camera_detect_draw(self, camera_idx : int or str = 0) -> tuple:
        cap = self.get_camera(camera_idx)
        while cap.opened():
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            boxes, draw_frame = self.detect_draw(frame)
            yield frame, boxes, draw_frame

    def camera_predict(self, camera_idx : int or str = 0) -> tuple:
        cap = self.get_camera(camera_idx)
        while cap.opened():
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            results = self.predict(frame)
            yield frame, results

    def camera_predict_capture(self, camera_idx : int or str = 0, save_path : str = "dataset") -> np.ndarray:
        cap = self.camera_detect_draw(camera_idx)
        window_name = "camera_predict_capture"
        next_frame = False

        while True:
            try:
                frame, boxes, frame_draw = next(cap)

                cv2.imshow(window_name, frame_draw)
                timeout = -1 if boxes else 1
                timeout = 1 if next_frame else timeout
                code = cv2.waitKey(timeout) & 0xff
                if code == ord('c'):
                    break

                elif code == ord('n'):
                    next_frame = not next_frame

                elif code == ord('a'):
                    file_path = os.path.join(save_path, f"{time.time()}.png")
                    cv2.imwrite(file_path, frame)

            except KeyboardInterrupt as e:
                break

        cv2.destroyWindow(window_name)


    def test_camera(self, idx : int = 0) -> None:
        cap = self.camera_predict(idx)
        while True:
            try:
                frame, results = next(cap)
                for hand_label, box, name, proba in results:
                    x, y, w, h = box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(frame, f"name : {name}, proba : {proba:.2f}", (x, y - 20)
                                , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                cv2.imshow("test_camera", frame)
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break
                
            except KeyboardInterrupt as e:
                break

        cv2.destroyAllWindows()
        cap.close()

    def test_char_predict(self, camera_idx : int = 0) -> None:
        cap = self.camera_predict(camera_idx)
        char_list = []
        def add_char(cur_time, box, name):
            if char_list:
                last_cur_time, last_box, last_name = char_list[-1]
                 

            char_list.append((cur_time, box, name))

        while True:
            try:
                frame, results = next(cap)
                cur_time = time.time()
                
                frame = image.cv2_putText(frame, f"str : {char_list}", (0, 20), 1, (0, 255, 0), 2)
                for hand_label, box, name, proba in results:
                        x, y, w, h = box
                        #center_x = x + int(w / 2)
                        #center_y = y + int(h / 2)
                        add_char(cur_time, box, name)

                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        frame = image.cv2_putText(frame, f"name : {name}, proba : {proba:.2f}", (x, y - 20), 1, (0, 0, 255), 2)

                cv2.imshow("test_char_predict", frame)
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break

            except KeyboardInterrupt as e:
                break

        cv2.destroyAllWindows()
        cap.close()

if __name__ == "__main__":
    cur_dir = os.path.dirname(__file__)
    dataset_dir = os.path.join(cur_dir, "..", "..", "dataset")
    dataset_dir = os.path.abspath(dataset_dir)

    util = HandTrainer()
    util.train(dataset_dir)

    util.test_char_predict()
    #util.camera_predict_capture()