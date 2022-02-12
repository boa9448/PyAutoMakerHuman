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
        
        frame = cv2.flip(frame, 1)
        result = lang.predict_str(frame)
        print(result)

        cv2.imshow("view", frame)
        if cv2.waitKey(1) & 0xff == ord('c'):
            lang.remove_char()

    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()