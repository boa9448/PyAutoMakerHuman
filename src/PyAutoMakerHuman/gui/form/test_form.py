# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_form.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLayout, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(838, 633)
        self.gridLayout_2 = QGridLayout(Frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 132, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 3, 2, 1)

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
        font.setPointSize(9)
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

        self.remaining_spin = QSpinBox(Frame)
        self.remaining_spin.setObjectName(u"remaining_spin")
        sizePolicy.setHeightForWidth(self.remaining_spin.sizePolicy().hasHeightForWidth())
        self.remaining_spin.setSizePolicy(sizePolicy)
        self.remaining_spin.setMaximumSize(QSize(104, 22))
        self.remaining_spin.setBaseSize(QSize(0, 0))
        self.remaining_spin.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.remaining_spin, 1, 0, 1, 1)

        self.level_img_label = QLabel(Frame)
        self.level_img_label.setObjectName(u"level_img_label")
        sizePolicy.setHeightForWidth(self.level_img_label.sizePolicy().hasHeightForWidth())
        self.level_img_label.setSizePolicy(sizePolicy)
        self.level_img_label.setMaximumSize(QSize(104, 22))
        self.level_img_label.setBaseSize(QSize(0, 0))
        self.level_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.level_img_label, 1, 1, 1, 1)


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

        self.question_img_label = QLabel(Frame)
        self.question_img_label.setObjectName(u"question_img_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.question_img_label.sizePolicy().hasHeightForWidth())
        self.question_img_label.setSizePolicy(sizePolicy1)
        self.question_img_label.setMinimumSize(QSize(208, 208))
        self.question_img_label.setMaximumSize(QSize(208, 208))
        self.question_img_label.setFont(font)
        self.question_img_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.question_img_label)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.success_img_label = QLabel(Frame)
        self.success_img_label.setObjectName(u"success_img_label")
        self.success_img_label.setFont(font)
        self.success_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.success_img_label, 0, 0, 1, 1)

        self.success_count_img_label = QLabel(Frame)
        self.success_count_img_label.setObjectName(u"success_count_img_label")
        self.success_count_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.success_count_img_label, 1, 0, 1, 1)

        self.fail_count_img_label = QLabel(Frame)
        self.fail_count_img_label.setObjectName(u"fail_count_img_label")
        self.fail_count_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.fail_count_img_label, 1, 1, 1, 1)

        self.fail_img_label = QLabel(Frame)
        self.fail_img_label.setObjectName(u"fail_img_label")
        self.fail_img_label.setFont(font)
        self.fail_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.fail_img_label, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 3, 2, 1)

        self.start_button = QPushButton(Frame)
        self.start_button.setObjectName(u"start_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy2)
        self.start_button.setMinimumSize(QSize(300, 50))
        self.start_button.setMaximumSize(QSize(300, 16777215))

        self.gridLayout_2.addWidget(self.start_button, 3, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 3, 2, 1, 1)

        self.screen_img_label = QLabel(Frame)
        self.screen_img_label.setObjectName(u"screen_img_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.screen_img_label.sizePolicy().hasHeightForWidth())
        self.screen_img_label.setSizePolicy(sizePolicy3)
        self.screen_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.screen_img_label, 0, 0, 3, 3)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.label_2.setText(QCoreApplication.translate("Frame", u"\ub09c\uc774\ub3c4", None))
        self.label.setText(QCoreApplication.translate("Frame", u"\ub0a8\uc740\uc2dc\uac04", None))
        self.level_img_label.setText(QCoreApplication.translate("Frame", u"\u2606\u2606\u2606", None))
        self.label_4.setText(QCoreApplication.translate("Frame", u"\ub2e8\uc5b4", None))
        self.question_img_label.setText(QCoreApplication.translate("Frame", u"\ucf54\ub85c\ub098", None))
        self.success_img_label.setText(QCoreApplication.translate("Frame", u"O", None))
        self.success_count_img_label.setText(QCoreApplication.translate("Frame", u"5\uac1c", None))
        self.fail_count_img_label.setText(QCoreApplication.translate("Frame", u"3\uac1c", None))
        self.fail_img_label.setText(QCoreApplication.translate("Frame", u"X", None))
        self.start_button.setText(QCoreApplication.translate("Frame", u"\uc2dc\uc791", None))
        self.screen_img_label.setText(QCoreApplication.translate("Frame", u"\uc601\uc0c1\uc774 \ubcf4\uc774\ub294 \uc601\uc5ed", None))
    # retranslateUi

