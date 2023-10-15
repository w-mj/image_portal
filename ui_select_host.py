# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_host.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_SelectHost(object):
    def setupUi(self, SelectHost):
        if not SelectHost.objectName():
            SelectHost.setObjectName(u"SelectHost")
        SelectHost.resize(184, 110)
        self.verticalLayout = QVBoxLayout(SelectHost)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(SelectHost)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.host_list = QComboBox(SelectHost)
        self.host_list.setObjectName(u"host_list")

        self.verticalLayout.addWidget(self.host_list)

        self.buttonBox = QDialogButtonBox(SelectHost)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SelectHost)
        self.buttonBox.accepted.connect(SelectHost.accept)
        self.buttonBox.rejected.connect(SelectHost.reject)

        QMetaObject.connectSlotsByName(SelectHost)
    # setupUi

    def retranslateUi(self, SelectHost):
        SelectHost.setWindowTitle(QCoreApplication.translate("SelectHost", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("SelectHost", u"\u9009\u62e9\u76ee\u6807\u4e3b\u673a", None))
    # retranslateUi

