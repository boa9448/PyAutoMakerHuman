# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera_form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(860, 515)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(72, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.camera_change_button = QPushButton(Dialog)
        self.camera_change_button.setObjectName(u"camera_change_button")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_change_button.sizePolicy().hasHeightForWidth())
        self.camera_change_button.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.camera_change_button, 1, 2, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 0, 2, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 4, 2, 1)

        self.side_camera_img_label = QLabel(Dialog)
        self.side_camera_img_label.setObjectName(u"side_camera_img_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.side_camera_img_label.sizePolicy().hasHeightForWidth())
        self.side_camera_img_label.setSizePolicy(sizePolicy2)
        self.side_camera_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.side_camera_img_label, 1, 3, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.front_camera_img_label = QLabel(Dialog)
        self.front_camera_img_label.setObjectName(u"front_camera_img_label")
        sizePolicy2.setHeightForWidth(self.front_camera_img_label.sizePolicy().hasHeightForWidth())
        self.front_camera_img_label.setSizePolicy(sizePolicy2)
        self.front_camera_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.front_camera_img_label, 1, 1, 1, 1)

        self.ok_button = QPushButton(Dialog)
        self.ok_button.setObjectName(u"ok_button")

        self.gridLayout.addWidget(self.ok_button, 2, 1, 1, 3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\uce74\uba54\ub77c \uc124\uc815", None))
        self.camera_change_button.setText(QCoreApplication.translate("Dialog", u"< - >", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\uce21\uba74 \uce74\uba54\ub77c", None))
        self.side_camera_img_label.setText(QCoreApplication.translate("Dialog", u"\uce21\uba74 \uce74\uba54\ub77c", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\uc815\uba74 \uce74\uba54\ub77c", None))
        self.front_camera_img_label.setText(QCoreApplication.translate("Dialog", u"\uc804\uba74 \uce74\uba54\ub77c", None))
        self.ok_button.setText(QCoreApplication.translate("Dialog", u"\ud655\uc778", None))
    # retranslateUi

