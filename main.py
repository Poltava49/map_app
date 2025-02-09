import sys
from PyQt5.Qt import QMainWindow, QApplication, Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from api_func import geocoder, get_image

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.size = 0.1
        self.textEdit.setPlaceholderText("Введите адрес здесь...")
        self.pushButton.clicked.connect(self.pull_image)


    def keyPressEvent(self, event):
        x = 0.015
        if event.key() == Qt.Key_Up and self.size >= 0.011:
            self.size -= x * 2
            self.pull_image()
        elif event.key() == Qt.Key_Down:
            self.size += x * 2
            self.pull_image()
        else:
            super().keyPressEvent(event)



    def pull_image(self):
        if widget := self.focusWidget():
            widget.clearFocus()
        self.pixmap = QPixmap(get_image(*geocoder(self.textEdit.toPlainText()), self.size))
        self.label.setPixmap(self.pixmap)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    ex.show()
    sys.exit(app.exec())