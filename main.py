import sys
from PyQt5.Qt import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from api_func import geocoder, get_image


class MapImage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.textEdit.setPlaceholderText("Введите адрес здесь...")
        self.pushButton.clicked.connect(self.pull_image)


    def pull_image(self):
        self.pixmap = QPixmap(get_image(*geocoder(self.textEdit.toPlainText()), size=0.1))
        self.label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapImage()
    ex.show()
    sys.exit(app.exec())