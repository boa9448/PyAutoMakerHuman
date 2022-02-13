import cv2
import numpy as np


from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QImage


from ..image import cv2_imread, cv2_putText

def draw_char_img(target_img_label : QLabel, char : str, font_scale = 20) -> None:
    label_size = target_img_label.size().toTuple()
    img = np.ndarray((*label_size[::-1], 3), np.uint8)
    img.fill(255)
    img = cv2_putText(img, char, (0, 0), font_scale, (0, 0, 0), 4, center=True)

    pixmap = numpy_to_pixmap(img)
    target_img_label.setPixmap(pixmap)

def numpy_to_pixmap(img : np.ndarray) -> QPixmap:
    h, w, c = img.shape
    if c == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    qimg = QImage(img.data, w, h, 3 * w, QImage.Format_BGR888)
    pixmap = QPixmap(qimg)
    return pixmap