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
        self.ui.host_manager_btn.clicked.connect(lambda: host_manager.show(self))
        self.ui.host_select.setModel(host_manager.get_model())
        self.ui.host_select.activated.connect(self.update_image_list)
        self.update_ui()

    def update_ui(self):
        ui = self.ui

    def update_image_list(self, index):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
