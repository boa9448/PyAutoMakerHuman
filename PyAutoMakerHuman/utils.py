import cv2
import numpy as np
import requests as rq
from image import cv2_imread


def get_webcam_frame(target_url : str):
    try:
        data = rq.get(target_url)
        data = np.frombuffer(data.content, dtype=np.byte)
        frame = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)

        return frame

    except:
        pass

    return None