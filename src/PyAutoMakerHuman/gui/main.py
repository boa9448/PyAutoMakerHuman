import sys
from threading import Thread, Event

from PySide6.QtCore import Slot, Signal, QObject
from PySide6.QtWidgets import QMainWindow, QApplication, QFrame, QStackedLayout
from PySide6.QtGui import QPixmap
from qt_material import apply_stylesheet

from .form.main_form import Ui_MainWindow
from .study import StudyWindow
from .test import TestWindow
from .camera import CameraDialog

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.init_handler()
        self.init_display()

    def init_handler(self):
        self.study_mode_button.clicked.connect(self.study_mode_button_handler)
        self.lang_mode_button.clicked.connect(self.lang_mode_button_handler)
        self.mirror_mode_button.clicked.connect(self.mirror_mode_button_handler)

    def init_display(self) -> None:
        self.camera_dialog = CameraDialog()
        self.study_frame = StudyWindow(self, self.camera_dialog.cameras())
        self.test_frame = TestWindow(self, self.camera_dialog.cameras())

        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(self.study_frame)

        self.stack_layout.addWidget(self.test_frame)
        self.frame.setLayout(self.stack_layout)

        self.study_frame.init()
        self.test_frame.init()
        text = "거울모드 {}".format("On" if self.study_frame.mirror_mode else "Off")
        self.mirror_mode_button.setText(text)

    def get_cameras(self) -> tuple:
        return self.camera_dialog.cameras()

    @Slot()
    def study_mode_button_handler(self) -> None:
        self.stack_layout.setCurrentIndex(0)

    @Slot()
    def lang_mode_button_handler(self) -> None:
        self.stack_layout.setCurrentIndex(1)

    @Slot()
    def mirror_mode_button_handler(self) -> None:
        target_frame = self.stack_layout.currentWidget()
        mode = target_frame.mirror_mode
        target_frame.mirror_mode = not mode
        text = "거울모드 {}".format("On" if target_frame.mirror_mode else "Off")
        self.mirror_mode_button.setText(text)

def start_main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    start_main()
