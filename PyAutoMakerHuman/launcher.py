import os
import sys
import cv2
from glob import glob
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from main_form import Ui_Form;

class RunOption:
    def __init__(self):
        self.dataset_folder_path = None

    def __del__(self):
        pass

    def set_dataset_folder_path(self, dataset_folder_path) -> None:
        self.dataset_folder_path = dataset_folder_path

    def get_dataset_folder_path(self) -> str or None:
        return self.dataset_folder_path

class TrainTestUtilForm(QMainWindow, Ui_Form):
    TRAIN_TEST_TYPE_LIST = ["손 탐지 기반", "홀리스틱 기반"]

    def __init__(self):
        self.run_option = RunOption()

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
            self.train_dataset_list.itemClicked.connect(self.train_dataset_list_click_handler)
        init_handler()

        self.show()

    def __del__(self):
        pass

    def add_dataset_to_list(self, target_list, dataset_folder_path):
        dataset_file_list = glob(os.path.join(dataset_folder_path, "*.*"), recursive = True)
        #[print(file_path) for file_path in dataset_file_list]
        target_list.addItems(dataset_file_list)

    def view_original_img(self, img_path):
        pixmap = QPixmap()
        pixmap.load(img_path)
        self.train_original_img_label.setPixmap(pixmap)

    def train_dataset_list_click_handler(self, item):
        self.view_original_img(item.text())

    def train_model_train_button_handler(self):
        print("train_model_train_button call")
    
    def train_model_save_button_handler(self):
        print("train_model_save_button call")

    def train_dataset_path_find_button_handler(self):
        print("train_dataset_path_find_button_clicked call")
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec():
            folder_path = dlg.selectedFiles()
            if folder_path:
                self.run_option.set_dataset_folder_path(folder_path[0])
                self.train_dataset_list.clear()
                self.add_dataset_to_list(self.train_dataset_list, folder_path[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainTestUtilForm()
    app.exec()