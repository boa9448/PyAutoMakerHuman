import env
import cv2
import imutils
import os
import PyAutoMakerHuman as pamh

hand = pamh.HandUtil()

cap = cv2.VideoCapture(0)

try:
    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            continue

        frame = cv2.flip(frame, 1)
        result = hand.detect(frame)

        print(result.to_dict())

        result.draw(frame)

        cv2.imshow("view", frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        
except KeyboardInterrupt as k:
    pass

cv2.destroyAllWindows()
cap.release()
