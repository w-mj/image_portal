# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
    QLayout, QListView, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(582, 552)
        self.actionEndpoint = QAction(MainWindow)
        self.actionEndpoint.setObjectName(u"actionEndpoint")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(self.centralwidget)
        self.formLayout.setObjectName(u"formLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.host_select = QComboBox(self.centralwidget)
        self.host_select.setObjectName(u"host_select")

        self.verticalLayout.addWidget(self.host_select)

        self.image_list = QListView(self.centralwidget)
        self.image_list.setObjectName(u"image_list")

        self.verticalLayout.addWidget(self.image_list)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.host_manager_btn = QPushButton(self.centralwidget)
        self.host_manager_btn.setObjectName(u"host_manager_btn")

        self.horizontalLayout.addWidget(self.host_manager_btn)

        self.save_to_file_btn = QPushButton(self.centralwidget)
        self.save_to_file_btn.setObjectName(u"save_to_file_btn")

        self.horizontalLayout.addWidget(self.save_to_file_btn)

        self.load_from_file_btn = QPushButton(self.centralwidget)
        self.load_from_file_btn.setObjectName(u"load_from_file_btn")

        self.horizontalLayout.addWidget(self.load_from_file_btn)

        self.sync_to_host_htn = QPushButton(self.centralwidget)
        self.sync_to_host_htn.setObjectName(u"sync_to_host_htn")

        self.horizontalLayout.addWidget(self.sync_to_host_htn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.formLayout.setLayout(0, QFormLayout.SpanningRole, self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ImageTransfer", None))
        self.actionEndpoint.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u673a\u7ba1\u7406", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.host_manager_btn.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u673a\u7ba1\u7406", None))
        self.save_to_file_btn.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u4e3a\u6587\u4ef6", None))
        self.load_from_file_btn.setText(QCoreApplication.translate("MainWindow", u"\u4ece\u6587\u4ef6\u5bfc\u5165", None))
        self.sync_to_host_htn.setText(QCoreApplication.translate("MainWindow", u"\u540c\u6b65\u5230\u4e3b\u673a", None))
    # retranslateUi

