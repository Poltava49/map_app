from PyQt5.Qt import QMainWindow, QPixmap
from PyQt5 import uic
from api_func import get_image
from models import AppState





class MyMainWindow(QMainWindow):
    def __init__(self,db) -> None:
        super().__init__()
        state = AppState()
        self.initUI()
        self.db =db
        self.state = state
        self.logic = logic
    def initUI(self) -> None:
        uic.loadUi('ui_files/interface.ui', self)
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

    def add_selected_places(self):
        if not self.textEdit_2.toPlainText() == '' or self.state.full_adress == '':
            self.listWidget.addItem(self.textEdit_2.toPlainText())
            self.listWidget_2.addItem(self.state.full_adress)
            self.db.add_selected_places(self.full_adress, self.textEdit_2.toPlainText())


    def add_users_seleced_places(self, names:list):
        self.listWidget.addItems(names)


    def add_user_list_history(self,list_history):
        self.listWidget_2.addItems(list_history)


    def remove_selected_name(self):
        self.textEdit_2.clear()


    def remove_selected_places(self):
        try:
            select_item = self.listWidget.currentItem().text()
            for item in self.listWidget.selectedItems():
                row = self.listWidget.row(item)  # Получаем индекс строки элемента
                self.listWidget.takeItem(row)
            self.db.remove_selected_places(select_item)
        except Exception as e:
            print(f'Ошибка - {e}. Нет избранных мест')


    def search_choose_selected_places(self):
        try:
            if self.listWidget.selectedItems()[0].text().split(',') != '':
                self.state.toponym_longitude, self.state.toponym_lattitude = self.db.dict_users_selected_places
                self.state.checkpoint.append(f"{self.state.toponym_longitude},{self.state.toponym_lattitude},ya_ru")
            else:
                if not self.textEdit_2.toPlainText() == '':
                    self.listWidget.addItem(self.textEdit_2.toPlainText())
            self.pixmap = QPixmap(
                get_image(self.state.toponym_longitude, self.state.toponym_lattitude, self.state.size, self.state.type_map, self.state.checkpoint))
            self.label.setPixmap(self.pixmap)
            self.pull_responce_info()
            self.state.checkpoint = []
        except Exception as e:
            print(f'Ошибка - {e}. Нет избранных мест')


    def pull_image(self, flag=False):
        if widget := self.focusWidget():
            widget.clearFocus()
        if not flag:
            self.get_coords()
        if self.logic.is_valid_coordinate(self.state.toponym_longitude, self.state.toponym_lattitude):
            self.pixmap = QPixmap(get_image(self.state.toponym_longitude, self.state.toponym_lattitude, self.state.size,
                                            self.state.type_map, self.state.checkpoint))
            self.label.setPixmap(self.pixmap)
        else:
            self.textEdit.setText("Некорректные координаты.")


    def remove_checkpoint(self):
        self.state.checkpoint = ['']
        self.pull_image()
        self.state.checkpoint = []
        self.textBrowser.clear()
        self.textBrowser_3.clear()


    def pull_responce_info(self,state=1):
        try:
            if state == 2:
                self.textBrowser.setText(f'{self.state.full_adress} {self.state.adress_index}')
            else:
                self.textBrowser.setText(f'{self.state.full_adress}')
        except:
            print("Нет полного адреса")

    def on_combobox_changed(self, index):
        self.state.type_map = self.map_layers[index]


