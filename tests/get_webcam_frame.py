import os
import cv2
import numpy as np
import time
import requests as rq

save_path = "temp"
target_url = "http://172.30.1.55:8080/shot.jpg"

start = time.time()
while True:
    data = rq.get(target_url)
    data = np.frombuffer(data.content, dtype=np.byte)
    frame = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)

    file_name = os.path.join(save_path, f"frame_{time.time()}.jpg")
    cv2.imwrite(file_name, frame)
    cv2.imshow("view", frame)
    cv2.waitKey(1)

    if time.time() - start > 5:
        break

cv2.destroyAllWindows()