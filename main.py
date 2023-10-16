import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog

from HostManager import HostManager
from task_dialog import TaskDialog, SaveImageTask, LoadImageTask, SyncImageTask
from ui_mainwindow import Ui_MainWindow
from ui_select_host import Ui_SelectHost

host_manager = HostManager()



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.host_manager_btn.clicked.connect(lambda: host_manager.show(self))
        self.ui.host_select.setModel(host_manager.get_model())
        self.ui.host_select.activated.connect(self.update_image_list)
        self.ui.save_to_file_btn.clicked.connect(self.on_save_image_click)
        self.ui.load_from_file_btn.clicked.connect(self.on_load_image_click)
        self.ui.sync_to_host_htn.clicked.connect(self.on_sync_image_click)
        self.model = None
        self.host_index = 0
        if len(host_manager.host_list) > 0:
            self.update_ui()

    def update_ui(self):
        index = self.host_index
        ui = self.ui
        host = host_manager.host_list[index]
        host.refresh_images()
        self.model = host.get_images_model()
        ui.image_list.setModel(self.model)

    def update_image_list(self, index):
        self.host_index = index
        self.update_ui()

    def on_save_image_click(self):
        selected = self.model.get_selected()
        if len(selected) == 0:
            box = QMessageBox(self)
            box.setWindowTitle("消息")
            box.setText("没有勾选镜像")
            box.setStandardButtons(QMessageBox.StandardButton.Ok)
            box.exec()
            return
        dialog = TaskDialog(self)
        dialog.setWindowTitle(f"保存{len(selected)}个镜像")
        tasks = [SaveImageTask(dialog, x) for x in selected]
        dialog.show_dialog(tasks)

    def on_load_image_click(self):
        file_d = QFileDialog.getOpenFileNames(self)
        files = file_d[0]
        if len(files) == 0:
            return
        dialog = TaskDialog(self)
        dialog.setWindowTitle(f"导入{len(files)}个镜像")
        host = host_manager.host_list[self.host_index]
        tasks = [LoadImageTask(dialog, host, x) for x in files]
        dialog.show_dialog(tasks)

    def on_sync_image_click(self):
        select_host_dialog = QDialog(self)
        ui = Ui_SelectHost()
        ui.setupUi(select_host_dialog)
        for x in host_manager.host_list:
            ui.host_list.addItem(x.get_name())
        if select_host_dialog.exec() == 0:
            return
        if ui.host_list.currentIndex() == self.host_index:
            box = QMessageBox(self)
            box.setWindowTitle("消息")
            box.setText("目标主机不能与当前主机相同")
            box.setStandardButtons(QMessageBox.StandardButton.Ok)
            box.exec()
            return
        selected = self.model.get_selected()
        if len(selected) == 0:
            box = QMessageBox(self)
            box.setWindowTitle("消息")
            box.setText("没有勾选镜像")
            box.setStandardButtons(QMessageBox.StandardButton.Ok)
            box.exec()
            return

        dialog = TaskDialog(self)
        dialog.setWindowTitle(f"转移{len(selected)}个镜像")
        host = host_manager.host_list[ui.host_list.currentIndex()]
        tasks = [SyncImageTask(dialog, x, host) for x in selected]
        dialog.show_dialog(tasks)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
