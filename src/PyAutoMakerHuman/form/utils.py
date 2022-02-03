import cv2
import numpy as np

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtWidgets import QApplication

def numpy_to_pixmap(img : np.ndarray) -> QPixmap:
    h, w, c = img.shape
    if c == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    qimg = QImage(img.data, h, w, c * h, QImage.Format_BGR888)
    pixmap = QPixmap(qimg)
    return pixmap