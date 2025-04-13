
from api_func import geocoder
from PyQt5.QtCore import Qt
from models import AppState
from api_func import get_adress, get_organization



class BaseLogic:

    def __init__(self, db, main_window) -> None:
        state = AppState()
        self.db = db
        self.state = state
        self.main_window = main_window



    def is_valid_coordinate(self, lat, lon):
        return (-90 <= float(lat) <= 90) and (-180 <= float(lon) <= 180)


    def get_coords(self):
        try:
            self.state.toponym_longitude, self.state.toponym_lattitude, self.state.full_adress, self.state.adress_index = geocoder(self.state.textEdit.toPlainText())
        except:
            if not self.state.textEdit.toPlainText() == '':
                self.state.state.toponym_longitude, self.state.toponym_lattitude, self.state.full_adress, self.state.adress_index = geocoder(self.state.textEdit.toPlainText())

        self.state.checkpoint.append(f"{self.state.toponym_longitude},{self.state.toponym_lattitude},ya_ru")
        self.main_window.pull_responce_info()
        self.db.add_user_history_search()


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
                self.state.new_y = abs(event.y()-start_y)
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
            self.state.info_organization = get_organization(self.state.full_adress, self.state.point_x, self.state.point_y)
            self.main_window.textBrowser_3.setText(self.state.info_organization)