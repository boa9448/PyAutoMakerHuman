import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QFrame, QStackedLayout
from qt_material import apply_stylesheet

from main_form import Ui_MainWindow
from game_form import Ui_Frame


class GameWindow(QFrame, Ui_Frame):
    CHAR_CHILD_COMBO_ITEMS = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅍ", "ㅎ"
                                , "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ", "ㄳ", "ㄵ", "ㄶ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅄ"]
    CHAR_PARENT_COMBO_ITEMS = ["ㅏ", "ㅐ", "ㅑ" , "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ"
                                , "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ," "ㅡ", "ㅢ", "ㅣ"]

    def __init__(self, parent = None):
        super(GameWindow, self).__init__(parent)
        self.setupUi(self)

        self.init_handler()
        self.init_display()
        self.show()

    def init_handler(self) -> None:
        self.char_child_combo.currentIndexChanged.connect(self.char_combo_change_handler)
        self.char_parent_combo.currentIndexChanged.connect(self.char_combo_change_handler)

    def init_display(self) -> None:
        self.char_child_combo.addItems(self.CHAR_CHILD_COMBO_ITEMS)
        self.char_parent_combo.addItems(self.CHAR_PARENT_COMBO_ITEMS)

    def char_combo_change_handler(self, idx : int) -> None:
        if self.sender() == self.char_child_combo:
            target_list = self.CHAR_CHILD_COMBO_ITEMS
        else:
            target_list = self.CHAR_PARENT_COMBO_ITEMS
            
        print(target_list[idx])

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
        

    def init_handler(self):
        self.study_mode_button.clicked.connect(self.study_mode_button_handler)
        self.lang_mode_button.clicked.connect(self.lang_mode_button_handler)
        self.mirror_mode_button.clicked.connect(self.mirror_mode_button_handler)

    def init_display(self):
        pass

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
