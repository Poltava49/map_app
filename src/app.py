from main_window import MyMainWindow
from db import DataBase
from api_func import geocoder
from PyQt5.QtCore import Qt
from models import AppState
from api_func import get_adress, get_organization


main_window = MyMainWindow()
db = DataBase()
state = AppState()


class BaseLogic:
    def is_valid_coordinate(self, lat, lon):
        return (-90 <= float(lat) <= 90) and (-180 <= float(lon) <= 180)


    def get_coords(self):
        try:
            main_window.toponym_longitude, main_window.toponym_lattitude, main_window.full_adress, main_window.adress_index = geocoder(main_window.textEdit.toPlainText())
        except:
            if not main_window.textEdit.toPlainText() == '':
                main_window.state.toponym_longitude, main_window.toponym_lattitude, main_window.full_adress, main_window.adress_index = geocoder(main_window.textEdit.toPlainText())

        main_window.checkpoint.append(f"{main_window.toponym_longitude},{main_window.toponym_lattitude},ya_ru")
        main_window.pull_responce_info()
        db.add_user_history_search()


    def keyPressEvent(self, event):
        x = 0.015
        if event.key() == Qt.Key_Up and main_window.size >= 0.011:
            main_window.size -= x * 2
            main_window.pull_image()
        elif event.key() == Qt.Key_Down:
            main_window.size += x * 2
            main_window.pull_image(flag=True)
        elif event.key() == Qt.Key_D:
            main_window.toponym_longitude = str(float(main_window.toponym_longitude) + main_window.step)
            main_window.pull_image(flag=True)
        elif event.key() == Qt.Key_A:
            main_window.toponym_longitude = str(float(main_window.toponym_longitude) - main_window.step)
            main_window.pull_image(flag=True)
        elif event.key() == Qt.Key_S:
            main_window.toponym_lattitude = str(float(main_window.state.toponym_lattitude) - main_window.step)
            main_window.pull_image(flag=True)
        elif event.key() == Qt.Key_W:
            main_window.toponym_lattitude = str(float(main_window.toponym_lattitude) + main_window.step)
            main_window.pull_image(flag=True)

    def mouseMoveEvent(self, event):
        start_x, start_y = 380, 365
        step_x, step_y = 0.00001843, 0.00001179

        if (int(event.x()) < 18 or int(event.x()) > 595) or (int(event.y()) < 190 or int(event.y()) > 500):
            print('вышли за границы')
        else:
            if event.x() < start_x:
                state.new_x = abs(start_x - event.x())
                state.point_x = str(float(state.toponym_longitude) - round((state.new_x * step_x), 4))
            elif event.x() > start_x:
                state.new_x = abs(event.x() - start_x)
                state.point_x = str(float(state.toponym_longitude) + round((state.new_x * step_x), 4))
            if event.y() < start_y:
                state.new_y = abs(start_y - event.y())
                state.point_y = str(float(state.toponym_lattitude) + round((state.new_y * step_y), 4))
            elif event.y() > start_y:
                state.new_y = abs(event.y()-start_y)
                state.point_y = str(float(state.toponym_lattitude) - round((state.new_y * step_y), 4))

            state.checkpoint.clear()
            state.checkpoint.append(f"{state.point_x},{state.point_y},ya_ru")
            state.new_x = 0
            state.new_y = 0
            main_window.pull_image(flag=True)
            try:
                state.full_adress, state.adress_index = get_adress(state.point_x, state.point_y)
            except:
                state.full_adress = get_adress(state.point_x, state.point_y)
            main_window.pull_responce_info()
            state.info_organization = get_organization(state.full_adress, state.point_x, state.point_y)
            main_window.textBrowser_3.setText(state.info_organization)