import os.path
import threading
from abc import abstractmethod
from typing import List, Any

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Signal

import utils
from HostManager import HostItem
from endpoints.endpoint import Image
from ui_task_dialog import Ui_Dialog


class TaskDialog(QDialog):
    progress_maximum_signal = Signal(int)
    progress_value_signal = Signal(int)
    progress_add_log_signal = Signal(str)
    progress_update_task_signal = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.log_text.setReadOnly(True)
        self.ui.task_text.setReadOnly(True)
        self._log = ""
        self.progress_maximum_signal.connect(self.set_progress_maximum_slot)
        self.progress_value_signal.connect(self.set_progress_value_slot)
        self.progress_add_log_signal.connect(self.add_log_slot)
        self.progress_update_task_signal.connect(self.update_task_text_slot)
        self.tasks = []

    def set_progress_maximum_slot(self, value):
        self.ui.progress_bar.setMaximum(value)

    def set_progress_value_slot(self, value):
        self.ui.progress_bar.setValue(value)

    def add_log_slot(self, log):
        self._log += log + "\n"
        self.ui.log_text.setPlainText(self._log)

    def update_task_text_slot(self, tasks):
        text = ""
        for t in tasks:
            status = ""
            if t.is_failed():
                status = "failed"
            elif t.is_running():
                status = "running"
            elif t.is_finished():
                status = "done"
            else:
                status = "waiting"
            text += f"{t.name()} ... [{status}]\n"
        self.ui.task_text.setPlainText(text)

    def show_dialog(self, tasks: List['BackgroundTask']):
        super().show()
        self.tasks = tasks
        def thread():
            for t in tasks:
                self.progress_update_task_signal.emit(tasks)
                self.progress_add_log_signal.emit(f"========= start run {t.name()} ============")
                t.start()
                self.progress_add_log_signal.emit(f"========= end run {t.name()} ============\n")
            self.progress_update_task_signal.emit(tasks)
        threading.Thread(target=thread).start()

    def closeEvent(self, arg__1):
        for t in self.tasks:
            t.kill()
        super().closeEvent(arg__1)


class BackgroundTask:
    def __init__(self, name: str, dialog: TaskDialog):
        self._name = name
        self.dialog = dialog
        self.state = 0   # 0: waiting, 1: running, 2: finished, 3: failed
        self.maximum = 0
        self.state_lock = threading.Lock()

    def name(self) -> str:
        return self._name

    def is_finished(self) -> bool:
        with self.state_lock:
            return self.state == 2

    def is_running(self) -> bool:
        with self.state_lock:
            return self.state == 1

    def is_failed(self) -> bool:
        with self.state_lock:
            return self.state == 3

    def kill(self):
        with self.state_lock:
            self.state = 3

    @abstractmethod
    def run(self):
        pass

    def add_log(self, text):
        self.dialog.progress_add_log_signal.emit(text)

    def start(self):
        if self.state != 0:
            print(f"start task {self._name} but state={self.state}")
            return
        try:
            with self.state_lock:
                self.state = 1
            self.run()
        except Exception as e:
            with self.state_lock:
                self.state = 3
            self.dialog.progress_add_log_signal.emit(str(e))
            return
        with self.state_lock:
            self.state = 2
        self.set_progress_value(self.maximum)

    def set_progress_maximum(self, value):
        self.maximum = value
        self.dialog.progress_maximum_signal.emit(10000)

    def set_progress_value(self, value):
        if self.maximum == 0:
            v = 0
        else:
            v = int(value / self.maximum * 10000)
        self.dialog.progress_value_signal.emit(v)


class SaveImageTask(BackgroundTask):
    def __init__(self, dialog, image: Image):
        super().__init__(f"save {image.name()}", dialog)
        self.image = image

    def get_name(self):
        return (self.image.name().
                replace(":", "_").
                replace("/", "_") +
                ".tar.gz")

    def run(self):
        stream = self.image.get_stream()
        self.set_progress_maximum(self.image.size())
        cnt = 0
        path = os.path.join(os.getcwd(), self.get_name())
        self.add_log(f"开始保存镜像：{self.image.name()}")
        self.add_log(f"镜像大小：{self.image.size_str()}")
        self.add_log(f"镜像文件名：{path}")
        with open(path, "wb") as f:
            while self.is_running():
                d = stream.read(1024)
                if not d:
                    break
                f.write(d)
                cnt += len(d)
                self.set_progress_value(cnt)
        self.add_log(f"保存完成，文件大小：{utils.size_str(os.stat(path).st_size)}")


class LoadImageTask(BackgroundTask):
    def __init__(self, dialog, host: HostItem, path: str):
        super().__init__(f"load {path}", dialog)
        self.host = host
        self.path = path

    def run(self):
        self.set_progress_maximum(os.stat(self.path).st_size)
        self.add_log(f"开始导入{self.path}")
        self.add_log(f"文件大小：{utils.size_str(os.stat(self.path).st_size)}")
        stream = self.host.get_endpoint().create_image_stream(None)
        cnt = 0
        try:
            with open(self.path, "rb") as f:
                while self.is_running():
                    d = f.read(1024)
                    if not d:
                        break
                    stream.write(d)
                    cnt += len(d)
                    self.set_progress_value(cnt)
                self.add_log("导入完成")
        finally:
            stream.close()


class SyncImageTask(BackgroundTask):
    def __init__(self, dialog, image, host):
        super().__init__(f"sync {image.name()} to {host.get_name()}", dialog)
        self.image = image
        self.host = host

    def run(self):
        self.set_progress_maximum(self.image.size())
        from_stream = self.image.get_stream()
        target_stream = self.host.get_endpoint().create_image_stream(None)
        self.add_log(f"开始将{self.image.name()}导入到{self.host.get_name()}")
        self.add_log(f"镜像大小：{self.image.size_str()}")
        cnt = 0
        try:
            while self.is_running():
                d = from_stream.read(1024)
                if not d:
                    break
                target_stream.write(d)
                cnt += len(d)
                self.set_progress_value(cnt)
            self.add_log(f"导入完成，传输数据大小：{utils.size_str(cnt)}")
        finally:
            target_stream.close()
