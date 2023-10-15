# This Python file uses the following encoding: utf-8
import json
from typing import Union, Any

import PySide6.QtCore

from endpoints.docker_cli_endpoint import DockerCLIEndpoint
from ui_host_manager_dialog import Ui_Dialog
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QAbstractListModel, QAbstractTableModel, QModelIndex, QModelRoleData
from PySide6.QtCore import Qt


class HostImageModel(QAbstractTableModel):
    def __init__(self, host_list):
        super().__init__()
        self.image_list = host_list
        self._check_stats = {}

    def setData(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], value: Any,
                role: int = ...) -> bool:
        if index.column() == 0 and role == Qt.ItemDataRole.CheckStateRole:
            self._check_stats[self.image_list[index.row()].name()] = Qt.CheckState.Checked if value > 0 else Qt.CheckState.Unchecked
            return True
        return False

    def flags(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex]) -> PySide6.QtCore.Qt.ItemFlag:
        if not index.isValid():
            return super().flags(index)
        flag = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.column() == 0:
            flag |= Qt.ItemFlag.ItemIsUserCheckable
        return flag

    def headerData(self, section: int, orientation: PySide6.QtCore.Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ["选择", "镜像名", "ID", "大小"][section]
        return super().headerData(section, orientation, role)

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return ""
            elif index.column() == 1:
                return self.image_list[index.row()].name()
            elif index.column() == 2:
                return self.image_list[index.row()].hash()
            elif index.column() == 3:
                return str(self.image_list[index.row()].size_str())
        elif role == Qt.ItemDataRole.CheckStateRole:
            if index.column() == 0:
                return self._check_stats.get(self.image_list[index.row()].name(), Qt.CheckState.Unchecked)
        return None

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.image_list)

    def columnCount(self, parent=...):
        return 4

    def get_selected(self):
        return [x for x in self.image_list if self._check_stats.get(x.name(), Qt.CheckState.Unchecked) == Qt.CheckState.Checked]


class HostItem:
    def __init__(self, d=None):
        if d is None:
            d = dict()
        self._data = d
        self._endpoint = None
        self._image_list = []
        self._model = None

    def get_name(self):
        return self._data.get("name", self._data.get("addr", "unnamed"))

    def get(self, key):
        return self._data.get(key, "")

    def set(self, key, value):
        self._data[key] = value

    def get_type(self):
        return self.get("type")

    def get_user(self):
        return self.get("user")

    def get_pass(self):
        return self.get("pass")

    def get_addr(self):
        return self.get("addr")

    def data(self):
        return self._data

    def get_endpoint(self):
        if self._endpoint and self._endpoint.type == self.get_type():
            return self._endpoint
        if self.get_type() == "Docker CLI":
            self._endpoint = DockerCLIEndpoint(self.get_type(), self.get_addr(), self.get_user(), self.get_pass())
        else:
            raise RuntimeError("Unknown host type " + self.get_type())
        return self._endpoint

    def refresh_images(self):
        model = self.get_endpoint()
        self._image_list = model.get_images()
        self._image_list = sorted(self._image_list, key=lambda x: x.name())
        if self._model:
            self._model.dataChanged.emit(QModelIndex(), 0, self._model.rowCount())

    def get_images_model(self):
        if not self._model:
            self._model = HostImageModel(self._image_list)
        return self._model


class HostListModel(QAbstractListModel):
    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.host_list[index.row()].get_name()
        return None

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.host_list)

    def __init__(self, host_list):
        super().__init__()
        self.host_list = host_list


class HostManager:
    def __init__(self):
        self.host_list = []
        self.load_from_file()
        self.model = HostListModel(self.host_list)

    def save_to_file(self):
        json.dump([x.data() for x in self.host_list], open("image_transfer.json", "w", encoding='utf8'))

    def load_from_file(self):
        try:
            self.host_list = json.load(open("image_transfer.json", encoding='utf8'))
            self.host_list = [HostItem(x) for x in self.host_list]
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError as e:
            print("load from json error ", e)
            pass

    def get_model(self):
        return self.model

    def show(self, parent=None):
        dialog = QDialog(parent)
        ui = Ui_Dialog()
        ui.setupUi(dialog)

        model = self.get_model()
        ui.host_list.setModel(model)

        current_select = 0

        ui.host_type.textActivated.connect(lambda x: self.host_list[current_select].set("type", x))

        def change_current_edit(i):
            nonlocal current_select
            current_select = i
            ui.host_name.setDisabled(current_select >= len(self.host_list))
            ui.host_addr.setDisabled(current_select >= len(self.host_list))
            ui.host_user.setDisabled(current_select >= len(self.host_list))
            ui.host_pass.setDisabled(current_select >= len(self.host_list))
            if current_select >= len(self.host_list):
                return
            ui.host_name.setText(self.host_list[i].get("name"))
            ui.host_addr.setText(self.host_list[i].get("addr"))
            ui.host_user.setText(self.host_list[i].get("user"))
            ui.host_pass.setText(self.host_list[i].get("pass"))

        ui.host_list.clicked.connect(lambda x: change_current_edit(x.row()))

        def text_setter(key):
            nonlocal current_select
            return lambda v: self.host_list[current_select].set(key, v)

        ui.host_name.textEdited.connect(text_setter("name"))
        ui.host_addr.textEdited.connect(text_setter("addr"))
        ui.host_user.textEdited.connect(text_setter("user"))
        ui.host_pass.textEdited.connect(text_setter("pass"))

        def add_blank_item():
            model.beginInsertRows(QModelIndex(), model.rowCount(), model.rowCount() + 1)
            self.host_list.append(HostItem({
                "name": "new" + str(len(self.host_list)),
                "type": ui.host_type.currentText()
            }))
            model.endInsertRows()
            change_current_edit(model.rowCount() - 1)

        ui.host_add_btn.clicked.connect(add_blank_item)

        def save():
            model.dataChanged.emit(QModelIndex(), current_select, current_select)
            self.save_to_file()

        ui.host_save_btn.clicked.connect(save)

        def delete_item():
            model.beginRemoveRows(QModelIndex(), current_select, current_select)
            self.host_list.pop(current_select)
            model.endRemoveRows()
            change_current_edit(current_select)

        ui.host_delete_btn.clicked.connect(delete_item)
        change_current_edit(0)

        dialog.show()
