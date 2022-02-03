from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QPixmap, QColor

from camera_form import Ui_Dialog


class CameraDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(CameraDialog, self).__init__()
        self.setupUi(self)
        self.init_handler()
        self.exec()

    def init_handler(self) -> None:
        self.ok_button.clicked.connect(self.ok_button_handler)

    @Slot()
    def ok_button_handler(self) -> None:
        self.close()