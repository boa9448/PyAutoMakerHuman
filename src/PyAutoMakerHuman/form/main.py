import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QFrame, QStackedLayout
from qt_material import apply_stylesheet

from main_form import Ui_MainWindow
from game_form import Ui_Frame


class GameWindow(QFrame, Ui_Frame):
    def __init__(self, parent = None):
        super(GameWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.game_frame = GameWindow(self)
        
        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(self.game_frame)

        self.frame.setLayout(self.stack_layout)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = MainWindow()
    window.show()
    app.exec()
