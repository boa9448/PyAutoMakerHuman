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
                    , ("boxes", self.get_box_list())
                    , ("keypoints_list", self.get_keypoints())]

        for data in data_list:
            yield data

    def count(self):
        return len(self.result.detections)

    def score(self):
        return [detection.score for detection in self.result.detections]

    def get_box_list(self, bRelative : bool = False):
        """
        바운딩 박스의 리트스를 리턴하는 함수
        bRelative가 True라면 정규화된 좌표를 리턴함
        """

        result_list = []
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

    def to_dict(self):
        return self.__iter__()

class FaceUtil:
    def __init__(self, model_selection = 1, min_detection_confidence = 0.5):
        self.detector = mp_face_detection.FaceDetection(
            model_selection = 1
            , min_detection_confidence = 0.5)

    def __del__(self):
        self.detector.close()

    def detect(self, img):
        result = self.detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        height, width, _ = img.shape
        return FaceResult((width, height), result)

if __name__ == "__main__":
    img = cv2.imread("C:\\th.jpg")
    face = FaceUtil()
    result = face.detect(img)
    box_list = result.get_box_list()
    for box in box_list:
        cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3])
        , (0, 255, 0), 2)

    cv2.imshow("view", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    point_list = result.get_keypoints()
    for point in point_list:
        [cv2.circle(img, key, 2, (0, 255, 255), 2) for key in point]

    cv2.imshow("view", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    print(result.score())