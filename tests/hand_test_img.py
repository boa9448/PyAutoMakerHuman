import env
import cv2
import imutils
import os
import PyAutoMakerHuman as pamh


img_path = os.path.join("tests", "hand2.jpg")
img = cv2.imread(img_path)
hand = pamh.HandUtil()


result = hand.detect(img)
print(result.to_dict())

new_landmark_list = hand.extract(img)
boxes = result.get_box_list()

for box, landmark in zip(boxes, new_landmark_list):
    hand = img[box[1] : box[1] + box[3], box[0] : box[0] + box[2]]
    height, width = hand.shape[:2]
    for mark in landmark:
        mark = (int(mark[0] * width), int(mark[1] * height), mark[2])
        cv2.circle(hand, (mark[0], mark[1]), 1, (0, 255, 0), 2)

    cv2.imshow("view", hand)
    cv2.waitKey()
    cv2.destroyAllWindows()