from typing import Any
from dataclasses import dataclass

from data import DBConnect
from settings import DB, TABLE_NAME_1, TABLE_NAME_2


@dataclass
class BaseClass:
    pk: int

    def __setattr__(self, key: str, value: Any) -> None:
        if key in self.__class__.__dict__ and key not in ('pk', 'table_name'):
            self.__dict__[key] = value
            dbase = DBConnect(DB)
            dbase.set_field(self.__class__.table_name, self.pk, key, value)
        else:
            super().__setattr__(key, value)

    @classmethod
    def get_object(cls, search: dict[str, str | int | bool]):
        dbase = DBConnect(DB)
        data_list = dbase.get_objects(cls.table_name, search=search)
        if len(data_list) >= 1:
            object = cls(*list(data_list[0].values()))
            return object

    @classmethod
    def get_objects(cls, search: dict[str, str | int | bool]):
        dbase = DBConnect(DB)
        data_list = dbase.get_objects(cls.table_name, search)
        if len(data_list) >= 1:
            object_list = [cls(*list(data.values())) for data in data_list]
            return object_list

    @classmethod
    def get_all(cls):
        dbase = DBConnect(DB)
        data_list = dbase.get_objects(cls.table_name)
        if len(data_list) >= 1:
            object_list = [cls(*list(data.values())) for data in data_list]
            return object_list

    @classmethod
    def delete(cls, delete: dict[str, str]):
        dbase = DBConnect(DB)
        dbase.delete_objects(cls.table_name, delete)


@dataclass
class User(BaseClass):
    tg_id: int = 0
    user_name: str = ''
    is_active: bool = True
    wins_num: int = 0
    games_num: int = 0

    table_name: str = TABLE_NAME_1

    @classmethod
    def create(cls, user_name, tg_id):
        dbase = DBConnect(DB)
        pk = dbase.create_object(cls.table_name, ['user_name', 'tg_id'], [user_name, tg_id])
        return cls.get_object({'id': pk})

    def __repr__(self):
        return f'User_{self.pk}_{self.user_name}'

    @classmethod
    def get_or_create(cls, user_info):
        object = cls.get_object({'tg_id': user_info.id})
        if not object:
            object = User.create(user_info.username, user_info.id)
        return object


@dataclass
class Game(BaseClass):
    user_id: int = 0
    is_active: bool = True
    number: int = 0
    tries_num: int = 10
    is_win: bool = False

    table_name: str = TABLE_NAME_2

    @classmethod
    def create(cls, user_id, number):
        dbase = DBConnect(DB)
        pk = dbase.create_object(cls.table_name, ['user_id', 'number'], [user_id, number])
        return cls.get_object({'id': pk})

    def __repr__(self):
        return f'Game_{self.pk}_{self.user_id}'
