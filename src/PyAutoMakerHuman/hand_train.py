import os
import time
import logging
from glob import glob

import cv2
import numpy as np

from . import hand
from . import train
from . import image

logging.basicConfig(level = logging.DEBUG)

class HandTrainer:
    def __init__(self, trainer : train.SvmUtil = train.SvmUtil()):
        self.detector = hand.HandUtil()
        self.trainer = trainer
        self.set_logger(logging.debug)

    def __del__(self):
        pass

    def set_logger(self, logger) -> None:
        self.logger = logger
        self.detector.set_logger(logger)
        self.trainer.set_logger(logger)

    def log(self, log_message: str) -> None:
        self.logger(f"[HandTrainer] : {log_message}")

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

    def predict(self, img : np.ndarray) -> tuple:
        result = self.detector.extract(img)
        if not result:
            return list()

        hand_result, datas = result
        predict_result = self.trainer.predict(datas)

        return hand_result, predict_result

if __name__ == "__main__":
    pass