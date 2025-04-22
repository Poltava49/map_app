from api_func import geocoder
from PyQt5.QtCore import Qt
from models import AppState
from api_func import get_adress, get_organization



class BaseLogic:

    def __init__(self, db, login_window) -> None:
        self.db = db
        self.user_login = login_window.get_user_login()


    def is_valid_coordinate(self, lat, lon):
        return (-90 <= float(lat) <= 90) and (-180 <= float(lon) <= 180)


    def get_coords(self):
        try:
            self.toponym_longitude, self.toponym_lattitude, self.full_adress, self.adress_index = geocoder(self.textEdit.toPlainText())
        except:
            if not self.textEdit.toPlainText() == '':
                self.toponym_longitude, self.toponym_lattitude, self.full_adress, self.adress_index = geocoder(self.textEdit.toPlainText())

        self.checkpoint.append(f"{self.toponym_longitude},{self.toponym_lattitude},ya_ru")
        self.db.add_user_history_search(self.full_adress, self.toponym_longitude,  self.toponym_lattitude, self.adress_index)


