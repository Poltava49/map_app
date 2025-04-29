from src.api_func import geocoder
from PyQt5.QtCore import Qt
from src.db import DataBase
from src.models import SearchHistory
from src.api_func import get_adress, get_organization, get_image


class BaseLogic:

    def __init__(self, db: DataBase, login_window) -> None:
        self.db = db
        self.user_login = login_window.get_user_login()
        self.user_id = self.db.get_user_id(self.user_login)

    def is_valid_coordinate(self, lat, lon):
        return (-90 <= float(lat) <= 90) and (-180 <= float(lon) <= 180)

    def get_coords(self, user_request):
        try:
            (
                self.toponym_longitude,
                self.toponym_lattitude,
                self.full_adress,
                self.adress_index,
            ) = geocoder(user_request)
            print(
                f"Прошел - {self.toponym_longitude, self.toponym_lattitude, self.full_adress, self.adress_index}"
            )
            return (
                self.toponym_longitude,
                self.toponym_lattitude,
                self.full_adress,
                self.adress_index,
            )
        except Exception as e:
            print(f" Ошибка. Некорректный ввод адреса {e}")

    def get_map_image(self, lon, lat, size, type, checkpoint):
        return get_image(lon, lat, size, type, checkpoint)

    def add_in_db_user_history(self, search_history: SearchHistory, user_login):
        self.user_id = self.db.get_user_id(user_login)
        self.db.add_user_history_search(
            SearchHistory(
                full_adress=self.full_adress,
                toponym_longitude=self.toponym_longitude,
                toponym_lattitude=self.toponym_lattitude,
                adress_index=self.adress_index,
            ),
            user_id=self.user_id,
        )

    def remove_selected_places(self, select_item):
        try:
            self.db.remove_selected_places(select_item)
        except Exception as e:
            print(f"Ошибка - {e}")

    def add_selected_places(self, full_adress, name):
        try:
            self.db.add_selected_places(full_adress, name, self.user_id)
        except Exception as e:
            print(f"Ошибка - {e}")

    def get_organization_info(self, adress, long, lat):
        return get_organization(adress, long, lat)
