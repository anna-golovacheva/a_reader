from typing import Any
from data import DBConnect
from settings import db

class User:
    table_name = 'users'

    pk = 0
    user_name = ''
    is_active = True
    wins_num = 0

    def __init__(self, pk, user_name, is_active, wins_num):
        self.pk = pk
        self.user_name = user_name
        self.is_active = is_active
        self.wins_num = wins_num

    def __setattr__(self, key: str, value: Any) -> None:
        if key in User.__dict__ and key not in ('pk', 'table_name'):
            self.__dict__[key] = value
            dbase = DBConnect(db)
            dbase.set_field(User.table_name, self.pk, key, value)
        else:
            super().__setattr__(key, value)

    @staticmethod
    def get_object(search: dict[str, str]):
        dbase = DBConnect(db)
        data_list = dbase.get_objects(User.table_name, search=search)
        if len(data_list) >= 1:
            object = User(*list(data_list[0].values()))
            return object

    @staticmethod
    def get_objects(search: dict[str, str]):
        dbase = DBConnect(db)
        data_list = dbase.get_objects(User.table_name, search)
        if len(data_list) >= 1:
            object_list = [User(*list(data.values())) for data in data_list]
            return object_list

    @staticmethod
    def create(user_name):
        dbase = DBConnect(db)
        pk = dbase.create_object(User.table_name, ['user_name',], [user_name])
        return User.get_object({'id': pk})

    @staticmethod
    def delete(delete: dict[str, str]):
        dbase = DBConnect(db)
        dbase.delete_objects(User.table_name, delete)

    def __repr__(self):
        return f'User_{self.pk}_{self.user_name}'
