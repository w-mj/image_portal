import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from HostManager import HostManager
from ui_mainwindow import Ui_MainWindow

host_manager = HostManager()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionEndpoint.triggered.connect(lambda: host_manager.show(self))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
