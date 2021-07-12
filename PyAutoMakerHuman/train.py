import os
import pickle
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
        self.model = SVC(C=1.0, kernel="linear", probability=True)
        self.model.fit(data, labels)
        print("[INFO] train end")

        return self.model

    def save_svm(self, save_path):
        f = open(os.path.join(save_path, "svm_model"), "wb")
        f.write(pickle.dumps(self.model))
        f.close()

        f = open(os.path.join(save_path, "le"), "wb")
        f.write(pickle.dumps(self.le))
        f.close()

    def load_svm(self, load_path):
        self.model = pickle.loads(open(os.path.join(load_path, "svm_model"), "rb").read())
        self.le = pickle.loads(open(os.path.join(load_path, "le"), "rb").read())

    def predict(self, data):
        result = self.model.predict_proba(data)[0]
        idx = np.argmax(result)

        proba = result[idx]
        name = self.le.classes_[idx]

        return str(name), float(proba)

class KerasUtil:
    def __init__(self):
        pass

    def __del__(self):
        pass