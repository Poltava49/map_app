from PyQt5.Qt import QMainWindow, QPixmap
from PyQt5 import uic
from api_func import get_image
from models import SearchHistory

from app import *


class MyMainWindow(QMainWindow):
    def __init__(self, logic) -> None:
        super().__init__()
        self.initUI()
        self.app_logic = logic

    def initUI(self) -> None:
        uic.loadUi('../ui_files/interface.ui', self)
        self.setMouseTracking(True)
        self.map_layers = ['map', 'sat', 'sat,skl']
        self.comboBox.addItems(['схема', 'спутник', 'гибрид'])
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.textEdit.setPlaceholderText("Введите адрес здесь...")
        self.pushButton.clicked.connect(self.pull_image)
        self.comboBox.currentIndexChanged.connect(self.pull_image)
        self.pushButton_2.clicked.connect(self.remove_checkpoint)
        self.checkBox.stateChanged.connect(self.pull_responce_info)
        self.pushButton_5.clicked.connect(self.search_choose_selected_places)
        self.pushButton_4.clicked.connect(self.remove_selected_places)
        self.pushButton_3.clicked.connect(self.add_selected_places)

    def get_adress(self):
        self.toponym_longitude, self.toponym_lattitude, self.full_adress, self.adress_index = (
        self.app_logic.get_coords(
            self.textEdit.toPlainText()))
        self.add_checkpoint(self.toponym_longitude, self.toponym_lattitude)

    def add_checkpoint(self, lon, lat):
        self.checkpoint.append(f"{lon},{lat},ya_ru")

    def add_selected_places(self):
        if not self.textEdit_2.toPlainText() == '' or self.full_adress == '':
            self.listWidget.addItem(self.textEdit_2.toPlainText())
            self.listWidget_2.addItem(self.state.full_adress)
            self.app_logic.add_selected_places(self.full_adress, self.textEdit_2.toPlainText())

    def add_users_seleced_places(self, names: list):
        self.listWidget.addItems(names)

    def add_user_list_history(self, list_history):
        self.listWidget_2.addItems(list_history)

    def remove_selected_name(self):
        self.textEdit_2.clear()

    def remove_selected_places(self):
        try:
            select_item = self.listWidget.currentItem().text()
            for item in self.listWidget.selectedItems():
                row = self.listWidget.row(item)  # Получаем индекс строки элемента
                self.listWidget.takeItem(row)
            self.app_logic.remove_selected_places(select_item)
        except Exception as e:
            print(f'Ошибка - {e}. Нет избранных мест')

    def search_choose_selected_places(self):
        try:
            if self.listWidget.selectedItems()[0].text().split(',') != '':
                self.toponym_longitude, self.toponym_lattitude = self.db.dict_users_selected_places
                self.state.checkpoint.append(f"{self.state.toponym_longitude},{self.state.toponym_lattitude},ya_ru")
            else:
                if not self.textEdit_2.toPlainText() == '':
                    self.listWidget.addItem(self.textEdit_2.toPlainText())
            self.pixmap = QPixmap(
                get_image(self.state.toponym_longitude, self.state.toponym_lattitude, self.state.size,
                          self.state.type_map, self.state.checkpoint))
            self.label.setPixmap(self.pixmap)
            self.pull_responce_info()
            self.state.checkpoint = []
        except Exception as e:
            print(f'Ошибка - {e}. Нет избранных мест')

    def pull_image(self, flag=False):
        if widget := self.focusWidget():
            widget.clearFocus()
        if not flag:
            self.get_adress()
        if self.app_logic.is_valid_coordinate(self.toponym_longitude, self.toponym_lattitude):
            self.pixmap = QPixmap(get_image(self.toponym_longitude, self.toponym_lattitude, self.size,
                                            self.type_map, self.checkpoint))
            self.label.setPixmap(self.pixmap)
        else:
            self.textEdit.setText("Некорректные координаты.")

    def remove_checkpoint(self):
        self.state.checkpoint = ['']
        self.pull_image()
        self.state.checkpoint = []
        self.textBrowser.clear()
        self.textBrowser_3.clear()

    def pull_responce_info(self, state=1):
        try:
            if state == 2:
                self.textBrowser.setText(f'{self.state.full_adress} {self.state.adress_index}')
            else:
                self.textBrowser.setText(f'{self.state.full_adress}')
        except:
            print("Нет полного адреса")

    def on_combobox_changed(self, index):
        self.state.type_map = self.map_layers[index]

    def keyPressEvent(self, event):
        x = 0.015
        if event.key() == Qt.Key_Up and self.state.size >= 0.011:
            self.state.size -= x * 2
            self.main_window.pull_image()

        elif event.key() == Qt.Key_Down:
            self.state.size += x * 2
            self.main_window.pull_image(flag=True)
        elif event.key() == Qt.Key_D:
            self.state.toponym_longitude = str(float(self.state.toponym_longitude) + self.state.step)
            self.main_window.pull_image(flag=True)
        elif event.key() == Qt.Key_A:
            self.state.toponym_longitude = str(float(self.state.toponym_longitude) - self.state.step)
            self.main_window.pull_image(flag=True)
        elif event.key() == Qt.Key_S:
            self.state.toponym_lattitude = str(float(self.state.state.toponym_lattitude) - self.state.step)
            self.main_window.pull_image(flag=True)
        elif event.key() == Qt.Key_W:
            self.state.toponym_lattitude = str(float(self.state.toponym_lattitude) + self.state.step)
            self.main_window.pull_image(flag=True)

    def mouseMoveEvent(self, event):
        start_x, start_y = 380, 365
        step_x, step_y = 0.00001843, 0.00001179

        if (int(event.x()) < 18 or int(event.x()) > 595) or (int(event.y()) < 190 or int(event.y()) > 500):
            print('вышли за границы')
        else:
            if event.x() < start_x:
                self.state.new_x = abs(start_x - event.x())
                self.state.point_x = str(float(self.state.toponym_longitude) - round((self.state.new_x * step_x), 4))
            elif event.x() > start_x:
                self.state.new_x = abs(event.x() - start_x)
                self.state.point_x = str(float(self.state.toponym_longitude) + round((self.state.new_x * step_x), 4))
            if event.y() < start_y:
                self.state.new_y = abs(start_y - event.y())
                self.state.point_y = str(float(self.state.toponym_lattitude) + round((self.state.new_y * step_y), 4))
            elif event.y() > start_y:
                self.state.new_y = abs(event.y() - start_y)
                self.state.point_y = str(float(self.state.toponym_lattitude) - round((self.state.new_y * step_y), 4))

            self.state.checkpoint.clear()
            self.state.checkpoint.append(f"{self.state.point_x},{self.state.point_y},ya_ru")
            self.state.new_x = 0
            self.state.new_y = 0
            self.main_window.pull_image(flag=True)
            try:
                self.state.full_adress, self.state.adress_index = get_adress(self.state.point_x, self.state.point_y)
            except:
                self.state.full_adress = get_adress(self.state.point_x, self.state.point_y)
            self.main_window.pull_responce_info()
            self.state.info_organization = get_organization(self.state.full_adress, self.state.point_x,
                                                            self.state.point_y)
            self.main_window.textBrowser_3.setText(self.state.info_organization)
