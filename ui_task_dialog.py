# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'task_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QPlainTextEdit, QProgressBar,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.task_text = QPlainTextEdit(Dialog)
        self.task_text.setObjectName(u"task_text")

        self.verticalLayout.addWidget(self.task_text)

        self.log_text = QPlainTextEdit(Dialog)
        self.log_text.setObjectName(u"log_text")

        self.verticalLayout.addWidget(self.log_text)

        self.progress_bar = QProgressBar(Dialog)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMaximum(1000)
        self.progress_bar.setValue(24)

        self.verticalLayout.addWidget(self.progress_bar)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
    # retranslateUi

