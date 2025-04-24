import sqlite3
import os
from models import SearchHistory, UserAttributes


class DataBase:
    def __init__(self) -> None:
        self.init_db()
        self.connection = sqlite3.connect("../db/map_users_db.sqlite")


    def init_db(self):
        """Создаем базу при инициализации"""
        path_db = "../db/map_users_db.sqlite"

        if not os.path.exists(path_db):
            print("База данных не найдена, создаем новую")

        connect = sqlite3.connect(path_db)
        cursor = connect.cursor()

        try:
            with open('../db/schema.sql') as sql_file:
                sql_script = sql_file.read()
                cursor.executescript(sql_script)
            print("База успешно создана")
        except Exception as e:
            print(f"Ошибка {e}")
        finally:
            connect.commit()
            connect.close()

    def check_user_by_login(self, login):
        try:
            self.connection.cursor().execute(f"""SELECT login FROM users WHERE login = '?'""", (login,)).fetchall()
            return True
        except:
            return False

    def validation_user_enter(self, login, password):
        try:
            res = self.connection.cursor().execute(f"""SELECT ?, ? FROM users""", (login, password)).fetchall()

            return res
        except Exception as e:
            return False

    def add_new_user(self, user_attr: UserAttributes):
        self.connection.cursor().execute(
            f"""INSERT INTO users (name,login,password) VALUES (?,?,?)""", (user_attr.name, user_attr.login, user_attr.password)).fetchall()
        self.connection.commit()
        self.connection.close()
        return True

    def add_user_history_search(self, search_history: SearchHistory, user_id):
        full_adress, toponym_longitude, toponym_lattitude, adress_index = search_history
        try:
            self.connection.cursor().execute(
                f"""INSERT INTO search_history (id, history, coords, index_adress) VALUES (?,?,?,?)""", (
                    user_id, full_adress, toponym_longitude, toponym_lattitude, adress_index))
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print(f"Ошибка - {e}. В базе есть история поиска по данному адресу")

    def add_selected_places(self, full_adress, name_place, user_id):
        self.connection.cursor().execute(
            f"""UPDATE search_history SET name = '{name_place}'
            WHERE history = ? and id = ?""", (full_adress, self.user_id))
        self.connection.commit()
        self.connection.close()

    def add_all_user_selected_places(self, user_id):
        list_history = []
        try:
            users_selected_places = (self.connection.cursor().execute(f"""SELECT name, coords, history, index_adress FROM search_history 
                                        WHERE id = ?""", (user_id,)).fetchall())
            return users_selected_places
            # for name, coords, history, self.index in users_selected_places:
            #     self.dict_users_selected_places[name] = coords
            #     list_history.append(history)
        except Exception as e:
            print(f'Ошибка - {e}. Нет избранных мест')

    def remove_selected_places(self, select_item):
        self.connection.cursor().execute(
            f""" DELETE FROM search_history WHERE name = ? and id = ?""", (select_item, self.id))
        self.connection.commit()
        self.connection.close()
