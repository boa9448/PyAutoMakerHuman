import os
import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

class FaceResult:
    def __init__(self, img_size, result):
        self.img_size = img_size
        self.width = img_size[0]
        self.height = img_size[1]
        self.result = result

    def __del__(self):
        pass

    def __iter__(self):
        data_list = [("count", self.count())
                    , ("score", self.score())
                    , ("boxes", self.get_box_list())
                    , ("keypoints_list", self.get_keypoints())]

        for data in data_list:
            yield data

    def count(self):
        if self.result.detections is None:
            return 0

        return len(self.result.detections)

    def score(self):
        return [detection.score for detection in self.result.detections]

    def get_box_list(self, bRelative : bool = False):
        """
        바운딩 박스의 리트스를 리턴하는 함수
        bRelative가 True라면 정규화된 좌표를 리턴함
        """

        result_list = []
        if self.result.detections is None:
            return result_list

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

    def get_keypoints(self, bRelative : bool = False):
        result_list = []

        if self.result.detections is None:
            return result_list

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
    
    def draw_detections(self, img):
        if self.count() == 0:
            return

        for detection in self.result.detections:
            mp_drawing.draw_detection(img, detection)

    def to_dict(self):
        return dict(self.__iter__())

class FaceUtil:
    def __init__(self, model_selection : int = 1, min_detection_confidence : float = 0.5):
        self.detector = mp_face_detection.FaceDetection(
            model_selection = model_selection
            , min_detection_confidence = min_detection_confidence)

        self.embedder = None

    def __del__(self):
        self.detector.close()

    def detect(self, img):
        result = self.detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        height, width, _ = img.shape
        return FaceResult((width, height), result)

    def initExtractor(self):
        """self.embedder = cv2.dnn.readNetFromTorch(
                        os.path.join(os.environ["EMBED_MODEL_PATH"]
                        , "openface_nn4.small2.v1.t7"))
        """
        self.embedder = cv2.dnn.readNetFromTorch("C:\\openface_nn4.small2.v1.t7")
        

    def extract(self, img):
        result = self.detect(img)
        boxes = result.get_box_list()

        vec_list = []
        for box in boxes:
            x, y, w, h = box
            face = img[y:y+h, x:x+w]
            cv2.imshow("face", face)
            cv2.waitKey()
            cv2.destroyAllWindows()
            (fH, fW) = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
	            (0, 0, 0), swapRB=True, crop=False)
            self.embedder.setInput(faceBlob)
            vec = self.embedder.forward()
            vec_list.append((box, vec))

        return vec_list



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

    img = cv2.imread("C:\\mask2.jpg")
    face = FaceUtil()
    face.initExtractor()
    result = face.extract(img)