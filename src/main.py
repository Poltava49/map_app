import sys
from PyQt5.Qt import QApplication, QDialog
from models import AppState
from login_window import LoginWindow
from app import BaseLogic
from db import DataBase
from registration_window import RegistrationWindow
from main_window import MyMainWindow



# def main() -> None:
#     app = QApplication(sys.argv)
#     reg_window = RegistrationWindow()
#     login_window = LoginWindow(reg_window)
#     reg_window.show()
#     db = DataBase(login_window.login)
#     main_window = MyMainWindow(db)
#     if login_window.exec_() == QDialog.Accepted:
#         logic = BaseLogic(db,main_window)
#         main_window.show()
#         # sys.exit(app.exec_())
#     else:
#         sys.exit(app.exec_())


def main():
    app = QApplication(sys.argv)
    reg_window = RegistrationWindow()
    login_window = LoginWindow(reg_window)

    if login_window.exec_() == QDialog.Accepted:
        db = DataBase(login_window.login)
        main_window = MyMainWindow(db)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(app.exec())


if __name__ == '__main__':
    main()





















#
#
# class AppState:
#     def __init__(self):
#         self.toponym_longitude = ''
#         self.toponym_lattitude = ''
#         self.current_user_login = ''
#         self.selected_places = {}
#         self.checkpoints = []
#         self.full_address = ''
#         self.address_index = ''
#         self.info_organization = ''
#         self.map_type = 'map'
#         self.map_size = 0.003
#
#
# class MapCoords:
#     def __init__(self):
#         self.state = state
#         self.setMouseTracking(True)
#     def key_event(self, event):
#         x = 0.015
#         if event.key() == Qt.Key_Up and self.state.size >= 0.011:
#             self.state.size -= x * 2
#             self.pull_image()
#         elif event.key() == Qt.Key_Down:
#             self.size += x * 2
#             self.pull_image(flag=True)
#         elif event.key() == Qt.Key_D:
#             self.toponym_longitude = str(float(self.toponym_longitude) + self.state.step)
#             self.pull_image(flag=True)
#         elif event.key() == Qt.Key_A:
#             self.toponym_longitude = str(float(self.toponym_longitude) - self.step)
#             self.pull_image(flag=True)
#         elif event.key() == Qt.Key_S:
#             self.toponym_lattitude = str(float(self.toponym_lattitude) - self.step)
#             self.pull_image(flag=True)
#         elif event.key() == Qt.Key_W:
#             self.toponym_lattitude = str(float(self.toponym_lattitude) + self.step)
#             self.pull_image(flag=True)
#         else:
#             super().keyPressEvent(event)
#
#
#     def mouseMoveEvent(self, event):
#         start_x, start_y = 380, 365
#         step_x, step_y = 0.00001913, 0.00001209
#         print(f'{event.x(), event.y()}')
#         if (int(event.x()) < 45 or int(event.x()) > 615) or (int(event.y()) < 196 or int(event.y()) > 530):
#             self.textBrowser_2.setText('вышли за границы')
#         else:
#             if event.x() < start_x:
#                 self.new_x = abs(start_x - event.x())
#                 self.point_x = str(float(self.toponym_longitude) - round((self.new_x * step_x), 4))
#             elif event.x() > start_x:
#                 self.new_x = abs(event.x() - start_x)
#                 self.point_x = str(float(self.toponym_longitude) + round((self.new_x * step_x), 4))
#             if event.y() < start_y:
#                 self.new_y = abs(start_y - event.y())
#                 self.point_y = str(float(self.toponym_lattitude) + round((self.new_y * step_y), 4))
#             elif event.y() > start_y:
#                 self.new_y = abs(event.y()-start_y)
#                 self.point_y = str(float(self.toponym_lattitude) - round((self.new_y * step_y), 4))
#
#     def is_valid_coordinate(self, lat, lon):
#         return (-90 <= float(lat) <= 90) and (-180 <= float(lon) <= 180)
#
#     def get_coords(self):
#         try:
#             self.toponym_longitude, self.toponym_lattitude, self.full_adress, self.adress_index = geocoder(
#                 self.textEdit.toPlainText())
#         except:
#             self.toponym_longitude, self.toponym_lattitude, self.full_adress = geocoder(self.textEdit.toPlainText())
#
#         self.checkpoint.append(f"{self.toponym_longitude},{self.toponym_lattitude},ya_ru")
#         self.pull_responce_info()
#
#
#
#
# class MainWindow:
#     def __init__(self, login):
#         super().__init__()
#         uic.loadUi('interface.ui', self)
#         self.add_all_user_selected_places()
#         self.map_layers = ['map', 'sat', 'sat,skl']
#         self.comboBox.addItems(['схема','спутник','гибрид'])
#         self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
#         self.textEdit.setPlaceholderText("Введите адрес здесь...")
#         self.pushButton.clicked.connect(self.pull_image)
#         self.comboBox.currentIndexChanged.connect(self.pull_image)
#         self.pushButton_2.clicked.connect(self.remove_checkpoint)
#         self.checkBox.stateChanged.connect(self.pull_responce_info)
#         self.pushButton_3.clicked.connect(self.add_selected_places)
#         self.pushButton_4.clicked.connect(self.remove_selected_places)
#         self.pushButton_5.clicked.connect(self.search_choose_selected_places)
#
#
#
#     def pull_responce_info(self, state=1):
#         if state == 2:
#             self.textBrowser.setText(f'{self.full_adress} {self.adress_index}')
#         else:
#             self.textBrowser.setText(f'{self.full_adress}')
#         self.add_user_history_search()
#
#
# class LoginWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         # Зададим тип базы данных
#         self.login = ''
#         self.connection = db
#         uic.loadUi('authorization_window.ui', self)
#         self.setWindowTitle("Авторизация")
#         self.setFixedSize(400, 290)
#         self.lineEdit_2.setEchoMode(self.lineEdit_2.Password)
#         self.pushButton.clicked.connect(self.check_user)
#         self.pushButton_2.clicked.connect(self.close_dialog)
#         self.pushButton_3.clicked.connect(self.add_new_user)
#
#
#     def add_new_user(self):
#         self.second_window = RegistrationWindow()  # Создаем экземпляр второго окна
#         self.second_window.exec_()
#
#
#     def close_dialog(self):
#         self.close()
#
#     def check_user(self):
#         # Проверка логина и пароля (заглушка)
#         self.login = self.lineEdit.text()
#         password = self.lineEdit_2.text()
#         res = self.connection.cursor().execute(f"""SELECT login, password FROM users""").fetchall()
#         if (self.login, password) in res:
#             self.accept()
#         else:
#             QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
#
# class RegistrationWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi('reg_window.ui', self)
#         self.connection = sqlite3.connect("map_users_db.sqlite")
#         self.pushButton.clicked.connect(self.add_new_user)
#
#
#
#
#
# class DataBase:
#     def add_new_user(self):
#         name, login, password = self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()
#         try:
#             res = \
#             self.connection.cursor().execute(f"""SELECT login FROM users WHERE login = '{login}'""").fetchall()[0][0]
#             if res == self.current_login:
#                 QMessageBox.warning(self, "Ошибка", "Такой пользователь существует")
#         except:
#             self.connection.cursor().execute(
#                 f"""INSERT INTO users (name,login,password) VALUES ('{name}', '{login}', '{password}')""").fetchall()
#             self.connection.commit()
#             QMessageBox.warning(self, "Успех", "Пользователь зарегистрирован")
#             self.close()
#
#
# class MyMainWindow(QMainWindow):
#     def __init__(self, login):
#         super().__init__()
#         uic.loadUi('interface.ui', self)
#         self.size = 0.003
#         self.step = 0.0001
#         self.type_map = 'map'
#         self.new_x = 0
#         self.new_y = 0
#         self.checkpoint = []
#         self.dict_users_selected_places = {}
#         self.label_2 = ''
#         self.point_x = 0
#         self.point_y = 0
#         self.info_organization = ''
#         self.current_user_login = login
#         self.connection = sqlite3.connect("map_users_db.sqlite")
#         self.id = (self.connection.cursor().execute(
#             f"""SELECT id FROM users WHERE login = '{self.current_user_login}'""").fetchall())[0][0]
#         self.add_all_user_selected_places()
#         self.setMouseTracking(True)
#         self.map_layers = ['map', 'sat', 'sat,skl']
#         self.comboBox.addItems(['схема','спутник','гибрид'])
#         self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
#         self.textEdit.setPlaceholderText("Введите адрес здесь...")
#         self.pushButton.clicked.connect(self.pull_image)
#         self.comboBox.currentIndexChanged.connect(self.pull_image)
#         self.pushButton_2.clicked.connect(self.remove_checkpoint)
#         self.checkBox.stateChanged.connect(self.pull_responce_info)
#         self.pushButton_3.clicked.connect(self.add_selected_places)
#         self.pushButton_4.clicked.connect(self.remove_selected_places)
#         self.pushButton_5.clicked.connect(self.search_choose_selected_places)
#
#     def add_user_history_search(self):
#         self.listWidget_2.addItem(self.full_adress)
#         self.connection.cursor().execute(
#             f"""INSERT INTO search_history (id, history, coords) VALUES ({self.id},'{self.full_adress}','{self.toponym_longitude},{self.toponym_lattitude}')""")
#         self.connection.commit()
#
#
#     def add_selected_places(self):
#         self.listWidget.addItem(self.textEdit_2.toPlainText())
#         self.connection.cursor().execute(
#             f"""UPDATE search_history SET name = '{self.textEdit_2.toPlainText()}'
#             WHERE history = '{self.full_adress}' and id = {self.id}""")
#         self.connection.commit()
#
#
#
#     def add_all_user_selected_places(self):
#         try:
#             users_selected_places = (self.connection.cursor().execute(f"""SELECT name, coords FROM search_history
#                                         WHERE id = {self.id} """).fetchall())
#             for name, coords in users_selected_places:
#                 self.dict_users_selected_places[name] = coords
#             self.listWidget.addItems(list(self.dict_users_selected_places.keys()))
#         except:
#             print('Нет избранных мест')
#
#     def search_choose_selected_places(self):
#         self.toponym_longitude, self.toponym_lattitude = self.dict_users_selected_places[(self.listWidget.selectedItems())[0].text()].split(',')
#         self.checkpoint.append(f"{self.toponym_longitude},{self.toponym_lattitude},ya_ru")
#         self.pixmap = QPixmap(
#             get_image(self.toponym_longitude, self.toponym_lattitude, self.size, self.type_map, self.checkpoint))
#         self.label.setPixmap(self.pixmap)
#         self.checkpoint = []
#
#
#
#
#
#     def remove_selected_places(self):
#         self.connection.cursor().execute(
#             f""" DELETE FROM search_history WHERE name = '{(self.listWidget.selectedItems())[0].text()}' and id = {self.id} """)
#         self.listWidget.selectedItems()
#         self.connection.commit()
#         for item in self.listWidget.selectedItems():
#             row = self.listWidget.row(item)  # Получаем индекс строки элемента
#             self.listWidget.takeItem(row)
#
#
#
#
#
#
#     def remove_checkpoint(self):
#         self.checkpoint = ['']
#         self.pull_image()
#         self.checkpoint = []
#         self.textBrowser.clear()
#         self.textBrowser_2.clear()
#         self.textBrowser_3.clear()
#     def pull_image(self, flag=False):
#         if widget := self.focusWidget():
#             widget.clearFocus()
#         if not flag:
#             self.get_coords()
#         if self.is_valid_coordinate(self.toponym_longitude, self.toponym_lattitude):
#             self.pixmap = QPixmap(get_image(self.toponym_longitude, self.toponym_lattitude, self.size, self.type_map, self.checkpoint))
#             self.label.setPixmap(self.pixmap)
#         else:
#             self.textEdit.setText("Некорректные координаты.")
#     def on_combobox_changed(self, index):
#         self.type_map = self.map_layers[index]
#     def mouseMoveEvent(self, event):
#
#         start_x, start_y = 380, 365
#         step_x, step_y = 0.00001913, 0.00001209
#         step_x, step_y = 0.00001843, 0.00001179
#         print(f'{event.x(), event.y()}')
#         if (int(event.x()) < 45 or int(event.x()) > 615) or (int(event.y()) < 196 or int(event.y()) > 530):
#             self.textBrowser_2.setText('вышли за границы')
#         else:
#             if event.x() < start_x:
#                 self.new_x = abs(start_x - event.x())
#                 self.point_x = str(float(self.toponym_longitude) - round((self.new_x * step_x), 4))
#             elif event.x() > start_x:
#                 self.new_x = abs(event.x() - start_x)
#                 self.point_x = str(float(self.toponym_longitude) + round((self.new_x * step_x), 4))
#             if event.y() < start_y:
#                 self.new_y = abs(start_y - event.y())
#                 self.point_y = str(float(self.toponym_lattitude) + round((self.new_y * step_y), 4))
#             elif event.y() > start_y:
#                 self.new_y = abs(event.y()-start_y)
#                 self.point_y = str(float(self.toponym_lattitude) - round((self.new_y * step_y), 4))
#             print(self.point_x, self.point_y)
#             self.checkpoint.clear()
#             self.checkpoint.append(f"{self.point_x},{self.point_y},ya_ru")
#             self.new_x = 0
#             self.new_y = 0
#             self.pull_responce_info()
#             self.pull_image(flag=True)
#             try:
#                 self.full_adress, self.adress_index = get_adress(self.point_x,self.point_y)
#             except:
#                 self.full_adress = get_adress(self.point_x, self.point_y)
#             self.pull_responce_info()
#             self.info_organization = get_organization(self.full_adress, self.point_x,self.point_y)
#             self.textBrowser_3.setText(self.info_organization)
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     login_window = LoginWindow()
#     if login_window.exec_() == QDialog.Accepted:
#         # Если авторизация успешна - показываем главное окно
#         state = AppState()
#         db = DataBase()
#         main_window = MyMainWindow()
#         main_window.show()
#         sys.exit(app.exec_())
#     else:
#         sys.exit(app.exec())



