from main_window import MyMainWindow
import sqlite3
main_window = MyMainWindow()
class DataBase:
    def __init__(self,login):
        super().__init__()
        self.current_user_login = login
        self.dict_users_selected_places = {}
        self.connection = sqlite3.connect("map_users_db.sqlite")
        self.id = (self.connection.cursor().execute(
            f"""SELECT id FROM users WHERE login = ?""",(self.current_user_login,)).fetchall())[0][0]
        self.add_all_user_selected_places()


    def add_user_history_search(self):
        try:
            self.connection.cursor().execute(
                f"""INSERT INTO search_history (id, history, coords, index_adress) VALUES (?,?,?,?)""", (self.id,self.state.full_adress,f'{self.state.toponym_longitude},{self.state.toponym_lattitude}', self.state.adress_index))
            self.connection.commit()
        except Exception as e:
            print(f"Ошибка - {e}. В базе есть история поиска по данному адресу")


    def add_selected_places(self, full_adress, name_place):
        self.connection.cursor().execute(
            f"""UPDATE search_history SET name = '{name_place}'
            WHERE history = ? and id = ?""",(full_adress, self.id))
        self.connection.commit()
        main_window.remove_selected_name()


    def add_all_user_selected_places(self):
        list_history = []
        try:
            users_selected_places = (self.connection.cursor().execute(f"""SELECT name, coords, history, index_adress FROM search_history 
                                        WHERE id = ?""", (self.id,)).fetchall())
            for name, coords, history, self.index in users_selected_places:
                self.dict_users_selected_places[name] = coords
                list_history.append(history)
            main_window.add_users_seleced_places(list(self.dict_users_selected_places.keys()))
            main_window.add_user_list_history(list_history)
        except Exception as e:
            print(f'Ошибка - {e}. Нет избранных мест')


    def remove_selected_places(self, select_item):
        self.connection.cursor().execute(
            f""" DELETE FROM search_history WHERE name = ? and id = ?""", (select_item, self.id))
        self.connection.commit()
