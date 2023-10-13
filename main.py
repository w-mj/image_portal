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
        if len(host_manager.host_list) > 0:
            self.update_ui(0)

    def update_ui(self, index):
        ui = self.ui
        host = host_manager.host_list[index]
        host.refresh_images()
        ui.image_list.setModel(host.get_images_model())

    def update_image_list(self, index):
        self.update_ui(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
