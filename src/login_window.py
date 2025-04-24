from PyQt5.Qt import QDialog, QMessageBox
import sqlite3
from PyQt5 import uic
from models import AppState


class LoginWindow(QDialog):
    def __init__(self, db, reg_window) -> None:
        super().__init__()
        self.connection = sqlite3.connect("map_users_db.sqlite")
        self.reg_window = reg_window
        self.db = db
        self.initUI()

    def initUI(self) -> None:
        uic.loadUi('../ui_files/authorization_window.ui', self)
        self.setWindowTitle("Авторизация")
        self.setFixedSize(400, 290)
        self.login = ''
        self.lineEdit_2.setEchoMode(self.lineEdit_2.Password)
        self.pushButton.clicked.connect(self.validation_user)
        self.pushButton_2.clicked.connect(self.close_dialog)
        self.pushButton_3.clicked.connect(self.add_new_user)

    def add_new_user(self):
        self.reg_window.exec_()

    def close_dialog(self):
        self.close()

    def validation_user(self):
        self.login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        res = self.db.validation_user_enter(self.login, password)
        if res:
            if (self.login, password) in res:
                self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")


    def get_user_login(self):
        return self.login
