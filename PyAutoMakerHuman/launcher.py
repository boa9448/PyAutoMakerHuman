import os
import sys
import time
import random
from threading import Thread, Event
from glob import glob

import cv2
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from main_form import Ui_Form
import face
import hand
import pose
import train

class LogSignal(QObject):
    sig = Signal(str, tuple)

    def __init__(self):
        super().__init__()

class TrainExitSignal(QObject):
    sig = Signal()

    def __init__(self):
        super().__init__()

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
        self.log_signal = LogSignal()
        self.train_exit_signal = TrainExitSignal()
        self.train_exit_event = Event()
        self.bTraining = False
        self.color_dict = {}

        super(TrainTestUtilForm, self).__init__()
        self.setupUi(self)

        self.tab_list = [(self.train_tab, self.train_log_list), (self.test_tab, self.test_log_list), self.tools_tab]

        def init_display():
            self.two_hand_checkBox.hide()

            for train_test_type in self.TRAIN_TEST_TYPE_LIST:
                self.train_type_combo.addItem(train_test_type)
                self.test_type_combo.addItem(train_test_type)
        init_display()

        def init_handler():
            self.log_signal.sig.connect(self.log)
            self.train_exit_signal.sig.connect(self.tarin_exit_signal_handler)

            self.main_menu_tab.currentChanged.connect(lambda x : print(x, " call!"))
            self.train_type_combo.currentIndexChanged.connect(self.train_test_type_combo_change_handler)
            self.test_type_combo.currentIndexChanged.connect(self.test_test_type_combo_change_handler)
            self.train_model_train_button.clicked.connect(self.train_model_train_button_handler)
            self.train_model_save_button.clicked.connect(self.train_model_save_button_handler)
            self.test_model_load_button.clicked.connect(self.test_model_load_button_handler)
            self.train_dataset_path_find_button.clicked.connect(self.train_dataset_path_find_button_handler)
            self.test_dataset_path_find_button.clicked.connect(self.test_dataset_path_find_button_handler)
            self.train_dataset_list.itemSelectionChanged.connect(self.train_dataset_list_select_change_handler)
            self.test_dataset_list.itemSelectionChanged.connect(self.test_dataset_list_select_change_handler)
            self.train_thresh_apply_button.clicked.connect(self.train_thresh_button_click_handler)
        init_handler()

        def init_data():
            thresh = self.train_thresh_spin_edit.text()
            thresh = float(thresh) / 100

            cur_type = self.train_type_combo.currentText()
            self.detector = self.init_detector(cur_type, thresh)
            self.trainer = train.SvmUtil()
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

        if detector is not None:
            detector.set_logger(self.log)
            
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
        target_log_idx = self.main_menu_tab.currentIndex()
        target_log_list = self.tab_list[target_log_idx][-1]
        target_log_list.addItem(log_message_item)
        target_log_list.scrollToBottom()

    def add_dataset_to_list(self, target_list, dataset_folder_path):
        print(os.path.join(dataset_folder_path, "**", "*.*"))
        dataset_file_list = glob(os.path.join(dataset_folder_path, "**", "*.*"), recursive = True)
        target_list.addItems(dataset_file_list)
        
        self.log(f"지정한 경로에서 총 : {len(dataset_file_list)}개의 파일을 찾았습니다")

    def view_original_img(self, target_img_label, img_path):
        pixmap = QPixmap()
        pixmap.load(img_path)
        if pixmap.isNull():
            self.messagebox("이미지를 열 수 없습니다.")
            self.log("이미지를 열 수 없습니다", (255, 0, 0))
            raise Exception("이미지를 열 수 없습니다")

        label_size = target_img_label.size()
        pixmap = pixmap.scaled(label_size, aspectMode = Qt.IgnoreAspectRatio)
        target_img_label.setPixmap(pixmap)

    def detect_draw(self, img_path) -> QImage:
        img = cv2.imread(img_path)
        if img is None:
            self.messagebox("이미지를 열 수 없습니다.")
            raise Exception("이미지를 열 수 없습니다")

        result = self.detector.detect(img)
        scores = result.scores()
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
    
    def detect_test_draw(self, img_path, size) -> QImage:
        img = cv2.imread(img_path)
        if img is None:
            self.messagebox("이미지를 열 수 없습니다.")
            raise Exception("이미지를 열 수 없습니다")

        # img = cv2.resize(img, size)
        data_list = self.detector.extract(img)
        if data_list is None:
            self.log(f"찾은 오브젝트가 없습니다")
        else:
            pass
        
        if data_list is not None:
            for idx, data in enumerate(data_list):
                name, proba = self.trainer.predict([data[-1]])
                box = data[0]

                if name in self.color_dict:
                    color = self.color_dict[name]
                else:
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    self.color_dict[name] = color


                cv2.putText(img, f"{name} : {proba:.2f}", (box[0], box[1] - 25)
                            , cv2.FONT_HERSHEY_SIMPLEX, 3, color, 10, cv2.LINE_AA)
                cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3])
                                , color, 10)

        height, width, channel = img.shape
        bytesPerLine = channel * width
        qImg = QImage(img.data, width, height, bytesPerLine
                        , QImage.Format_BGR888 if channel == 3 else QImage.Format_BGR30)
        return qImg

    def view_landmark_img(self, target_img_label, img_path):
        try:
            qImg = self.detect_draw(img_path)
            pixmap = QPixmap(qImg)
            label_size = target_img_label.size()
            pixmap = pixmap.scaled(label_size, aspectMode= Qt.IgnoreAspectRatio)
            target_img_label.setPixmap(pixmap)
        except:
            self.log("이미지를 열 수 없습니다.", (255, 0, 0))

    def view_test_img(self, target_img_label : QLabel, img_path):
        try:
            size = target_img_label.size()
            qImg = self.detect_test_draw(img_path, (size.width(), size.height()))
            pixmap = QPixmap(qImg)
            label_size = target_img_label.size()
            pixmap = pixmap.scaled(label_size, aspectMode= Qt.IgnoreAspectRatio)
            target_img_label.setPixmap(pixmap)
        except:
            self.log("이미지를 열 수 없습니다.", (255, 0, 0))

    @Slot()
    def train_dataset_list_select_change_handler(self):
        item = self.train_dataset_list.currentItem()
        try:
            self.log(f"{item.text()} 을(를) 열기를 시도합니다")
            self.view_original_img(self.train_original_img_label, item.text())
            self.view_landmark_img(self.train_result_img_label, item.text())
            self.log(f"{item.text()} 의 작업을 끝냈습니다")
        except Exception as e:
            print(e)
            self.log(f"{item.text()} 의 작업을 실패했습니다", (255, 0, 0))

    @Slot()
    def test_dataset_list_select_change_handler(self):
        item = self.test_dataset_list.currentItem()
        try:
            self.log(f"{item.text()} 을(를) 열기를 시도합니다")
            self.view_original_img(self.test_original_img_label, item.text())
            self.view_test_img(self.test_result_img_label, item.text())
            self.log(f"{item.text()} 의 작업을 끝냈습니다")
        except Exception as e:
            print(e)
            self.log(f"{item.text()} 의 작업을 실패했습니다", (255, 0, 0))

    @Slot()
    def train_thresh_button_click_handler(self):
        cur_text = self.train_type_combo.currentText()
        thresh = self.train_thresh_spin_edit.text()
        thresh = float(thresh) / 100
        self.detector = self.init_detector(cur_text, thresh)
        self.log("변경 완료")

    @Slot()
    def test_thresh_button_click_handler(self):
        cur_text = self.test_type_combo.currentText()
        thresh = self.train_thresh_spin_edit.text()
        thresh = float(75) / 100
        self.detector = self.init_detector(cur_text, thresh)
        self.log("변경 완료")

    @Slot()
    def train_test_type_combo_change_handler(self, idx):
        self.train_thresh_button_click_handler()

    @Slot()
    def test_test_type_combo_change_handler(self, idx):
        self.test_thresh_button_click_handler()

    @Slot()
    def tarin_exit_signal_handler(self):
        """
        self.bTraining = False
        self.train_exit_event.clear()
        self.train_model_train_button.setText("모델 학습 시작")
        """

        self.train_model_train_button_handler()

    @Slot()
    def train_model_train_button_handler(self):
        if self.bTraining == False:
            print("train_model_train_button call")
            dataset_folder = self.run_option.get_dataset_folder_path()
            if dataset_folder is None:
                self.log("데이터셋이 들어있는 폴더를 선택해주세요", (255, 0, 0))
                return

            def train_thread_func(detector, trainer, dataset_folder, log_signal, train_done_signal, exit_event):
                def train_log(log : str, color : tuple) -> None:
                    log_signal.sig.emit(log, color)

                detector.set_logger(train_log)
                data = detector.extract_dataset(dataset_folder, exit_event)
                train_data, name = data["data"], data["name"]
                if len(train_data) == 0 or len(name) == 0:
                    log_signal.sig.emit("데이터셋에서 학습할 수 있는 특징이 없습니다.", (255, 0, 0))
                    return

                trainer.train_svm(train_data, name)
                train_done_signal.sig.emit()

            self.train_thread = Thread(target=train_thread_func, args=(self.detector, self.trainer, dataset_folder
                                        , self.log_signal, self.train_exit_signal, self.train_exit_event))
            self.train_exit_event.clear()
            self.train_thread.start()
            self.train_model_train_button.setText("모델 학습 중지")
        else:
            self.train_exit_event.set()
            self.train_model_train_button.setText("중지하는 중...")
            self.train_thread.join()
            self.train_model_train_button.setText("모델 학습 시작")

        self.bTraining = not self.bTraining

    
    @Slot()
    def train_model_save_button_handler(self):
        print("train_model_save_button call")
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec():
            folder_path = dlg.selectedFiles()
            if folder_path:
                self.trainer.save_svm(folder_path[0])
                self.log(f"{folder_path[0]}에 모델을 저장했습니다.", (0, 255, 0))

    @Slot()
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

    @Slot()
    def test_model_load_button_handler(self):
        print("test_model_load_button_handler call")
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec():
            folder_path = dlg.selectedFiles()
            if folder_path:
                self.trainer.load_svm(folder_path[0])
                self.log(f"{folder_path[0]}의 모델을 불러왔습니다.", (0, 255, 0))

    @Slot()
    def test_dataset_path_find_button_handler(self):
        print("test_dataset_path_find_button_handler call")
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec():
            folder_path = dlg.selectedFiles()
            if folder_path:
                self.test_dataset_list.clear()
                self.add_dataset_to_list(self.test_dataset_list, folder_path[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainTestUtilForm()
    app.exec()