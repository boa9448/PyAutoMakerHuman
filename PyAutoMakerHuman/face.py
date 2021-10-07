import os
import platform
import fnmatch
from typing import Generator
import imutils
import numpy as np
import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

if platform.system() == "Windows":
    import tensorflow.lite as tflite
else:
    import tflite_runtime.interpreter as tflite

if not ("FACE_MODEL_PATH" in os.environ):
    import __init__


class FaceResult:
    def __init__(self, img_size, result):
        self.img_size = img_size
        self.width = img_size[0]
        self.height = img_size[1]
        self.result = result

    def __del__(self):
        pass

    def __iter__(self) -> Generator:
        data_list = []

        count = self.count()
        if count == 0:
            return

        scores = self.scores()
        boxes = self.get_box_list()
        keypoints_list = self.get_keypoints()

        for score, box, keypoints in zip(scores, boxes, keypoints_list):
            data_list.append({
                "score" : score
                , "box" : box
                , "keypoints" : keypoints
            })

        for data in data_list:
            yield data

    def count(self) -> int:
        if self.result.detections is None:
            return 0

        return len(self.result.detections)

    def scores(self) -> list:
        if self.count() == 0:
            return None

        return [detection.score for detection in self.result.detections]

    def get_box_list(self, bRelative : bool = False) -> list:
        """
        바운딩 박스의 리트스를 리턴하는 함수
        bRelative가 True라면 정규화된 좌표를 리턴함
        """

        result_list = []
        if self.count() == 0:
            return None

        for detection in self.result.detections:
            box = detection.location_data.relative_bounding_box
            result_list.append([
                box.xmin
                , box.ymin
                , box.width
                , box.height
            ])
        
        if not bRelative:
            width, height = self.img_size
            for idx in range(len(result_list)):
                result = result_list[idx]
                result_list[idx] = [
                    int(result[0] * width)
                    , int(result[1] * height)
                    , int(result[2] * width)
                    , int(result[3] * height)
                ]

        return result_list

    def get_keypoints(self, bRelative : bool = False) -> list:
        result_list = []

        if self.count() == 0:
            return None

        for detection in self.result.detections:
            keypoint_list = list(detection.location_data.relative_keypoints)
            result_list.append(
                [(point.x, point.y) for point in keypoint_list]
            )


        if not bRelative:
            width, height = self.img_size
            for idx in range(len(result_list)):
                result = result_list[idx]
                result_list[idx] = [
                    (int(point[0] * width), int(point[1] * height)) for point in result
                ]

        return result_list
    
    def draw(self, img):
        if self.count() == 0:
            return

        for detection in self.result.detections:
            mp_drawing.draw_detection(img, detection)

class FaceUtil:
    def __init__(self, model_selection : int = 1, min_detection_confidence : float = 0.8):
        self.logger = None
        self.detector = mp_face_detection.FaceDetection(
            model_selection = model_selection
            , min_detection_confidence = min_detection_confidence)

        self.init_extractor()
        self.init_mask_classifier()

    def __del__(self):
        self.detector.close()

    def set_logger(self, logger):
        self.logger = logger

    def log(self, log : str, color : tuple = (255, 255, 255)) -> None:
        if self.logger is None:
            print(log)
            return

        self.logger(log, color)

    def detect(self, img):
        result = self.detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        height, width, _ = img.shape
        return FaceResult((width, height), result)
    
    def init_mask_classifier(self):
        self.mask_classifier = tflite.Interpreter(os.path.join(os.environ["FACE_MODEL_PATH"]
                                                , "mask_classifier.tflite"))

        self.mask_classifier.allocate_tensors()

        self.input_details = self.mask_classifier.get_input_details()
        self.output_details = self.mask_classifier.get_output_details()

        self.input_shape = self.input_details[0]['shape']
        self.height = self.input_shape[1]
        self.width = self.input_shape[2]

    def mask_predict(self, img):
        face = img
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (self.width, self.height))
        face = face.astype(dtype = np.float32)
        face /= 255.

        input_data = [face]
        self.mask_classifier.set_tensor(self.input_details[0]['index'], input_data)
        self.mask_classifier.invoke()

        (mask, withoutMask) = self.mask_classifier.get_tensor(self.output_details[0]['index'])[0]
        mask_use = True if mask > withoutMask else False
        proba = mask if mask > withoutMask else withoutMask

        return (mask_use, proba)


    def init_extractor(self):
        #경로 제대로 설정 해야함
        self.embedder = cv2.dnn.readNetFromTorch(
                        os.path.join(os.environ["FACE_MODEL_PATH"]
                        , "openface_nn4.small2.v1.t7"))

    def extract(self, img):
        result = self.detect(img)
        boxes = result.get_box_list()

        vec_list = []
        if not boxes:
            return vec_list    

        for box in boxes:
            x, y, w, h = box
            face = img[y:y+h, x:x+w]
            (fH, fW) = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
	            (0, 0, 0), swapRB=True, crop=False)
            self.embedder.setInput(faceBlob)
            vec = self.embedder.forward()
            vec_list.append((box, vec.flatten()))

        return vec_list

    def extract_dataset(self, dataset_path):
        ext_list = ["*.jpg", "*.png", "*.JPG", "*.PNG"]
        file_list = []
        
        for ext in ext_list:
            for root, dirs, files in os.walk(dataset_path):
                if not files:
                    continue

                for file in fnmatch.filter(files, ext):
                    file_list.append(os.path.join(root, file))

        print(f"[INFO] file count : {len(file_list)}")

        name_list = []
        embed_list = []
        for idx, file in enumerate(file_list):
            print(f"[INFO] process... {idx + 1}/{len(file_list)}")
            name = file.split(os.path.sep)[-2]

            img = cv2.imread(file)
            img = imutils.resize(img, width=600)
            embed = self.extract(img)
            if not embed:
                continue

            name_list.append(name)
            embed_list.append(embed[0][1]) #1개, 박스 정보는 제외

        print("done")
        return {"name" : name_list, "data" : embed_list}






if __name__ == "__main__":
    def detect_test():
        cap = cv2.VideoCapture(0)
        face = FaceUtil()
        while cap.isOpened():
            try:
                success, frame = cap.read()
                if not success:
                    continue
                
                result = face.detect(frame)
                result.draw_detections(frame)

                cv2.imshow("view", frame)
                cv2.waitKey(1)
                print(result.to_dict())
            except Exception as e:
                print(e)
        
        cv2.destroyAllWindows()
        cap.release()

    def extract_test():
        os.chdir("..")
        os.environ["FACE_MODEL_PATH"] = os.path.join("PyAutoMakerHuman\\", "models")
        img = cv2.imread("C:\\th.jpg")
        face = FaceUtil()
        face.initExtractor()
        result = face.extract(img)

        return result

    #result = extract_test()
    def extract_test2():
        os.environ["FACE_MODEL_PATH"] = os.path.join("PyAutoMakerHuman\\", "models")
        face = FaceUtil()
        face.initExtractor()
        result = face.extract_dataset("dataset")

        return result

