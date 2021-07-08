import cv2
import imutils
from imutils import paths
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC




class TrainUtil:
    def load_dataset(self, dataSetPath):
        pass

    def train_svm(self, dataSetPath, thresh = 0.8):
        data = self.load_dataset(dataSetPath, thresh)
        emb = data["embeddings"]

        self.le = LabelEncoder()
        labels = self.le.fit_transform(data["names"])
        
        print("[INFO] training model...")
        self.recognizer = SVC(C=1.0, kernel="linear", probability=True)
        self.recognizer.fit(emb, labels)
        print("[INFO] train end")