import env
import cv2
import imutils
import os
import PyAutoMakerHuman as pamh

img_path = "C:\\th.jpg"

face = pamh.FaceUtil(min_detection_confidence=0.7)

img = cv2.imread(img_path)
result = face.detect(img)

face_box_list = result.get_box_list()
for box in face_box_list:
    face_roi = img[box[1] : box[1] + box[3], box[0] : box[0] + box[2]]
    mask_use, proba = face.mask_predict(face_roi)
    
    color = (0, 255, 0) if mask_use else (0, 0, 255)
    text = "mask" if mask_use else "no mask" 
    text = f"{text} : {proba:.2f}"
    cv2.putText(img, text, (box[0], box[1] - 25), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color, 2)

cv2.imshow("view", img)
cv2.waitKey()
cv2.destroyAllWindows()