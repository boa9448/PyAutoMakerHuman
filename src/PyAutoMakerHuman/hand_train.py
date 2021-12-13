import os
from glob import glob

import cv2
import numpy as np

import hand
import train

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

    def predict(self, img : np.ndarray) -> list:
        datas = self.detector.extract(img)
        if datas is None:
            return list()

        results = []
        for hand_label, box, data in datas:
            name, proba = self.trainer.predict([data])
            results.append((hand_label, box, name, proba))

        return results

    def test_camera(self, idx : int = 0) -> None:
        cap = cv2.VideoCapture(idx)
        while cap.isOpened():
            try:
                success, frame = cap.read()
                if not success:
                    continue

                frame = cv2.flip(frame, 1)
                results = util.predict(frame)
                for hand_label, box, name, proba in results:
                    x, y, w, h = box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(frame, f"name : {name}, proba : {proba:.2f}", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                cv2.imshow("test_camera", frame)
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break
                
            except KeyboardInterrupt as e:
                break

        cv2.destroyAllWindows()
        cap.release()

if __name__ == "__main__":
    cur_dir = os.path.dirname(__file__)
    dataset_dir = os.path.join(cur_dir, "..", "..", "dataset")
    dataset_dir = os.path.abspath(dataset_dir)

    util = HandTrainer()
    util.train(dataset_dir)

    util.test_camera()