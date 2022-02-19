# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLayout, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(838, 633)
        self.gridLayout_2 = QGridLayout(Frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_2 = QLabel(Frame)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QSize(104, 22))
        self.label_2.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label = QLabel(Frame)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(0, 22))
        self.label.setMaximumSize(QSize(104, 22))
        self.label.setBaseSize(QSize(0, 0))
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.spinBox = QSpinBox(Frame)
        self.spinBox.setObjectName(u"spinBox")
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMaximumSize(QSize(104, 22))
        self.spinBox.setBaseSize(QSize(0, 0))
        self.spinBox.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.spinBox, 1, 0, 1, 1)

        self.label_3 = QLabel(Frame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMaximumSize(QSize(104, 22))
        self.label_3.setBaseSize(QSize(0, 0))
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.label_4 = QLabel(Frame)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(208, 0))
        self.label_4.setMaximumSize(QSize(208, 22))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setMargin(0)

        self.verticalLayout_2.addWidget(self.label_4)

        self.study_img_label = QLabel(Frame)
        self.study_img_label.setObjectName(u"study_img_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.study_img_label.sizePolicy().hasHeightForWidth())
        self.study_img_label.setSizePolicy(sizePolicy1)
        self.study_img_label.setMinimumSize(QSize(208, 208))
        self.study_img_label.setMaximumSize(QSize(208, 208))
        font1 = QFont()
        font1.setPointSize(30)
        self.study_img_label.setFont(font1)
        self.study_img_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.study_img_label)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_5 = QLabel(Frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_7 = QLabel(Frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_8 = QLabel(Frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_8, 1, 1, 1, 1)

        self.label_6 = QLabel(Frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_6, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 2, 1)

        self.verticalSpacer = QSpacerItem(20, 132, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.screen_img_label = QLabel(Frame)
        self.screen_img_label.setObjectName(u"screen_img_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.screen_img_label.sizePolicy().hasHeightForWidth())
        self.screen_img_label.setSizePolicy(sizePolicy2)
        self.screen_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.screen_img_label, 0, 0, 3, 1)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.label_2.setText(QCoreApplication.translate("Frame", u"\ub09c\uc774\ub3c4", None))
        self.label.setText(QCoreApplication.translate("Frame", u"\ub0a8\uc740\uc2dc\uac04", None))
        self.label_3.setText(QCoreApplication.translate("Frame", u"\u2606\u2606\u2606", None))
        self.label_4.setText(QCoreApplication.translate("Frame", u"\ub2e8\uc5b4", None))
        self.study_img_label.setText(QCoreApplication.translate("Frame", u"\ucf54\ub85c\ub098", None))
        self.label_5.setText(QCoreApplication.translate("Frame", u"O", None))
        self.label_7.setText(QCoreApplication.translate("Frame", u"5\uac1c", None))
        self.label_8.setText(QCoreApplication.translate("Frame", u"3\uac1c", None))
        self.label_6.setText(QCoreApplication.translate("Frame", u"X", None))
        self.screen_img_label.setText(QCoreApplication.translate("Frame", u"\uc601\uc0c1\uc774 \ubcf4\uc774\ub294 \uc601\uc5ed", None))
    # retranslateUi

