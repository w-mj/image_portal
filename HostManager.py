# This Python file uses the following encoding: utf-8
import json
from typing import Union, Any

import PySide6.QtCore

from endpoints.endpoint import HostItem
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


class HostManager:
    def __init__(self):
        self.host_list = []
        self.load_from_file()

    def save_to_file(self):
        json.dump(self.host_list, open("image_transfer.json", "w", encoding='utf8'))

    def load_from_file(self):
        try:
            self.host_list = json.load(open("image_transfer.json", encoding='utf8'))
        except FileNotFoundError:
            pass

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
