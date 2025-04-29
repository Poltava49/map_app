import sqlite3
import os
import config
from models import SearchHistory, UserAttributes


class DataBase:
    def __init__(self, db_file_path: str = config.DB_FILE_PATH) -> None:
        self.init_db()
        self.connection = sqlite3.connect(db_file_path)

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
            # connect.close()

    def check_user_by_login(self, login):
        try:
            self.connection.cursor().execute(f"""SELECT login FROM users WHERE login = '?'""", (login,)).fetchall()
            self.connection.commit()
            return True
        except:
            return False

    def validation_user_enter(self, login, password):
        try:
            res = self.connection.cursor().execute(f"""SELECT login, password FROM users WHERE login = ? and password = ?""", (login, password)).fetchall()
            self.connection.commit()
            return res
        except Exception as e:
            print(f"Ошибка - {e}")
            return False



    def add_new_user(self, user_attr: UserAttributes):
        self.connection.cursor().execute(
            f"""INSERT INTO users (name,login,password) VALUES (?,?,?)""", (user_attr.name, user_attr.login, user_attr.password)).fetchall()
        self.connection.commit()
        # self.connection.close()
        return True

    def add_user_history_search(self, search_history: SearchHistory, user_id):
        try:
            self.connection.cursor().execute(
                f"""INSERT INTO search_history (user_id, history, coords) VALUES (?,?,?)""", (
                    user_id, search_history.full_adress, f"{search_history.toponym_longitude}, {search_history.toponym_lattitude}"))
            self.connection.commit()
            print("Успех")
        except Exception as e:
            print(f"Ошибка - {e}. В базе есть история поиска по данному адресу")

    def get_user_id(self, user_login):
        user_id = self.connection.cursor().execute(
            f"""SELECT user_id FROM users WHERE login = ?""", (
                user_login, )).fetchone()

        print(f"type - {type(user_id)}, user_id - {user_id}")
        self.connection.commit()
        # self.connection.close()
        return str(user_id)


    def add_selected_places(self, full_adress, name_place, user_id):
        self.connection.cursor().execute(
            f"""UPDATE search_history SET name = '{name_place}'
            WHERE history = ? and user_id = ?""", (full_adress, user_id))
        self.connection.commit()
        # self.connection.close()

    def add_all_user_selected_places(self, user_id):
        list_history = []
        try:
            users_selected_places = (self.connection.cursor().execute(f"""SELECT name, coords, history, index_adress FROM search_history 
                                        WHERE user_id = ?""", (user_id,)).fetchall())
            return users_selected_places
            # for name, coords, history, self.index in users_selected_places:
            #     self.dict_users_selected_places[name] = coords
            #     list_history.append(history)
        except Exception as e:
            print(f'Ошибка - {e}. Нет избранных мест')

    def remove_selected_places(self, select_item):
        self.connection.cursor().execute(
            f""" DELETE FROM search_history WHERE name = ? and user_id = ?""", (select_item, self.id))
        self.connection.commit()
        # self.connection.close()

    def get_cache(self, url, params):
        list_history = []
        try:
            users_selected_places = (self.connection.cursor().execute(f"""SELECT name, coords, history, index_adress FROM search_history 
                                        WHERE user_id = ?""", (user_id,)).fetchall())
            return users_selected_places
            # for name, coords, history, self.index in users_selected_places:
            #     self.dict_users_selected_places[name] = coords
            #     list_history.append(history)
        except Exception as e:
            print(f'Ошибка - {e}. Нет избранных мест')
