from PyQt5.Qt import QDialog, QMessageBox
import sqlite3
from PyQt5 import uic
from db import DataBase



class RegistrationWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.connection = sqlite3.connect("map_users_db.sqlite")



    def initUI(self):
        uic.loadUi('../ui_files/reg_window.ui', self)
        self.pushButton.clicked.connect(self.add_new_user)



    def add_new_user(self):
        name, login, password = self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()
        try:
            res = self.connection.cursor().execute(f"""SELECT login FROM users WHERE login = '{login}'""").fetchall()[0][0]
            if res == self.current_login:
                QMessageBox.warning(self, "Ошибка", "Такой пользователь существует")
        except:
                self.connection.cursor().execute(f"""INSERT INTO users (name,login,password) VALUES ('{name}', '{login}', '{password}')""").fetchall()
                self.connection.commit()
                QMessageBox.warning(self, "Успех", "Пользователь зарегистрирован")
                self.close()

