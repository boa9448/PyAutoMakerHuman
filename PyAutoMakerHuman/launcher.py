import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from main_form import Ui_Form;

class TrainTestUtilForm(QMainWindow, Ui_Form):
    TRAIN_TEST_TYPE_LIST = ["손 탐지 기반", "홀리스틱 기반"]

    def __init__(self):
        super(TrainTestUtilForm, self).__init__()
        self.setupUi(self)

        def init_display():
            for train_test_type in self.TRAIN_TEST_TYPE_LIST:
                self.train_type_combo.addItem(train_test_type)
                self.test_type_combo.addItem(train_test_type)
        init_display()

        def init_handler():
            self.train_model_train_button.clicked.connect(self.train_model_train_button_handler)
            self.train_model_save_button.clicked.connect(self.train_model_save_button_handler)
            self.train_dataset_path_find_button.clicked.connect(self.train_dataset_path_find_button_handler)
        init_handler()

        self.show()

    def __del__(self):
        pass

    def train_model_train_button_handler(self):
        print("train_model_train_button call")
    
    def train_model_save_button_handler(self):
        print("train_model_save_button call")

    def train_dataset_path_find_button_handler(self):
        print("train_dataset_path_find_button_clicked call")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainTestUtilForm()
    app.exec()