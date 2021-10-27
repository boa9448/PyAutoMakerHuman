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
import face
import hand
import pose
import train
from custom_signal import LogSignal, CamSignal, WorkDoneSignal
from thread import WorkThread, WorkQThread, WorkPyThread
from image import cv2_imread, cv2_imwrite


def get_file_list(folder_path : str) -> list:
    file_lsit = glob(os.path.join(folder_path, "**", "*.*"), recursive = True)
    return file_lsit

class TrainTestUtilForm(QMainWindow, Ui_Form):
    TRAIN_TEST_TYPE_DICT = {"수형 인식" : 0, "수형 인식(홀리스틱)" : 1, "얼굴 인식" : 2}

    def __init__(self):
        super(TrainTestUtilForm, self).__init__()
        self.setupUi(self)

        def init_data():
            self.color_dict = dict()

            self.log_signal = LogSignal()

            self.test_dataset_add_end_signal = WorkDoneSignal()
            self.test_dataset_add_thread = None

            min_thresh = self.train_thresh_spin_edit.text()
            min_thresh = float(min_thresh) / 100
            self.test_detector = self.init_detector(0, min_thresh)
            self.test_trainer = train.SvmUtil()

            min_thresh = self.tools_thresh_spin_edit.text()
            min_thresh = float(min_thresh) / 100
            self.tools_detector = self.init_detector(0, min_thresh)

            self.test_use_cam = False
            self.test_cam_thread = None
            self.test_cam_signal = CamSignal()

            self.tools_cap = None
            self.tools_img_dict = dict()
            self.tools_cam_thread = None
            self.tools_cam_signal = CamSignal()
            self.tools_cam_done_signal = WorkDoneSignal()
        init_data()

        def init_display():
            for model_type in self.TRAIN_TEST_TYPE_DICT:
                self.train_type_combo.addItem(model_type)
                self.test_type_combo.addItem(model_type)
                self.tools_type_combo.addItem(model_type)

            # 잠시 숨김
            self.train_two_hand_checkBox.hide()
        init_display()

        def init_handler():
            self.log_signal.sig.connect(self.log)
            self.train_dataset_add_end_signal.sig.connect(self.train_dataset_add_end_signal_handler)
            self.test_dataset_add_end_signal.sig.connect(self.test_dataset_add_end_signal_handler)
            self.train_done_signal.sig.connect(self.train_model_train_button_clicked_handler)
            self.test_cam_signal.sig.connect(self.test_cam_signal_handler)
            self.tools_cam_signal.sig.connect(self.tools_cam_signal_handler)
            self.tools_cam_done_signal.sig.connect(self.tools_cam_done_signal_handler)

            self.main_menu_tab.currentChanged.connect(self.main_menu_tab_changed_hander)

            self.train_type_combo.currentIndexChanged.connect(self.train_type_combo_chnaged_handler)
            self.train_model_train_button.clicked.connect(self.train_model_train_button_clicked_handler)
            self.train_model_save_button.clicked.connect(self.train_model_save_button_clicked_handler)
            self.train_dataset_path_find_button.clicked.connect(self.train_dataset_path_find_button_clicked_handler)
            self.train_dataset_list.itemSelectionChanged.connect(self.train_dataset_list_itemSelectionChanged_handler)
            self.train_thresh_apply_button.clicked.connect(self.train_thresh_apply_button_clicked_handler)

            self.test_type_combo.currentIndexChanged.connect(self.test_type_combo_chnaged_handler)
            self.test_model_load_button.clicked.connect(self.test_model_load_button_handler)
            self.test_dataset_path_find_button.clicked.connect(self.test_dataset_path_find_button_handler)
            self.test_cam_use_check.stateChanged.connect(self.test_cam_use_check_handler)
            self.test_dataset_list.itemSelectionChanged.connect(self.test_dataset_list_itemSelectionChanged_handler)
            self.test_thresh_apply_button.clicked.connect(self.test_thresh_apply_button_clicked_handler)

            self.tools_type_combo.currentIndexChanged.connect(self.tools_type_combo_chnaged_handler)
            self.tools_thresh_apply_button.clicked.connect(self.tools_thresh_apply_button_clicked_handler)
            self.tools_capture_button.clicked.connect(self.tools_capture_button_handler)
            self.tools_video_button.clicked.connect(self.tools_video_button_handler)
            self.tools_save_path_find_button.clicked.connect(self.tools_save_path_find_button_handler)
            self.tools_img_list.itemSelectionChanged.connect(self.tools_img_list_itemSelectionChanged_handler)
            self.tools_img_remove_button.clicked.connect(self.tools_img_remove_button_handler)

        init_handler()

        self.log("프로그램 시작")
        
    def __del__(self):
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        thread_list = [self.train_dataset_add_thread, self.test_dataset_add_thread, self.test_cam_thread]
        for target_thread in thread_list:
            if target_thread is None:
                continue
            target_thread.exit()
            target_thread.join()

        return super().closeEvent(event)

    def init_detector(self, idx : int, thresh : float) -> hand.HandUtil or pose.PoseUtil or None:
        detector = None

        if idx == 0:
            detector = hand.HandUtil(min_detection_confidence = thresh)
        elif idx == 1:
            detector = pose.PoseUtil()
        elif idx == 2:
            detector = face.FaceUtil(min_detection_confidence = thresh)

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

    def get_train_file_list(self) -> list:
        file_list = []
        count = self.train_dataset_list.count()
        for idx in range(count):
            file = self.train_dataset_list.item(idx)
            file_list.append(file.text())

        return file_list

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

    def detect_draw(self, detector, img : np.ndarray, target_label : QLabel) -> None:
        result = detector.detect(img)
        scores = result.scores()
        if scores is None:
            self.log(f"찾은 오브젝트가 없습니다")
        else:
            self.log(f"찾은 개수 : {len(scores)} ({scores})")

        result.draw(img)
        qImg = self.ndarray_to_qimage(img)
        self.draw_label(target_label, qImg)

    def detect_test_draw(self, img : np.ndarray, font_scale : int  = 3, thickness : int = 10) -> tuple:
        data_list = self.test_detector.extract(img)
        
        name, proba = None, None
        if data_list is not None:
            for idx, data in enumerate(data_list):
                name, proba = self.test_trainer.predict([data[-1]])
                box = data[0]

                if name in self.color_dict:
                    color = self.color_dict[name]
                else:
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    self.color_dict[name] = color


                cv2.putText(img, f"{name} : {proba:.2f}", (box[0], box[1] - 25)
                            , cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)
                cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3])
                                , color, thickness)
        
        return (img, (name, proba))

    def tools_add_img_list(self, img):
        tools_img_dict_len = len(self.tools_img_dict)
        tools_img_name = f"image_{tools_img_dict_len}"
        self.tools_img_dict[tools_img_name] = img
        self.tools_img_list.addItem(tools_img_name)

    @Slot()
    def train_dataset_add_end_signal_handler(self):
        self.train_dataset_list.setDisabled(False)
        self.train_dataset_add_thread = None

    @Slot()
    def test_dataset_add_end_signal_handler(self):
        self.test_dataset_list.setDisabled(False)
        self.test_dataset_add_thread = None

    @Slot()
    def train_type_combo_chnaged_handler(self, idx : int) -> None:
        print("훈련 타입 변경")
        min_thresh = self.train_thresh_spin_edit.text()
        min_thresh = float(min_thresh) / 100
        self.train_detector = self.init_detector(idx, min_thresh)
        self.log("훈련 타입 변경", (0, 255, 0))

    @staticmethod
    def train_thread_func(args : tuple) -> None:
        detector, trainer, dataset_list, log_signal, done_signal, exit_event = args

        def train_logger(log_message : str, color : tuple) -> None:
            log_signal.sig.emit(log_message, color)

        detector.set_logger(train_logger)
        data = detector.extract_dataset(dataset_list, exit_event)
        train_data, name = data["data"], data["name"]
        if len(train_data) == 0 or len(name) == 0:
            train_logger("데이터셋에서 학습할 수 있는 특징이 없습니다.", (255, 0, 0))
            done_signal.sig.emit()
            return

        trainer.train_svm(train_data, name)
        done_signal.sig.emit()

    @Slot()
    def train_model_train_button_clicked_handler(self):
        print("훈련 모델 버튼 클릭")
        if self.train_thread is None:
            self.train_thread = WorkThread(WorkQThread, self.train_thread_func
                                                        , (self.train_detector, self.train_trainer
                                                        , self.get_train_file_list(), self.log_signal
                                                        , self.train_done_signal)
                                                        , self)

            self.train_dataset_list.setDisabled(True)
            self.train_thresh_apply_button.setDisabled(True)
            self.train_thread.start()
            self.train_model_train_button.setText("학습중")
        else:
            self.train_thread.exit()
            self.train_thread.join()
            self.train_thread = None
            self.train_model_train_button.setText("모델 학습 시작")
            self.train_dataset_list.setDisabled(False)
            self.train_thresh_apply_button.setDisabled(False)

    @Slot()
    def test_cam_signal_handler(self, code : int, img : np.ndarray):
        qImg = self.ndarray_to_qimage(img)

        target_label = self.test_original_img_label if code == self.test_cam_signal.ORIGINAL else self.test_result_img_label
        self.draw_label(target_label, qImg)

    @Slot()
    def tools_cam_signal_handler(self, code : int, img : np.ndarray):
        qImg = self.ndarray_to_qimage(img)
        self.tools_add_img_list(img)

        target_label = self.tools_original_img_label if code == self.tools_cam_signal.ORIGINAL else self.tools_result_img_label
        self.draw_label(target_label, qImg)

    @Slot()
    def tools_cam_done_signal_handler(self):
        self.tools_cam_thread.exit()
        self.tools_cam_thread.join()
        self.tools_cam_thread = None

        self.tools_capture_button.setDisabled(False)
        self.tools_video_button.setText("촬영 시작")

    def main_menu_tab_changed_hander(self, idx):
        if idx == 2:
            self.tools_cap = cv2.VideoCapture(0)
            if self.tools_cap.isOpened() == False:
                self.tools_cap.release()
                self.tools_cap = None
                self.log("카메라를 열 수 없습니다.", (255, 0, 0))
                return
        else:
            if self.tools_cap is not None:
                self.tools_cap.release()
                self.tools_cap = None

    @Slot()
    def train_model_save_button_clicked_handler(self):
        print("훈련 모델 저장 버튼")
        folder_path = self.get_folder_paths()
        if folder_path:
            self.train_trainer.save_svm(folder_path[0])
            self.log(f"{folder_path[0]}에 모델을 저장했습니다.", (0, 255, 0))

    @staticmethod
    def file_add_thread_func(args : tuple) -> None:
        folder_path, target_list, end_signal, exit_event = args

        file_list = get_file_list(folder_path)
        for file in file_list:
            item = QListWidgetItem(file)
            target_list.addItem(item)

        end_signal.sig.emit()

    @Slot()
    def train_dataset_path_find_button_clicked_handler(self):
        print("훈련 데이터셋 찾기 버튼")
        folder_paths = self.get_folder_paths()
        if folder_paths is None:
            return

        self.train_dataset_list.clear()
        self.train_dataset_list.setDisabled(True)
        self.train_file_add_thread = WorkThread(WorkQThread, self.file_add_thread_func
                                                , (folder_paths[0], self.train_dataset_list, self.train_dataset_add_end_signal)
                                                , self)
        self.train_file_add_thread.start()

    @Slot()
    def train_dataset_list_itemSelectionChanged_handler(self) -> None:
        print("훈련 데이터셋 선택 아이템 체인지")
        file_path = self.train_dataset_list.currentItem().text()
        img = cv2_imread(file_path)
        if img is None:
            return

        qImg = self.ndarray_to_qimage(img)
        self.draw_label(self.train_original_img_label, qImg)

        self.detect_draw(self.train_detector, img, self.train_result_img_label)

    
    @Slot()
    def train_thresh_apply_button_clicked_handler(self):
        print("훈련 데이터셋 임계율 설정 버튼")
        min_thresh = self.train_thresh_spin_edit.text()
        min_thresh = float(min_thresh) / 100
        idx = self.train_type_combo.currentIndex()
        self.train_detector = self.init_detector(idx, min_thresh)
        self.log("설정 완료!", (0, 255, 0))

    @Slot()
    def test_type_combo_chnaged_handler(self, idx : int) -> None:
        print("테스트 타입 변경")
        min_thresh = self.test_thresh_spin_edit.text()
        min_thresh = float(min_thresh) / 100
        self.test_detector = self.init_detector(idx, min_thresh)
        self.log("테스트 타입 변경", (0, 255, 0))

    @Slot()
    def test_model_load_button_handler(self) -> None:
        folder_paths = self.get_folder_paths()
        if folder_paths is None:
            return

        self.test_trainer.load_svm(folder_paths[0])
        self.test_target_label_combo.clear()
        self.test_target_label_combo.addItems(self.test_trainer.get_labels())
        self.log(f"{folder_paths[0]}의 모델을 불러왔습니다", (0, 255, 0))

    @Slot()
    def test_dataset_path_find_button_handler(self) -> None:
        folder_paths = self.get_folder_paths()
        if folder_paths is None:
            return

        self.test_dataset_list.clear()
        self.test_dataset_list.setDisabled(True)
        self.test_file_add_thread = WorkThread(WorkQThread, self.file_add_thread_func
                                                            ,(folder_paths[0], self.test_dataset_list, self.test_dataset_add_end_signal)
                                                            , self)
        self.test_file_add_thread.start()

    @staticmethod
    def cam_thread_func(args : tuple):
        detect_test_draw, target_combo, log_signal, cam_signal, exit_event = args

        def test_cam_logger(log_message : str, color : tuple) -> None:
            log_signal.sig.emit(log_message, color)

        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            if exit_event.is_set():
                break

            ret, frame = cap.read()
            if ret == False:
                continue
            
            frame = cv2.flip(frame, 1)
            cam_signal.sig.emit(cam_signal.ORIGINAL, frame.copy())
            frame, result = detect_test_draw(frame, 1, 3)
            name, proba = result
            target_label = target_combo.currentText()
            if name is not None and name == target_label:
                cv2.putText(frame, "O", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 5)
            else:
                cv2.putText(frame, "X", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 5)

            cam_signal.sig.emit(cam_signal.RESULT, frame)

        cap.release()

    @Slot()
    def test_cam_use_check_handler(self, state):
        if state:
            self.test_use_cam = True
            self.test_cam_thread = WorkThread(WorkQThread, self.cam_thread_func
                                    , (self.detect_test_draw
                                    , self.test_target_label_combo,  self.log_signal
                                    , self.test_cam_signal), self)

            self.test_cam_thread.start()

        else:
            self.test_cam_thread.exit()
            self.test_cam_thread.join()
            self.test_cam_thread = None
            self.test_use_cam = False

        self.test_dataset_list.setDisabled(True if state else False)

    @Slot()
    def test_dataset_list_itemSelectionChanged_handler(self) -> None:
        print("테스트 데이터셋 선택 아이템 체인지")
        file_path = self.test_dataset_list.currentItem().text()
        img = cv2_imread(file_path)
        if img is None:
            return

        qImg = self.ndarray_to_qimage(img)
        self.draw_label(self.test_original_img_label, qImg)

        img, _ = self.detect_test_draw(img, 1, 3)
        qImg = self.ndarray_to_qimage(img)
        self.draw_label(self.test_result_img_label, qImg)

    @Slot()
    def test_thresh_apply_button_clicked_handler(self):
        print("테스트 임계율 설정 버튼")
        min_thresh = self.test_thresh_spin_edit.text()
        min_thresh = float(min_thresh) / 100
        idx = self.test_type_combo.currentIndex()
        self.test_detector = self.init_detector(idx, min_thresh)
        self.log("설정 완료!", (0, 255, 0))

    
    @Slot()
    def tools_thresh_apply_button_clicked_handler(self):
        print("도구 임계율 설정 버튼")
        min_thresh = self.test_thresh_spin_edit.text()
        min_thresh = float(min_thresh) / 100
        idx = self.tools_type_combo.currentIndex()
        self.tools_detector = self.init_detector(idx, min_thresh)
        self.log("설정 완료!", (0, 255, 0))

    @Slot()
    def tools_type_combo_chnaged_handler(self, idx):
        print("도구 타입 변경")
        min_thresh = self.tools_thresh_spin_edit.text()
        min_thresh = float(min_thresh) / 100
        self.tools_detector = self.init_detector(idx, min_thresh)
        self.log("도구 타입 변경", (0, 255, 0))

    @Slot()
    def tools_capture_button_handler(self):
        if self.tools_cap is None or self.tools_cap.isOpened() == False:
            self.log("카메라를 열 수 없습니다.", (255, 0, 0))
            return

        ret, frame = self.tools_cap.read()
        if ret == False:
            self.log("프레임을 얻을 수 없습니다. 잠시후 다시 시도해주세요", (255, 0, 0))
            return

        org_frame = frame.copy()
        self.draw_label(self.tools_original_img_label, self.ndarray_to_qimage(frame))
        
        self.detect_draw(self.tools_detector, frame, self.tools_result_img_label)
        self.tools_add_img_list(org_frame)

    @staticmethod
    def tools_video_capture_thread_func(args : tuple) -> None:
        cap, cam_signal, cature_time, done_signal, exit_event = args

        start_time = time.time()
        while cap.isOpened() and exit_event.is_set() == False:
            if time.time() - start_time > cature_time:
                break

            ret, frame = cap.read()
            if ret == False:
                continue

            cam_signal.sig.emit(cam_signal.ORIGINAL, frame.copy())
            time.sleep(0.2)

        done_signal.sig.emit()

    @Slot()
    def tools_video_button_handler(self):
        if self.tools_cam_thread is None:
            self.tools_capture_button.setDisabled(True)
            self.tools_cam_thread = WorkThread(WorkQThread, self.tools_video_capture_thread_func
                                                            , (self.tools_cap, self.tools_cam_signal, 10, self.tools_cam_done_signal))
            self.tools_cam_thread.start()
            self.tools_video_button.setText("촬영 중지")
        else:
            self.tools_cam_thread.exit()
            self.tools_cam_thread.join()
            self.tools_cam_thread = None

            self.tools_capture_button.setDisabled(False)
            self.tools_video_button.setText("촬영 시작")

    @Slot()
    def tools_save_path_find_button_handler(self):
        folder_paths = self.get_folder_paths()
        if folder_paths is None:
            return

        for name, img in self.tools_img_dict.items():
            name += ".png"
            img_path = os.path.join(folder_paths[0], name,)
            cv2_imwrite(img_path, img)


    @Slot()
    def tools_img_list_itemSelectionChanged_handler(self):
        if not self.tools_img_dict:
            return

        img_name = self.tools_img_list.currentItem().text()
        img = self.tools_img_dict[img_name].copy()
        
        qimg = self.ndarray_to_qimage(img)
        self.draw_label(self.tools_original_img_label, qimg)
        self.detect_draw(self.tools_detector, img, self.tools_result_img_label)

    @Slot()
    def tools_img_remove_button_handler(self):
        self.tools_img_dict.clear()
        self.tools_img_list.clear()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainTestUtilForm()
    window.show()
    app.exec()