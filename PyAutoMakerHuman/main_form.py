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
        Form.resize(1122, 661)
        self.main_menu_tab = QTabWidget(Form)
        self.main_menu_tab.setObjectName(u"main_menu_tab")
        self.main_menu_tab.setGeometry(QRect(10, 10, 1101, 641))
        self.train_tab = QWidget()
        self.train_tab.setObjectName(u"train_tab")
        self.groupBox = QGroupBox(self.train_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 0, 391, 341))
        self.verticalLayoutWidget_2 = QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(9, 19, 371, 311))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.train_original_img_label = QLabel(self.verticalLayoutWidget_2)
        self.train_original_img_label.setObjectName(u"train_original_img_label")

        self.verticalLayout_3.addWidget(self.train_original_img_label)

        self.groupBox_2 = QGroupBox(self.train_tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(410, 0, 391, 341))
        self.verticalLayoutWidget_3 = QWidget(self.groupBox_2)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(9, 19, 371, 311))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.train_result_img_label = QLabel(self.verticalLayoutWidget_3)
        self.train_result_img_label.setObjectName(u"train_result_img_label")

        self.verticalLayout_4.addWidget(self.train_result_img_label)

        self.groupBox_3 = QGroupBox(self.train_tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(810, 0, 271, 601))
        self.verticalLayoutWidget = QWidget(self.groupBox_3)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 251, 571))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
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


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.train_model_train_button = QPushButton(self.verticalLayoutWidget)
        self.train_model_train_button.setObjectName(u"train_model_train_button")

        self.verticalLayout_6.addWidget(self.train_model_train_button)

        self.train_model_save_button = QPushButton(self.verticalLayoutWidget)
        self.train_model_save_button.setObjectName(u"train_model_save_button")

        self.verticalLayout_6.addWidget(self.train_model_save_button)


        self.verticalLayout.addLayout(self.verticalLayout_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.train_dataset_path_find_button = QPushButton(self.verticalLayoutWidget)
        self.train_dataset_path_find_button.setObjectName(u"train_dataset_path_find_button")

        self.horizontalLayout.addWidget(self.train_dataset_path_find_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.train_dataset_list = QListWidget(self.verticalLayoutWidget)
        self.train_dataset_list.setObjectName(u"train_dataset_list")

        self.verticalLayout_7.addWidget(self.train_dataset_list)


        self.verticalLayout.addLayout(self.verticalLayout_7)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.two_hand_checkBox = QCheckBox(self.verticalLayoutWidget)
        self.two_hand_checkBox.setObjectName(u"two_hand_checkBox")

        self.horizontalLayout_7.addWidget(self.two_hand_checkBox)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

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

        self.groupBox_4 = QGroupBox(self.train_tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 340, 791, 261))
        self.verticalLayoutWidget_5 = QWidget(self.groupBox_4)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 20, 771, 231))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.train_log_list = QListWidget(self.verticalLayoutWidget_5)
        self.train_log_list.setObjectName(u"train_log_list")

        self.verticalLayout_2.addWidget(self.train_log_list)

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
        self.groupBox_7.setGeometry(QRect(830, 0, 251, 601))
        self.verticalLayoutWidget_9 = QWidget(self.groupBox_7)
        self.verticalLayoutWidget_9.setObjectName(u"verticalLayoutWidget_9")
        self.verticalLayoutWidget_9.setGeometry(QRect(10, 20, 231, 571))
        self.verticalLayout_11 = QVBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
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


        self.verticalLayout_12.addLayout(self.horizontalLayout_5)

        self.test_model_load_button = QPushButton(self.verticalLayoutWidget_9)
        self.test_model_load_button.setObjectName(u"test_model_load_button")

        self.verticalLayout_12.addWidget(self.test_model_load_button)


        self.verticalLayout_11.addLayout(self.verticalLayout_12)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(self.verticalLayoutWidget_9)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.test_dataset_path_find_button = QPushButton(self.verticalLayoutWidget_9)
        self.test_dataset_path_find_button.setObjectName(u"test_dataset_path_find_button")

        self.horizontalLayout_2.addWidget(self.test_dataset_path_find_button)


        self.verticalLayout_11.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")

        self.verticalLayout_11.addLayout(self.horizontalLayout_8)

        self.test_cam_use_check = QCheckBox(self.verticalLayoutWidget_9)
        self.test_cam_use_check.setObjectName(u"test_cam_use_check")

        self.verticalLayout_11.addWidget(self.test_cam_use_check)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.test_dataset_list = QListWidget(self.verticalLayoutWidget_9)
        self.test_dataset_list.setObjectName(u"test_dataset_list")

        self.verticalLayout_13.addWidget(self.test_dataset_list)


        self.verticalLayout_11.addLayout(self.verticalLayout_13)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")

        self.verticalLayout_11.addLayout(self.horizontalLayout_6)

        self.groupBox_8 = QGroupBox(self.test_tab)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(10, 430, 811, 171))
        self.verticalLayoutWidget_8 = QWidget(self.groupBox_8)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(10, 20, 791, 141))
        self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.test_log_list = QListWidget(self.verticalLayoutWidget_8)
        self.test_log_list.setObjectName(u"test_log_list")

        self.verticalLayout_10.addWidget(self.test_log_list)

        self.main_menu_tab.addTab(self.test_tab, "")
        self.tools_tab = QWidget()
        self.tools_tab.setObjectName(u"tools_tab")
        self.main_menu_tab.addTab(self.tools_tab, "")

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
        self.label_2.setText(QCoreApplication.translate("Form", u"\ud0c0\uc785 :   ", None))
#if QT_CONFIG(accessibility)
        self.train_type_combo.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.train_type_combo.setPlaceholderText("")
        self.train_model_train_button.setText(QCoreApplication.translate("Form", u"\ubaa8\ub378 \ud559\uc2b5 \uc2dc\uc791", None))
        self.train_model_save_button.setText(QCoreApplication.translate("Form", u"\ubaa8\ub378 \uc800\uc7a5\ud558\uae30", None))
        self.label.setText(QCoreApplication.translate("Form", u"\ub370\uc774\ud130\uc14b \ud3f4\ub354 \uc5f4\uae30 : ", None))
        self.train_dataset_path_find_button.setText(QCoreApplication.translate("Form", u"\ucc3e\uc544\ubcf4\uae30", None))
        self.two_hand_checkBox.setText(QCoreApplication.translate("Form", u"2\uac1c\uc758 \uc190\uc744 \ud559\uc2b5 \uc2dc\ud0a4\ub3c4\ub85d \uace0\uc815", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\ud0d0\uc9c0 \uc784\uacc4\uc728(%) : ", None))
        self.train_thresh_spin_edit.setSpecialValueText(QCoreApplication.translate("Form", u"75.0", None))
        self.train_thresh_apply_button.setText(QCoreApplication.translate("Form", u"\uc801\uc6a9", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"\uc791\uc5c5 \ub85c\uadf8", None))
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
        self.test_model_load_button.setText(QCoreApplication.translate("Form", u"\ubaa8\ub378 \ubd88\ub7ec\uc624\uae30", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\ud14c\uc2a4\ud2b8\uc14b \ud3f4\ub354 \uc5f4\uae30 : ", None))
        self.test_dataset_path_find_button.setText(QCoreApplication.translate("Form", u"\ucc3e\uc544\ubcf4\uae30", None))
        self.test_cam_use_check.setText(QCoreApplication.translate("Form", u"\uc6f9\ucea0\uc744 \uc774\uc6a9\ud574\uc11c \ud14c\uc2a4\ud2b8", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Form", u"\uc791\uc5c5 \ub85c\uadf8", None))
        self.main_menu_tab.setTabText(self.main_menu_tab.indexOf(self.test_tab), QCoreApplication.translate("Form", u"\ubaa8\ub378 \ud14c\uc2a4\ud2b8", None))
        self.main_menu_tab.setTabText(self.main_menu_tab.indexOf(self.tools_tab), QCoreApplication.translate("Form", u"\ub3c4\uad6c", None))
    # retranslateUi

