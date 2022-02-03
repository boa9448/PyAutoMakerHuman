# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_form.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(838, 632)
        self.gridLayout_2 = QGridLayout(Frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.direction_img_label = QLabel(Frame)
        self.direction_img_label.setObjectName(u"direction_img_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.direction_img_label.sizePolicy().hasHeightForWidth())
        self.direction_img_label.setSizePolicy(sizePolicy)
        self.direction_img_label.setMinimumSize(QSize(150, 100))
        self.direction_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.direction_img_label, 3, 1, 1, 1)

        self.shape_img_label = QLabel(Frame)
        self.shape_img_label.setObjectName(u"shape_img_label")
        sizePolicy.setHeightForWidth(self.shape_img_label.sizePolicy().hasHeightForWidth())
        self.shape_img_label.setSizePolicy(sizePolicy)
        self.shape_img_label.setMinimumSize(QSize(150, 100))
        self.shape_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.shape_img_label, 3, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 5, 2, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.study_select_label = QLabel(Frame)
        self.study_select_label.setObjectName(u"study_select_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.study_select_label.sizePolicy().hasHeightForWidth())
        self.study_select_label.setSizePolicy(sizePolicy1)
        self.study_select_label.setMinimumSize(QSize(0, 0))
        self.study_select_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.study_select_label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.char_child_combo = QComboBox(Frame)
        self.char_child_combo.setObjectName(u"char_child_combo")

        self.horizontalLayout_2.addWidget(self.char_child_combo)

        self.char_parent_combo = QComboBox(Frame)
        self.char_parent_combo.setObjectName(u"char_parent_combo")

        self.horizontalLayout_2.addWidget(self.char_parent_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.study_img_label = QLabel(Frame)
        self.study_img_label.setObjectName(u"study_img_label")
        self.study_img_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.study_img_label)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 5, 2, 1)

        self.horizontalSpacer_3 = QSpacerItem(349, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(351, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.screen_img_label = QLabel(Frame)
        self.screen_img_label.setObjectName(u"screen_img_label")
        self.screen_img_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.screen_img_label, 0, 0, 2, 3)

        self.direction_label = QLabel(Frame)
        self.direction_label.setObjectName(u"direction_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.direction_label.sizePolicy().hasHeightForWidth())
        self.direction_label.setSizePolicy(sizePolicy2)
        self.direction_label.setMinimumSize(QSize(150, 25))
        self.direction_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.direction_label, 2, 1, 1, 1)

        self.shape_label = QLabel(Frame)
        self.shape_label.setObjectName(u"shape_label")
        sizePolicy2.setHeightForWidth(self.shape_label.sizePolicy().hasHeightForWidth())
        self.shape_label.setSizePolicy(sizePolicy2)
        self.shape_label.setMinimumSize(QSize(150, 25))
        self.shape_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.shape_label, 2, 2, 1, 1)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.direction_img_label.setText(QCoreApplication.translate("Frame", u"\ubc29\ud5a5 \uc774\ubbf8\uc9c0", None))
        self.shape_img_label.setText(QCoreApplication.translate("Frame", u"\uc218\ud615 \uc77c\uce58 \uc774\ubbf8\uc9c0", None))
        self.study_select_label.setText(QCoreApplication.translate("Frame", u"\ud559\uc2b5\ud560 \uc9c0\ubb38\uc790 \uc120\ud0dd", None))
        self.study_img_label.setText(QCoreApplication.translate("Frame", u"\ud559\uc2b5\ud560 \uc774\ubbf8\uc9c0", None))
        self.screen_img_label.setText(QCoreApplication.translate("Frame", u"\uc601\uc0c1\uc774 \ubcf4\uc774\ub294 \uc601\uc5ed", None))
        self.direction_label.setText(QCoreApplication.translate("Frame", u"\ubc29\ud5a5", None))
        self.shape_label.setText(QCoreApplication.translate("Frame", u"\uc218\ud615", None))
    # retranslateUi

