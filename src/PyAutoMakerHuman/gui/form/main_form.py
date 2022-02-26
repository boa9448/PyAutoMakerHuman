# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(983, 664)
        self.actioninfo = QAction(MainWindow)
        self.actioninfo.setObjectName(u"actioninfo")
        self.actionexit = QAction(MainWindow)
        self.actionexit.setObjectName(u"actionexit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.study_mode_button = QPushButton(self.centralwidget)
        self.study_mode_button.setObjectName(u"study_mode_button")

        self.horizontalLayout.addWidget(self.study_mode_button)

        self.lang_mode_button = QPushButton(self.centralwidget)
        self.lang_mode_button.setObjectName(u"lang_mode_button")

        self.horizontalLayout.addWidget(self.lang_mode_button)

        self.conversation_mode_button = QPushButton(self.centralwidget)
        self.conversation_mode_button.setObjectName(u"conversation_mode_button")

        self.horizontalLayout.addWidget(self.conversation_mode_button)

        self.mirror_mode_button = QPushButton(self.centralwidget)
        self.mirror_mode_button.setObjectName(u"mirror_mode_button")

        self.horizontalLayout.addWidget(self.mirror_mode_button)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame, 1, 0, 1, 2)

        self.horizontalSpacer = QSpacerItem(694, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 983, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actioninfo)
        self.menu.addSeparator()
        self.menu.addAction(self.actionexit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\uc9c0\ud654\uc790", None))
        self.actioninfo.setText(QCoreApplication.translate("MainWindow", u"\uc815\ubcf4", None))
        self.actionexit.setText(QCoreApplication.translate("MainWindow", u"\uc885\ub8cc", None))
        self.study_mode_button.setText(QCoreApplication.translate("MainWindow", u"\ud559\uc2b5\ubaa8\ub4dc", None))
        self.lang_mode_button.setText(QCoreApplication.translate("MainWindow", u"\uc9c0\ud654\ubaa8\ub4dc", None))
        self.conversation_mode_button.setText(QCoreApplication.translate("MainWindow", u"\ud68c\ud654\ubaa8\ub4dc", None))
        self.mirror_mode_button.setText(QCoreApplication.translate("MainWindow", u"\uac70\uc6b8\ubaa8\ub4dc On/Off", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c", None))
    # retranslateUi

