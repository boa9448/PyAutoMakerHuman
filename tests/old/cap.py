import cv2
import time
import os

save_path = "temp"
cap = cv2.VideoCapture(0)

start = time.time()
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    file_name = f"frame_{time.time()}.jpg"
    cv2.imwrite(os.path.join(save_path, file_name), frame)
    cv2.imshow("view", frame)
    cv2.waitKey(100)

    if time.time() - start > 10:
        break

cap.release()
cv2.destroyAllWindows()