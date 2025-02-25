import sys
from PyQt5.Qt import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from api_func import geocoder, get_image, get_adress, get_organization
from PyQt5.QtCore import Qt

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.size = 0.003
        self.step = 0.0001
        self.type_map = 'map'
        self.new_x = 0
        self.new_y = 0
        self.checkpoint = []
        self.label_2 = ''
        self.point_x = 0
        self.point_y = 0
        self.info_organization = ''
        self.setMouseTracking(True)
        self.map_layers = ['map', 'sat', 'sat,skl']
        self.comboBox.addItems(['схема','спутник','гибрид'])
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.textEdit.setPlaceholderText("Введите адрес здесь...")
        self.pushButton.clicked.connect(self.pull_image)
        self.comboBox.currentIndexChanged.connect(self.pull_image)
        self.pushButton_2.clicked.connect(self.remove_checkpoint)
        self.checkBox.stateChanged.connect(self.pull_responce_info)


    def keyPressEvent(self, event):
        x = 0.015
        if event.key() == Qt.Key_Up and self.size >= 0.011:
            self.size -= x * 2
            self.pull_image()
        elif event.key() == Qt.Key_Down:
            self.size += x * 2
            self.pull_image(flag=True)
        elif event.key() == Qt.Key_D:
            self.toponym_longitude = str(float(self.toponym_longitude) + self.step)
            self.pull_image(flag=True)
        elif event.key() == Qt.Key_A:
            self.toponym_longitude = str(float(self.toponym_longitude) - self.step)
            self.pull_image(flag=True)
        elif event.key() == Qt.Key_S:
            self.toponym_lattitude = str(float(self.toponym_lattitude) - self.step)
            self.pull_image(flag=True)
        elif event.key() == Qt.Key_W:
            self.toponym_lattitude = str(float(self.toponym_lattitude) + self.step)
            self.pull_image(flag=True)
        else:
            super().keyPressEvent(event)


    def is_valid_coordinate(self, lat, lon):
        return (-90 <= float(lat) <= 90) and (-180 <= float(lon) <= 180)


    def get_coords(self):
        try:
            self.toponym_longitude, self.toponym_lattitude, self.full_adress, self.adress_index = geocoder(self.textEdit.toPlainText())
        except:
            self.toponym_longitude, self.toponym_lattitude, self.full_adress = geocoder(self.textEdit.toPlainText())
        self.checkpoint.append(f"{self.toponym_longitude},{self.toponym_lattitude},ya_ru")
        self.pull_responce_info()



    def pull_responce_info(self,state=1):
        if state == 2 :
            self.textBrowser.setText(f'{self.full_adress} {self.adress_index}')
        else:
            self.textBrowser.setText(f'{self.full_adress}')


    def remove_checkpoint(self):
        self.checkpoint = ['']
        self.pull_image()
        self.checkpoint = []
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()



    def pull_image(self, flag=False):
        if widget := self.focusWidget():
            widget.clearFocus()
        if not flag:
            self.get_coords()
        if self.is_valid_coordinate(self.toponym_longitude, self.toponym_lattitude):
            self.pixmap = QPixmap(get_image(self.toponym_longitude, self.toponym_lattitude, self.size, self.type_map, self.checkpoint))
            self.label.setPixmap(self.pixmap)
        else:
            self.textEdit.setText("Некорректные координаты.")


    def on_combobox_changed(self, index):
        self.type_map = self.map_layers[index]


    def mouseMoveEvent(self, event):

        start_x, start_y = 380, 365
        step_x, step_y = 0.00001913, 0.00001209
        print(f'{event.x(), event.y()}')
        if (int(event.x()) < 45 or int(event.x()) > 615) or (int(event.y()) < 196 or int(event.y()) > 530):
            self.textBrowser_2.setText('вышли за границы')
        else:
            if event.x() < start_x:
                self.new_x = abs(start_x - event.x())
                self.point_x = str(float(self.toponym_longitude) - round((self.new_x * step_x), 4))
            elif event.x() > start_x:
                self.new_x = abs(event.x() - start_x)
                self.point_x = str(float(self.toponym_longitude) + round((self.new_x * step_x), 4))
            if event.y() < start_y:
                self.new_y = abs(start_y - event.y())
                self.point_y = str(float(self.toponym_lattitude) + round((self.new_y * step_y), 4))
            elif event.y() > start_y:
                self.new_y = abs(event.y()-start_y)
                self.point_y = str(float(self.toponym_lattitude) - round((self.new_y * step_y), 4))
            print(self.point_x, self.point_y)
            self.checkpoint.clear()
            self.checkpoint.append(f"{self.point_x},{self.point_y},ya_ru")
            self.new_x = 0
            self.new_y = 0
            self.pull_responce_info()
            self.pull_image(flag=True)
            try:
                self.full_adress, self.adress_index = get_adress(self.point_x,self.point_y)
            except:
                self.full_adress = get_adress(self.point_x, self.point_y)

            self.pull_responce_info()
            self.info_organization = get_organization(self.full_adress, self.point_x,self.point_y)
            self.textBrowser_3.setText(self.info_organization)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    ex.show()
    sys.exit(app.exec())