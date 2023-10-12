# This Python file uses the following encoding: utf-8
from typing import Union, Any

import PySide6.QtCore

from ui_host_manager_dialog import Ui_Dialog
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QAbstractListModel, QModelIndex, QModelRoleData
from PySide6.QtCore import Qt


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


class HostItem:
    def __init__(self, d=None):
        if d is None:
            d = dict()
        self.data = d

    def get_name(self):
        return self.data.get("name", self.data.get("addr", "unnamed"))

    def get(self, key):
        return self.data.get(key, "")

    def set(self, key, value):
        self.data[key] = value


class HostManager:
    def __init__(self):
        self.host_list = []

    def show(self, parent=None):
        dialog = QDialog(parent)
        ui = Ui_Dialog()
        ui.setupUi(dialog)

        model = HostListModel(self.host_list)
        ui.host_list.setModel(model)

        current_select = 0

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
            self.host_list.append(HostItem({"name": "new" + str(len(self.host_list))}))
            model.endInsertRows()
            change_current_edit(model.rowCount() - 1)

        ui.host_add_btn.clicked.connect(add_blank_item)
        ui.host_save_btn.clicked.connect(lambda: model.dataChanged.emit(QModelIndex(), current_select, current_select))

        def delete_item():
            model.beginRemoveRows(QModelIndex(), current_select, current_select)
            self.host_list.pop(current_select)
            model.endRemoveRows()
            change_current_edit(current_select)

        ui.host_delete_btn.clicked.connect(delete_item)
        change_current_edit(0)

        dialog.show()
