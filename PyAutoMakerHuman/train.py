import cv2
import imutils
import numpy as np
from imutils import paths
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC


class SvmUtil:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def train_svm(self, data, label):
        self.le = LabelEncoder()
        labels = self.le.fit_transform(label)
        
        print("[INFO] training model...")
        self.recognizer = SVC(C=1.0, kernel="linear", probability=True)
        self.recognizer.fit(data, labels)
        print("[INFO] train end")

        return self.recognizer

    def save_svm(self, save_path):
        pass

    def load_svm(self, load_path):
        pass

    def predict(self, data):
        result = self.recognizer.predict_proba(data)[0]
        idx = np.argmax(result)

        proba = result[idx]
        name = self.le.classes_[idx]

        return name, proba