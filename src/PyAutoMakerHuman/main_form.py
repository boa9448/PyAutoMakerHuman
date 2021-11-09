# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_form.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(1122, 745)
        self.main_menu_tab = QTabWidget(Form)
        self.main_menu_tab.setObjectName(u"main_menu_tab")
        self.main_menu_tab.setGeometry(QRect(10, 10, 1101, 471))
        self.train_tab = QWidget()
        self.train_tab.setObjectName(u"train_tab")
        self.groupBox = QGroupBox(self.train_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 0, 401, 431))
        self.verticalLayoutWidget_2 = QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(9, 19, 381, 401))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.train_original_img_label = QLabel(self.verticalLayoutWidget_2)
        self.train_original_img_label.setObjectName(u"train_original_img_label")

        self.verticalLayout_3.addWidget(self.train_original_img_label)

        self.groupBox_2 = QGroupBox(self.train_tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(420, 0, 401, 431))
        self.verticalLayoutWidget_3 = QWidget(self.groupBox_2)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(9, 19, 381, 401))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.train_result_img_label = QLabel(self.verticalLayoutWidget_3)
        self.train_result_img_label.setObjectName(u"train_result_img_label")

        self.verticalLayout_4.addWidget(self.train_result_img_label)

        self.groupBox_3 = QGroupBox(self.train_tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(830, 0, 261, 431))
        self.verticalLayoutWidget = QWidget(self.groupBox_3)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 246, 401))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.train_type_combo = QComboBox(self.verticalLayoutWidget)
        self.train_type_combo.setObjectName(u"train_type_combo")
        self.train_type_combo.setEditable(False)

        self.horizontalLayout_3.addWidget(self.train_type_combo)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.train_thresh_spin_edit = QDoubleSpinBox(self.verticalLayoutWidget)
        self.train_thresh_spin_edit.setObjectName(u"train_thresh_spin_edit")
        self.train_thresh_spin_edit.setEnabled(True)
        self.train_thresh_spin_edit.setDecimals(3)

        self.horizontalLayout_4.addWidget(self.train_thresh_spin_edit)

        self.train_thresh_apply_button = QPushButton(self.verticalLayoutWidget)
        self.train_thresh_apply_button.setObjectName(u"train_thresh_apply_button")

        self.horizontalLayout_4.addWidget(self.train_thresh_apply_button)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.train_model_train_button = QPushButton(self.verticalLayoutWidget)
        self.train_model_train_button.setObjectName(u"train_model_train_button")

        self.verticalLayout.addWidget(self.train_model_train_button)

        self.train_model_save_button = QPushButton(self.verticalLayoutWidget)
        self.train_model_save_button.setObjectName(u"train_model_save_button")

        self.verticalLayout.addWidget(self.train_model_save_button)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.train_dataset_path_find_button = QPushButton(self.verticalLayoutWidget)
        self.train_dataset_path_find_button.setObjectName(u"train_dataset_path_find_button")

        self.horizontalLayout.addWidget(self.train_dataset_path_find_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.train_dataset_list = QListWidget(self.verticalLayoutWidget)
        self.train_dataset_list.setObjectName(u"train_dataset_list")

        self.verticalLayout.addWidget(self.train_dataset_list)

        self.train_two_hand_checkBox = QCheckBox(self.verticalLayoutWidget)
        self.train_two_hand_checkBox.setObjectName(u"train_two_hand_checkBox")

        self.verticalLayout.addWidget(self.train_two_hand_checkBox)

        self.main_menu_tab.addTab(self.train_tab, "")
        self.test_tab = QWidget()
        self.test_tab.setObjectName(u"test_tab")
        self.groupBox_5 = QGroupBox(self.test_tab)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(10, 0, 401, 431))
        self.verticalLayoutWidget_4 = QWidget(self.groupBox_5)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(9, 19, 381, 401))
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.test_original_img_label = QLabel(self.verticalLayoutWidget_4)
        self.test_original_img_label.setObjectName(u"test_original_img_label")

        self.verticalLayout_5.addWidget(self.test_original_img_label)

        self.groupBox_6 = QGroupBox(self.test_tab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(420, 0, 401, 431))
        self.verticalLayoutWidget_6 = QWidget(self.groupBox_6)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(9, 19, 381, 401))
        self.verticalLayout_8 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.test_result_img_label = QLabel(self.verticalLayoutWidget_6)
        self.test_result_img_label.setObjectName(u"test_result_img_label")

        self.verticalLayout_8.addWidget(self.test_result_img_label)

        self.groupBox_7 = QGroupBox(self.test_tab)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(830, 0, 261, 431))
        self.verticalLayoutWidget_9 = QWidget(self.groupBox_7)
        self.verticalLayoutWidget_9.setObjectName(u"verticalLayoutWidget_9")
        self.verticalLayoutWidget_9.setGeometry(QRect(10, 20, 246, 401))
        self.verticalLayout_11 = QVBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.verticalLayoutWidget_9)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.test_type_combo = QComboBox(self.verticalLayoutWidget_9)
        self.test_type_combo.setObjectName(u"test_type_combo")
        self.test_type_combo.setEditable(False)

        self.horizontalLayout_5.addWidget(self.test_type_combo)


        self.verticalLayout_11.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.verticalLayoutWidget_9)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.label_6)

        self.test_thresh_spin_edit = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.test_thresh_spin_edit.setObjectName(u"test_thresh_spin_edit")
        self.test_thresh_spin_edit.setEnabled(True)
        self.test_thresh_spin_edit.setDecimals(3)

        self.horizontalLayout_6.addWidget(self.test_thresh_spin_edit)

        self.test_thresh_apply_button = QPushButton(self.verticalLayoutWidget_9)
        self.test_thresh_apply_button.setObjectName(u"test_thresh_apply_button")

        self.horizontalLayout_6.addWidget(self.test_thresh_apply_button)


        self.verticalLayout_11.addLayout(self.horizontalLayout_6)

        self.test_model_load_button = QPushButton(self.verticalLayoutWidget_9)
        self.test_model_load_button.setObjectName(u"test_model_load_button")

        self.verticalLayout_11.addWidget(self.test_model_load_button)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(self.verticalLayoutWidget_9)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.test_dataset_path_find_button = QPushButton(self.verticalLayoutWidget_9)
        self.test_dataset_path_find_button.setObjectName(u"test_dataset_path_find_button")

        self.horizontalLayout_2.addWidget(self.test_dataset_path_find_button)


        self.verticalLayout_11.addLayout(self.horizontalLayout_2)

        self.test_cam_use_check = QCheckBox(self.verticalLayoutWidget_9)
        self.test_cam_use_check.setObjectName(u"test_cam_use_check")

        self.verticalLayout_11.addWidget(self.test_cam_use_check)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_10 = QLabel(self.verticalLayoutWidget_9)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)

        self.horizontalLayout_11.addWidget(self.label_10)

        self.test_target_label_combo = QComboBox(self.verticalLayoutWidget_9)
        self.test_target_label_combo.setObjectName(u"test_target_label_combo")
        self.test_target_label_combo.setEditable(False)

        self.horizontalLayout_11.addWidget(self.test_target_label_combo)


        self.verticalLayout_11.addLayout(self.horizontalLayout_11)

        self.test_dataset_list = QListWidget(self.verticalLayoutWidget_9)
        self.test_dataset_list.setObjectName(u"test_dataset_list")

        self.verticalLayout_11.addWidget(self.test_dataset_list)

        self.main_menu_tab.addTab(self.test_tab, "")
        self.tools_tab = QWidget()
        self.tools_tab.setObjectName(u"tools_tab")
        self.groupBox_8 = QGroupBox(self.tools_tab)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(10, 0, 401, 431))
        self.verticalLayoutWidget_7 = QWidget(self.groupBox_8)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(9, 19, 381, 401))
        self.verticalLayout_9 = QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.tools_original_img_label = QLabel(self.verticalLayoutWidget_7)
        self.tools_original_img_label.setObjectName(u"tools_original_img_label")

        self.verticalLayout_9.addWidget(self.tools_original_img_label)

        self.groupBox_9 = QGroupBox(self.tools_tab)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setGeometry(QRect(420, 0, 401, 431))
        self.verticalLayoutWidget_8 = QWidget(self.groupBox_9)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(9, 19, 381, 401))
        self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.tools_result_img_label = QLabel(self.verticalLayoutWidget_8)
        self.tools_result_img_label.setObjectName(u"tools_result_img_label")

        self.verticalLayout_10.addWidget(self.tools_result_img_label)

        self.groupBox_10 = QGroupBox(self.tools_tab)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setGeometry(QRect(830, 0, 261, 431))
        self.verticalLayoutWidget_10 = QWidget(self.groupBox_10)
        self.verticalLayoutWidget_10.setObjectName(u"verticalLayoutWidget_10")
        self.verticalLayoutWidget_10.setGeometry(QRect(10, 20, 246, 401))
        self.verticalLayout_14 = QVBoxLayout(self.verticalLayoutWidget_10)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_7 = QLabel(self.verticalLayoutWidget_10)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.label_7)

        self.tools_type_combo = QComboBox(self.verticalLayoutWidget_10)
        self.tools_type_combo.setObjectName(u"tools_type_combo")
        self.tools_type_combo.setEditable(False)

        self.horizontalLayout_8.addWidget(self.tools_type_combo)


        self.verticalLayout_14.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_9 = QLabel(self.verticalLayoutWidget_10)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)

        self.horizontalLayout_12.addWidget(self.label_9)

        self.tools_thresh_spin_edit = QDoubleSpinBox(self.verticalLayoutWidget_10)
        self.tools_thresh_spin_edit.setObjectName(u"tools_thresh_spin_edit")
        self.tools_thresh_spin_edit.setEnabled(True)
        self.tools_thresh_spin_edit.setDecimals(3)

        self.horizontalLayout_12.addWidget(self.tools_thresh_spin_edit)

        self.tools_thresh_apply_button = QPushButton(self.verticalLayoutWidget_10)
        self.tools_thresh_apply_button.setObjectName(u"tools_thresh_apply_button")

        self.horizontalLayout_12.addWidget(self.tools_thresh_apply_button)


        self.verticalLayout_14.addLayout(self.horizontalLayout_12)

        self.tools_capture_button = QPushButton(self.verticalLayoutWidget_10)
        self.tools_capture_button.setObjectName(u"tools_capture_button")

        self.verticalLayout_14.addWidget(self.tools_capture_button)

        self.tools_video_button = QPushButton(self.verticalLayoutWidget_10)
        self.tools_video_button.setObjectName(u"tools_video_button")

        self.verticalLayout_14.addWidget(self.tools_video_button)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_8 = QLabel(self.verticalLayoutWidget_10)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_9.addWidget(self.label_8)

        self.tools_save_path_find_button = QPushButton(self.verticalLayoutWidget_10)
        self.tools_save_path_find_button.setObjectName(u"tools_save_path_find_button")

        self.horizontalLayout_9.addWidget(self.tools_save_path_find_button)


        self.verticalLayout_14.addLayout(self.horizontalLayout_9)

        self.tools_img_list = QListWidget(self.verticalLayoutWidget_10)
        self.tools_img_list.setObjectName(u"tools_img_list")

        self.verticalLayout_14.addWidget(self.tools_img_list)

        self.tools_img_remove_button = QPushButton(self.verticalLayoutWidget_10)
        self.tools_img_remove_button.setObjectName(u"tools_img_remove_button")

        self.verticalLayout_14.addWidget(self.tools_img_remove_button)

        self.main_menu_tab.addTab(self.tools_tab, "")
        self.groupBox_4 = QGroupBox(Form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 480, 1101, 261))
        self.verticalLayoutWidget_5 = QWidget(self.groupBox_4)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 20, 1071, 231))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.main_log_list = QListWidget(self.verticalLayoutWidget_5)
        self.main_log_list.setObjectName(u"main_log_list")

        self.verticalLayout_2.addWidget(self.main_log_list)


        self.retranslateUi(Form)

        self.main_menu_tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\ub3c4\uc6b0\ubbf8 \uc720\ud2f8", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\uc6d0\ubcf8", None))
        self.train_original_img_label.setText(QCoreApplication.translate("Form", u"\uc6d0\ubcf8 \uc774\ubbf8\uc9c0", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\ub79c\ub4dc\ub9c8\ud06c \uc774\ubbf8\uc9c0", None))
        self.train_result_img_label.setText(QCoreApplication.translate("Form", u"\ub79c\ub4dc\ub9c8\ud06c \uc774\ubbf8\uc9c0", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\ubaa8\ub378 \ud559\uc2b5", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\ubaa8\ub378 \ud0c0\uc785 :   ", None))
#if QT_CONFIG(accessibility)
        self.train_type_combo.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.train_type_combo.setPlaceholderText("")
        self.label_3.setText(QCoreApplication.translate("Form", u"\ud0d0\uc9c0 \uc784\uacc4\uc728(%) : ", None))
        self.train_thresh_spin_edit.setSpecialValueText(QCoreApplication.translate("Form", u"70.0", None))
        self.train_thresh_apply_button.setText(QCoreApplication.translate("Form", u"\uc801\uc6a9", None))
        self.train_model_train_button.setText(QCoreApplication.translate("Form", u"\ubaa8\ub378 \ud559\uc2b5 \uc2dc\uc791", None))
        self.train_model_save_button.setText(QCoreApplication.translate("Form", u"\ubaa8\ub378 \uc800\uc7a5\ud558\uae30", None))
        self.label.setText(QCoreApplication.translate("Form", u"\ub370\uc774\ud130\uc14b \ud3f4\ub354 \uc5f4\uae30 : ", None))
        self.train_dataset_path_find_button.setText(QCoreApplication.translate("Form", u"\ucc3e\uc544\ubcf4\uae30", None))
        self.train_two_hand_checkBox.setText(QCoreApplication.translate("Form", u"2\uac1c\uc758 \uc190\uc744 \ud559\uc2b5 \uc2dc\ud0a4\ub3c4\ub85d \uace0\uc815", None))
        self.main_menu_tab.setTabText(self.main_menu_tab.indexOf(self.train_tab), QCoreApplication.translate("Form", u"\ubaa8\ub378 \ud559\uc2b5", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"\uc6d0\ubcf8", None))
        self.test_original_img_label.setText(QCoreApplication.translate("Form", u"\uc6d0\ubcf8 \uc774\ubbf8\uc9c0", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"\ud14c\uc2a4\ud2b8 \uacb0\uacfc \uc774\ubbf8\uc9c0", None))
        self.test_result_img_label.setText(QCoreApplication.translate("Form", u"\ud14c\uc2a4\ud2b8 \uacb0\uacfc \uc774\ubbf8\uc9c0", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Form", u"\ub3c4\uad6c", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\ubaa8\ub378 \ud0c0\uc785 :   ", None))
#if QT_CONFIG(accessibility)
        self.test_type_combo.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.test_type_combo.setPlaceholderText("")
        self.label_6.setText(QCoreApplication.translate("Form", u"\ud0d0\uc9c0 \uc784\uacc4\uc728(%) : ", None))
        self.test_thresh_spin_edit.setSpecialValueText(QCoreApplication.translate("Form", u"70.0", None))
        self.test_thresh_apply_button.setText(QCoreApplication.translate("Form", u"\uc801\uc6a9", None))
        self.test_model_load_button.setText(QCoreApplication.translate("Form", u"\ubaa8\ub378 \ubd88\ub7ec\uc624\uae30", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\ud14c\uc2a4\ud2b8\uc14b \ud3f4\ub354 \uc5f4\uae30 : ", None))
        self.test_dataset_path_find_button.setText(QCoreApplication.translate("Form", u"\ucc3e\uc544\ubcf4\uae30", None))
        self.test_cam_use_check.setText(QCoreApplication.translate("Form", u"\uc6f9\ucea0\uc744 \uc774\uc6a9\ud574\uc11c \ud14c\uc2a4\ud2b8", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\ub300\uc0c1 \ub77c\ubca8 :   ", None))
#if QT_CONFIG(accessibility)
        self.test_target_label_combo.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.test_target_label_combo.setPlaceholderText("")
        self.main_menu_tab.setTabText(self.main_menu_tab.indexOf(self.test_tab), QCoreApplication.translate("Form", u"\ubaa8\ub378 \ud14c\uc2a4\ud2b8", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Form", u"\uc6d0\ubcf8", None))
        self.tools_original_img_label.setText(QCoreApplication.translate("Form", u"\uc6d0\ubcf8 \uc774\ubbf8\uc9c0", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Form", u"\ub79c\ub4dc\ub9c8\ud06c \uc774\ubbf8\uc9c0", None))
        self.tools_result_img_label.setText(QCoreApplication.translate("Form", u"\ub79c\ub4dc\ub9c8\ud06c \uc774\ubbf8\uc9c0", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Form", u"\ub3c4\uad6c", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\ubaa8\ub378 \ud0c0\uc785 :   ", None))
#if QT_CONFIG(accessibility)
        self.tools_type_combo.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.tools_type_combo.setPlaceholderText("")
        self.label_9.setText(QCoreApplication.translate("Form", u"\ud0d0\uc9c0 \uc784\uacc4\uc728(%) : ", None))
        self.tools_thresh_spin_edit.setSpecialValueText(QCoreApplication.translate("Form", u"70.0", None))
        self.tools_thresh_apply_button.setText(QCoreApplication.translate("Form", u"\uc801\uc6a9", None))
        self.tools_capture_button.setText(QCoreApplication.translate("Form", u"\ucea1\uccd0", None))
        self.tools_video_button.setText(QCoreApplication.translate("Form", u"\ucd2c\uc601 \uc2dc\uc791", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\uc774\ubbf8\uc9c0 \uc800\uc7a5 \uc704\uce58 : ", None))
        self.tools_save_path_find_button.setText(QCoreApplication.translate("Form", u"\ucc3e\uc544\ubcf4\uae30", None))
        self.tools_img_remove_button.setText(QCoreApplication.translate("Form", u"\uc774\ubbf8\uc9c0 \uc0ad\uc81c", None))
        self.main_menu_tab.setTabText(self.main_menu_tab.indexOf(self.tools_tab), QCoreApplication.translate("Form", u"\ub3c4\uad6c", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"\uc791\uc5c5 \ub85c\uadf8", None))
    # retranslateUi

