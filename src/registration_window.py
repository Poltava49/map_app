from PyQt5.Qt import QDialog, QMessageBox
import sqlite3
from PyQt5 import uic
from db import DataBase
from models import UserAttributes

class RegistrationWindow(QDialog):
    def __init__(self, db) -> None:
        super().__init__()
        self.initUI()
        self.db = db

    def initUI(self):
        uic.loadUi('../ui_files/reg_window.ui', self)
        self.pushButton.clicked.connect(self.pull_new_user)

    def pull_new_user(self):
        name, login, password = self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()
        if self.db.check_user_by_login(login):
            QMessageBox.warning(self, "Ошибка", "Такой пользователь существует")
        else:
            res = self.db.add_new_user(UserAttributes(name=name, login=login, password=password))
            if res:
                QMessageBox.warning(self, "Успех", "Пользователь зарегистрирован")
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка при регистрации пользователя")
