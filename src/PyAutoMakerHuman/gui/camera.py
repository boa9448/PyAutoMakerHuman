import logging
from threading import Thread, Event, Lock

import cv2
import numpy as np
from PySide6.QtCore import QSize, Slot, Signal, QObject
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtGui import QPixmap, QColor, QCloseEvent

from .form.camera_form import Ui_Dialog
from .utils import numpy_to_pixmap

CAMERA_SIGNAL_FAIL = 0
CAMERA_SIGNAL_FRONT = 1
CAMERA_SIGNAL_SIDE = 2

logging.basicConfig(level=logging.DEBUG)

class CameraSignal(QObject):
    pixmap_signal = Signal(int, QPixmap)

    def front(self, pixmap):
        self.pixmap_signal.emit(CAMERA_SIGNAL_FRONT, pixmap)

    def side(self, pixmap):
        self.pixmap_signal.emit(CAMERA_SIGNAL_SIDE, pixmap)

    def fail(self):
        self.pixmap_signal.emit(CAMERA_SIGNAL_FAIL, QPixmap())


class CaptureThread(Thread):
    def __init__(self, cameras : tuple, camera_signal : CameraSignal):
        super().__init__()
        self.cameras = cameras
        self.camera_signal = camera_signal
        self.exit_event = Event()
        self.camera_change_lock = Lock()

    def __del__(self):
        logging.debug("[+] 캡쳐 스레드 소멸")

    def setCameras(self, cameras : tuple):
        if self.camera_change_lock.acquire(True):
            self.cameras = cameras
            self.camera_change_lock.release()
    
    def sleep_(self, timeout : float):
        self.exit_event.wait(timeout)

    def send_front(self, pixmap : QPixmap):
        self.camera_signal.front(pixmap)

    def send_side(self, pixmap : QPixmap):
        self.camera_signal.side(pixmap)

    def send_fail(self):
        self.camera_signal.fail()

    def run(self) -> None:
        logging.debug("[+] 캡쳐 스레드 시작")
        while not self.exit_event.is_set():
            self.camera_change_lock.acquire(True)
            for proc, camera in zip([self.send_front, self.send_side], self.cameras):
                if not camera.isOpened():
                    self.send_fail()
                    continue

                success, frame = camera.read()
                pixmap = numpy_to_pixmap(frame) if success else QPixmap()
                proc(pixmap)

            self.camera_change_lock.release()

        logging.debug("[+] 캡쳐 스레드 종료")

    def exit(self) -> None:
        self.exit_event.set()

    def join(self, timeout = None) -> None:
        self.exit()
        return super().join(timeout)
    

class CameraDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(CameraDialog, self).__init__()
        self.setupUi(self)
        self.init_handler()
        self.init_data()
        self.check_camera()
        self.exec()

    def __del__(self):
        self.front_camera.release()
        self.side_camera.release()

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        self.capture_thread.join()
        return super().closeEvent(arg__1)

    def init_handler(self) -> None:
        self.ok_button.clicked.connect(self.ok_button_handler)
        self.camera_change_button.clicked.connect(self.camera_change_button_handler)

    def init_data(self) -> None:
        self.front_camera = cv2.VideoCapture(0)
        self.side_camera = cv2.VideoCapture(1)
        self.camera_signal = CameraSignal()
        self.camera_signal.pixmap_signal.connect(self.camera_signal_handler)
        self.capture_thread = CaptureThread((self.front_camera, self.side_camera), self.camera_signal)
        self.capture_thread.start()

    def dispose_data(self) -> None:
        self.capture_thread.join()

        if self.front_camera.isOpened():
            self.front_camera.release()

        if self.side_camera.isOpened():
            self.side_camera.release()

    def check_camera(self) -> bool:
        title = "{} 카메라가 없습니다"
        text = "{} 카메라가 없습니다. 다시 로드 할까요?"

        def message_box(title : str, text : str):
            box = QMessageBox()
            box.setWindowTitle(title)
            box.setText(text)
            box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            return box.exec()

        if not self.front_camera.isOpened():
            if message_box(title.format("전면"), text.format("전면")) == QMessageBox.Yes:
                self.dispose_data()
                self.init_data()

            return False
        elif not self.side_camera.isOpened():
            if message_box(title.format("측면"), text.format("측면")) == QMessageBox.Yes:
                self.dispose_data()
                self.init_data()
                return False
            
            return True

        return True

    def front(self) -> cv2.VideoCapture:
        return self.front_camera

    def side(self) -> cv2.VideoCapture:
        return self.side_camera

    def cameras(self) -> tuple:
        return self.front(), self.side()

    @Slot(int, QPixmap)
    def camera_signal_handler(self, code : int, pixmap : QPixmap) -> None:
        if code == CAMERA_SIGNAL_FAIL:
            pass
        elif code == CAMERA_SIGNAL_FRONT:
            size = self.front_camera_img_label.size()
            pixmap = pixmap.scaled(size)
            self.front_camera_img_label.setPixmap(pixmap)
        elif code == CAMERA_SIGNAL_SIDE:
            size = self.side_camera_img_label.size()
            pixmap = pixmap.scaled(size)
            self.side_camera_img_label.setPixmap(pixmap)

    @Slot()
    def ok_button_handler(self) -> None:
        if not self.check_camera():
            return

        self.close()

    @Slot()
    def camera_change_button_handler(self) -> None:
        if not self.capture_thread.is_alive():
            return
        self.capture_thread.setCameras((self.side_camera, self.front_camera))
        self.front_camera, self.side_camera = self.side_camera, self.front_camera

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = CameraDialog()