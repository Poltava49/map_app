import sys
from PyQt5.Qt import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from api_func import geocoder, get_image
from PyQt5.QtCore import Qt

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.size = 0.1
        self.step = 0.001
        self.type_map = 'map'
        self.map_layers = ['map', 'sat', 'sat,skl']
        self.comboBox.addItems(['схема','спутник','гибрид'])
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.textEdit.setPlaceholderText("Введите адрес здесь...")
        self.pushButton.clicked.connect(self.pull_image)


    def keyPressEvent(self, event):
        x = 0.015
        if event.key() == Qt.Key_Up and self.size >= 0.011:
            self.size -= x * 2
            self.pull_image()
        elif event.key() == Qt.Key_Down:
            self.size += x * 2
        elif event.key() == Qt.Key_D:
            self.toponym_longitude = str(float(self.toponym_longitude) + self.step)
        elif event.key() == Qt.Key_A:
            self.toponym_longitude = str(float(self.toponym_longitude) - self.step)
        elif event.key() == Qt.Key_S:
            self.toponym_lattitude = str(float(self.toponym_lattitude) - self.step)
        elif event.key() == Qt.Key_W:
            self.toponym_lattitude = str(float(self.toponym_lattitude) + self.step)
        else:
            super().keyPressEvent(event)
        self.pull_image(flag=True)

    def is_valid_coordinate(self, lat, lon):
        return (-90 <= float(lat) <= 90) and (-180 <= float(lon) <= 180)

    def get_coords(self):
        self.toponym_longitude, self.toponym_lattitude = geocoder(self.textEdit.toPlainText())



    def pull_image(self, flag=False):
        if widget := self.focusWidget():
            widget.clearFocus()

        if not flag:
            self.get_coords()
        if self.is_valid_coordinate(self.toponym_longitude, self.toponym_lattitude):
            self.pixmap = QPixmap(get_image(self.toponym_longitude, self.toponym_lattitude, self.size, self.type_map))
            self.label.setPixmap(self.pixmap)
        else:
            self.textEdit.setText("Некорректные координаты.")


    def on_combobox_changed(self, index):
        self.type_map = self.map_layers[index]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    ex.show()
    sys.exit(app.exec())