import os
import sys
import time
from glob import glob

import cv2
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from main_form import Ui_Form
import face, hand, pose, train

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
    TRAIN_TEST_TYPE_LIST = ["얼굴 인식", "수형 인식", "수형 인식(홀리스틱)"]

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
            self.train_type_combo.currentIndexChanged.connect(self.train_type_combo_change_handler)
            self.train_model_train_button.clicked.connect(self.train_model_train_button_handler)
            self.train_model_save_button.clicked.connect(self.train_model_save_button_handler)
            self.train_dataset_path_find_button.clicked.connect(self.train_dataset_path_find_button_handler)
            self.train_dataset_list.itemSelectionChanged.connect(self.train_dataset_list_select_change_handler)
            self.train_thresh_apply_button.clicked.connect(self.train_thresh_button_click_handler)
        init_handler()

        def init_data():
            thresh = self.train_thresh_spin_edit.text()
            thresh = float(thresh) / 100

            cur_type = self.train_type_combo.currentText()
            self.detector = self.init_detector(cur_type, thresh)
        init_data()

        self.log("프로그램 켜짐")
        self.show()

    def __del__(self):
        pass

    def init_detector(self, type_name, thresh):
        detector = None
        if type_name == self.TRAIN_TEST_TYPE_LIST[0]:
            detector = face.FaceUtil(1, thresh)
        elif type_name == self.TRAIN_TEST_TYPE_LIST[1]:
            detector = hand.HandUtil(min_detection_confidence = thresh)
        elif type_name == self.TRAIN_TEST_TYPE_LIST[2]:
            # 홀리스틱(손) 작성하면 여기로
            pass
        else:
            pass

        return detector

    def messagebox(self, message, title = "확인 메시지"):
        box = QMessageBox()
        box.setText(message)
        box.setWindowTitle(title)
        box.exec()

    def log(self, log_message, color = (255, 255, 255)):
        cur_time =  time.strftime('%X', time.localtime(time.time()))
        log_message = f"[{cur_time}] : {log_message}"
        log_message_item = QListWidgetItem(log_message)
        bg_color = QColor(*color)
        log_message_item.setBackground(bg_color)
        self.train_log_list.addItem(log_message_item)
        self.train_log_list.scrollToBottom()

    def add_dataset_to_list(self, target_list, dataset_folder_path):
        print(os.path.join(dataset_folder_path, "**", "*.*"))
        dataset_file_list = glob(os.path.join(dataset_folder_path, "**", "*.*"), recursive = True)
        target_list.addItems(dataset_file_list)
        
        self.log(f"지정한 경로에서 총 : {len(dataset_file_list)}개의 파일을 찾았습니다")

    def view_original_img(self, img_path):
        pixmap = QPixmap()
        pixmap.load(img_path)
        if pixmap.isNull():
            self.messagebox("이미지를 열 수 없습니다.")
            self.log("이미지를 열 수 없습니다", (255, 0, 0))
            raise Exception("이미지를 열 수 없습니다")

        label_size = self.train_original_img_label.size()
        pixmap = pixmap.scaled(label_size, aspectMode = Qt.IgnoreAspectRatio)
        self.train_original_img_label.setPixmap(pixmap)

    def detect_drow(self, img_path) -> QImage:
        img = cv2.imread(img_path)
        if img is None:
            self.messagebox("이미지를 열 수 없습니다.")
            self.log("이미지를 열 수 없습니다", (255, 0, 0))
            raise Exception("이미지를 열 수 없습니다")

        result = self.detector.detect(img)

        scores = result.score()
        if scores is None:
            self.log(f"찾은 오브젝트가 없습니다")
        else:
            self.log(f"찾은 개수 : {len(scores)} ({scores})")


        result.draw(img)
        height, width, channel = img.shape
        bytesPerLine = channel * width
        qImg = QImage(img.data, width, height, bytesPerLine
                        , QImage.Format_BGR888 if channel == 3 else QImage.Format_BGR30)
        return qImg

    def view_landmark_img(self, img_path):
        qImg = self.detect_drow(img_path)
        pixmap = QPixmap(qImg)
        label_size = self.train_result_img_label.size()
        pixmap = pixmap.scaled(label_size, aspectMode= Qt.IgnoreAspectRatio)
        self.train_result_img_label.setPixmap(pixmap)

    def train_dataset_list_select_change_handler(self):
        item = self.train_dataset_list.currentItem()
        try:
            self.log(f"{item.text()} 을(를) 열기를 시도합니다")
            self.view_original_img(item.text())
            self.view_landmark_img(item.text())
            self.log(f"{item.text()} 의 작업을 끝냈습니다")
        except:
            self.log(f"{item.text()} 의 작업을 실패했습니다", (255, 0, 0))

    def train_thresh_button_click_handler(self):
        cur_text = self.train_type_combo.currentText()
        thresh = self.train_thresh_spin_edit.text()
        thresh = float(thresh) / 100
        self.detector = self.init_detector(cur_text, thresh)
        self.log("변경 완료")

    def train_type_combo_change_handler(self, idx):
        self.train_thresh_button_click_handler()

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