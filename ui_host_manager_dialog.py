# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'host_manager_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.host_list = QListView(Dialog)
        self.host_list.setObjectName(u"host_list")
        self.host_list.setGeometry(QRect(10, 20, 101, 261))
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(120, 20, 271, 201))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.host_user = QLineEdit(self.gridLayoutWidget)
        self.host_user.setObjectName(u"host_user")

        self.gridLayout.addWidget(self.host_user, 3, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.host_pass = QLineEdit(self.gridLayoutWidget)
        self.host_pass.setObjectName(u"host_pass")

        self.gridLayout.addWidget(self.host_pass, 4, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.host_addr = QLineEdit(self.gridLayoutWidget)
        self.host_addr.setObjectName(u"host_addr")

        self.gridLayout.addWidget(self.host_addr, 2, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.host_type = QComboBox(self.gridLayoutWidget)
        self.host_type.addItem("")
        self.host_type.setObjectName(u"host_type")

        self.gridLayout.addWidget(self.host_type, 0, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.host_name = QLineEdit(self.gridLayoutWidget)
        self.host_name.setObjectName(u"host_name")

        self.gridLayout.addWidget(self.host_name, 1, 1, 1, 1)

        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(120, 250, 271, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.host_add_btn = QPushButton(self.horizontalLayoutWidget)
        self.host_add_btn.setObjectName(u"host_add_btn")

        self.horizontalLayout.addWidget(self.host_add_btn)

        self.host_delete_btn = QPushButton(self.horizontalLayoutWidget)
        self.host_delete_btn.setObjectName(u"host_delete_btn")

        self.horizontalLayout.addWidget(self.host_delete_btn)

        self.host_save_btn = QPushButton(self.horizontalLayoutWidget)
        self.host_save_btn.setObjectName(u"host_save_btn")

        self.horizontalLayout.addWidget(self.host_save_btn)

        QWidget.setTabOrder(self.host_list, self.host_type)
        QWidget.setTabOrder(self.host_type, self.host_name)
        QWidget.setTabOrder(self.host_name, self.host_addr)
        QWidget.setTabOrder(self.host_addr, self.host_user)
        QWidget.setTabOrder(self.host_user, self.host_pass)
        QWidget.setTabOrder(self.host_pass, self.host_add_btn)
        QWidget.setTabOrder(self.host_add_btn, self.host_delete_btn)
        QWidget.setTabOrder(self.host_delete_btn, self.host_save_btn)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u7528\u6237\u540d", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u5730\u5740", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u5bc6\u7801", None))
        self.host_type.setItemText(0, QCoreApplication.translate("Dialog", u"Docker CLI", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"\u7c7b\u578b", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u540d\u79f0", None))
        self.host_add_btn.setText(QCoreApplication.translate("Dialog", u"\u6dfb\u52a0", None))
        self.host_delete_btn.setText(QCoreApplication.translate("Dialog", u"\u5220\u9664", None))
        self.host_save_btn.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58", None))
    # retranslateUi

