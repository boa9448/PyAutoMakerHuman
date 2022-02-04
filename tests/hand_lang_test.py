import cv2

import env
from PyAutoMakerHuman import hand_lang

lang = hand_lang.HandLang()
cap = cv2.VideoCapture(0)
while cap.isOpened():
    try:
        success, frame = cap.read()
        if not success:
            continue

        result = lang.predict(frame)
        print(result)

        cv2.imshow("view", frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()