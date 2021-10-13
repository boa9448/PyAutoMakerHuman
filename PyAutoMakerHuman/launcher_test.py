import os
import sys
import time
import random
from threading import Thread, Event
from glob import glob
from typing import List

import cv2
import numpy as np
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from main_form import Ui_Form
# 테스트 개발엔 잠시 주석
# import face
import hand
import pose
import train
from custom_signal import LogSignal, TrainExitSignal, TestCamSignal, TrainDataSetAddEndSignal

class TrainTestUtilForm(QMainWindow, Ui_Form):
    TRAIN_TEST_TYPE_DICT = {"수형 인식" : 0, "수형 인식(홀리스틱)" : 1, "얼굴 인식" : 2}

    def __init__(self):
        super(TrainTestUtilForm, self).__init__()
        self.setupUi(self)

        def init_data():
            self.log_signal = LogSignal()

            self.train_dataset_add_end_signal = TrainDataSetAddEndSignal()
            self.train_dataset_add_thread = None
            self.train_dataset_add_thread_exit_event = Event()

            min_thresh = self.train_thresh_spin_edit.text()
            min_thresh = float(min_thresh) / 100
            self.train_detector = self.init_detector(0, min_thresh)
            self.train_trainer = train.SvmUtil()

            min_thresh = self.train_thresh_spin_edit.text()
            min_thresh = float(min_thresh) / 100
            self.test_detector = self.init_detector(0, min_thresh)
            self.test_trainer = train.SvmUtil()
        init_data()

        def init_display():
            for model_type in self.TRAIN_TEST_TYPE_DICT:
                self.train_type_combo.addItem(model_type)
                self.test_type_combo.addItem(model_type)

            # 잠시 숨김
            self.train_two_hand_checkBox.hide()
        init_display()

        def init_handler():
            self.log_signal.sig.connect(self.log)
            self.train_dataset_add_end_signal.sig.connect(self.train_dataset_add_end_signal_handler)

            self.train_type_combo.currentIndexChanged.connect(self.train_type_combo_chnaged_handler)
            self.train_model_train_button.clicked.connect(self.train_model_train_button_clicked_handler)
            self.train_model_save_button.clicked.connect(self.train_model_save_button_clicked_handler)
            self.train_dataset_path_find_button.clicked.connect(self.train_dataset_path_find_button_clicked_handler)
            self.train_dataset_list.itemSelectionChanged.connect(self.train_dataset_list_itemSelectionChanged_handler)
            self.train_thresh_apply_button.clicked.connect(self.train_thresh_apply_button_clicked_handler)

            self.test_type_combo.currentIndexChanged.connect(self.test_type_combo_chnaged_handler)

        init_handler()

        self.log("프로그램 시작")
        
    def __del__(self):
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        return super().closeEvent(event)

    def init_detector(self, idx : int, thresh : float) -> hand.HandUtil or pose.PoseUtil or None:
        detector = None

        if idx == 0:
            detector = hand.HandUtil(min_detection_confidence = thresh)
        elif idx == 1:
            detector = pose.PoseUtil()
        elif idx == 2:
            pass

        return detector

    def log(self, log_message : str, color : tuple = (255, 255, 255)) -> None:
        cur_time =  time.strftime('%X', time.localtime(time.time()))
        log_message = f"[{cur_time}] : {log_message}"
        log_message_item = QListWidgetItem(log_message)
        bg_color = QColor(*color)
        log_message_item.setBackground(bg_color)
        self.main_log_list.addItem(log_message_item)
        self.main_log_list.scrollToBottom()

    def get_folder_paths(self) -> list or None:
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec():
            folder_paths = dlg.selectedFiles()
            if folder_paths:
                return folder_paths

        return None

    def get_file_list(self, folder_path : str) -> list:
        file_lsit = glob(os.path.join(folder_path, "**", "*.*"), recursive = True)
        return file_lsit

    def ndarray_to_qimage(self, img : np.ndarray) -> QImage:
        height, width, channel = img.shape
        bytesPerLine = channel * width
        qImg = QImage(img.data, width, height, bytesPerLine
                        , QImage.Format_BGR888 if channel == 3 else QImage.Format_BGR30)
        return qImg

    def draw_label(self, img_label : QLabel, qImg : QImage) -> None:
        pixmap = QPixmap(qImg)
        pixmap = pixmap.scaled(img_label.size(), aspectMode= Qt.IgnoreAspectRatio)
        img_label.setPixmap(pixmap)

    @Slot()
    def train_dataset_add_end_signal_handler(self):
        self.train_dataset_list.setDisabled(False)
        self.train_dataset_add_thread = None

    @Slot()
    def train_type_combo_chnaged_handler(self, idx : int) -> None:
        print("훈련 타입 변경")
        min_thresh = self.train_thresh_spin_edit.text()
        min_thresh = float(min_thresh) / 100
        self.train_detector = self.init_detector(idx, min_thresh)

    @Slot()
    def train_model_train_button_clicked_handler(self):
        print("훈련 모델 버튼 클릭")

    @Slot()
    def train_model_save_button_clicked_handler(self):
        print("훈련 모델 저장 버튼")

    @Slot()
    def train_dataset_path_find_button_clicked_handler(self):
        print("훈련 데이터셋 찾기 버튼")
        folder_paths = self.get_folder_paths()
        if folder_paths is None:
            return

        def file_add_thread_func(folder_path : str, target_list : QListWidget, end_signal : TrainDataSetAddEndSignal) -> None:
            file_list = self.get_file_list(folder_path)
            for file in file_list:
                item = QListWidgetItem(file)
                target_list.addItem(item)

            end_signal.sig.emit()

        self.train_dataset_add_thread_exit_event.clear()
        self.train_dataset_list.clear()
        self.train_dataset_list.setDisabled(True)
        self.train_file_add_thread = Thread(target=file_add_thread_func, args=(folder_paths[0], self.train_dataset_list, self.train_dataset_add_end_signal))
        self.train_file_add_thread.start()

    @Slot()
    def train_dataset_list_itemSelectionChanged_handler(self):
        print("훈련 데이터셋 선택 아이템 체인지")
        file_path = self.train_dataset_list.currentItem().text()
        img = cv2.imread(file_path)
        if img is None:
            return

        qImg = self.ndarray_to_qimage(img)
        self.draw_label(self.train_original_img_label, qImg)

        result = self.train_detector.detect(img)
        scores = result.scores()
        if scores is None:
            self.log(f"찾은 오브젝트가 없습니다")
        else:
            self.log(f"찾은 개수 : {len(scores)} ({scores})")

        result.draw(img)
        qImg = self.ndarray_to_qimage(img)
        self.draw_label(self.train_result_img_label, qImg)

    
    @Slot()
    def train_thresh_apply_button_clicked_handler(self):
        print("훈련 데이터셋 임계율 설정 버튼")
        min_thresh = self.train_thresh_spin_edit.text()
        min_thresh = float(min_thresh) / 100
        idx = self.train_type_combo.currentIndex()
        self.train_detector = self.init_detector(idx, min_thresh)

    @Slot()
    def test_type_combo_chnaged_handler(self, idx : int) -> None:
        print("테스트 타입 변경")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainTestUtilForm()
    window.show()
    app.exec()