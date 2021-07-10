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