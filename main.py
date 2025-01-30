import requests
import sys
from PyQt5.Qt import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from random import uniform

class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.textEdit.setPlaceholderText("Введите адрес здесь...")
        self.mapImage = QLabel(self)
        self.mapImage.move(90, 120)
        self.mapImage.resize(400, 400)
        self.pushButton.clicked.connect(self.pull_image)



    def pull_image(self):
        self.pixmap = QPixmap(self.get_image(*self.geocoder(self.textEdit.toPlainText())))
        self.mapImage.setPixmap(self.pixmap)



    def geocoder(self, address):
        geocoder_params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                                "geocode": address,
                                "format": "json",
                                "kind": "district"
                                }
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            pass
        json_response = response.json()
        toponym_longitude, toponym_lattitude = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(' ')
        return toponym_longitude, toponym_lattitude


    def get_image(self, toponym_longitude, toponym_lattitude):
        self.size = uniform(0.0001, 0.05)
        params = {
            'll': f"{toponym_longitude},{toponym_lattitude}",
            'spn': f'{self.size},{self.size}',
            'size': '650,450',
            'l': 'map',
            'z': 5
        }
        url = 'https://static-maps.yandex.ru/1.x/?'
        response = requests.get(url, params)

        if response := requests.get(url, params=params):
            with open("picture.png", "wb") as file:
                file.write(response.content)
            return 'picture.png'
        else:
            return None




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())