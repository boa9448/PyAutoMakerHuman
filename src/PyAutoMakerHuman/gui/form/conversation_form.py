# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'conversation_form.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTextEdit, QWidget)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(838, 646)
        self.gridLayout = QGridLayout(Frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(Frame)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(0, 80))

        self.horizontalLayout_2.addWidget(self.label)

        self.expectation_edit = QTextEdit(Frame)
        self.expectation_edit.setObjectName(u"expectation_edit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.expectation_edit.sizePolicy().hasHeightForWidth())
        self.expectation_edit.setSizePolicy(sizePolicy1)
        self.expectation_edit.setMinimumSize(QSize(0, 0))
        self.expectation_edit.setMaximumSize(QSize(16777215, 80))

        self.horizontalLayout_2.addWidget(self.expectation_edit)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.start_button = QPushButton(Frame)
        self.start_button.setObjectName(u"start_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy2)
        self.start_button.setMinimumSize(QSize(300, 50))
        self.start_button.setMaximumSize(QSize(300, 16777215))

        self.gridLayout.addWidget(self.start_button, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)

        self.screen_img_label = QLabel(Frame)
        self.screen_img_label.setObjectName(u"screen_img_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.screen_img_label.sizePolicy().hasHeightForWidth())
        self.screen_img_label.setSizePolicy(sizePolicy3)
        self.screen_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.screen_img_label, 0, 0, 1, 3)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.label.setText(QCoreApplication.translate("Frame", u"\uc608\uc0c1 \ubb38\uc790\uc5f4 : ", None))
        self.start_button.setText(QCoreApplication.translate("Frame", u"\uc2dc\uc791", None))
        self.screen_img_label.setText(QCoreApplication.translate("Frame", u"\uc601\uc0c1\uc774 \ubcf4\uc774\ub294 \uc601\uc5ed", None))
    # retranslateUi

