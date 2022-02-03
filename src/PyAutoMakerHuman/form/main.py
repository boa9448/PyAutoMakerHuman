import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QFrame, QStackedLayout
from qt_material import apply_stylesheet

from main_form import Ui_MainWindow
from game import GameWindow

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.game_frame = GameWindow(self)

        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(self.game_frame)

        self.stack_layout.addWidget(QFrame())
        self.frame.setLayout(self.stack_layout)

        self.init_handler()

        self.game_frame.init()

    def init_handler(self):
        self.study_mode_button.clicked.connect(self.study_mode_button_handler)
        self.lang_mode_button.clicked.connect(self.lang_mode_button_handler)
        self.mirror_mode_button.clicked.connect(self.mirror_mode_button_handler)

    def study_mode_button_handler(self) -> None:
        self.stack_layout.setCurrentIndex(0)

    def lang_mode_button_handler(self) -> None:
        self.stack_layout.setCurrentIndex(1)

    def mirror_mode_button_handler(self) -> None:
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = MainWindow()
    window.show()
    app.exec()
