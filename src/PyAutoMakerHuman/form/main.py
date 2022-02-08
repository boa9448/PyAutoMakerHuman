import sys
from threading import Thread, Event

from PySide6.QtCore import Slot, Signal, QObject
from PySide6.QtWidgets import QMainWindow, QApplication, QFrame, QStackedLayout
from PySide6.QtGui import QPixmap
from qt_material import apply_stylesheet

from .main_form import Ui_MainWindow
from .study import StudyWindow
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
        self.game_frame = StudyWindow(self)

        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(self.game_frame)

        self.stack_layout.addWidget(QFrame())
        self.frame.setLayout(self.stack_layout)

        self.game_frame.init()
        text = "거울모드 {}".format("On" if self.game_frame.get_mirror_mode() else "Off")
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
        mode = self.game_frame.get_mirror_mode()
        self.game_frame.set_mirror_mode(not mode)
        text = "거울모드 {}".format("On" if self.game_frame.get_mirror_mode() else "Off")
        self.mirror_mode_button.setText(text)

def start_main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    start_main()
