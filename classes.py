from typing import Any
from dataclasses import dataclass

from data import DBConnect
from settings import db, table_name_1, table_name_2


@dataclass
class BaseClass:
    pk: int

    def __setattr__(self, key: str, value: Any) -> None:
        if key in self.__class__.__dict__ and key not in ('pk', 'table_name'):
            self.__dict__[key] = value
            dbase = DBConnect(db)
            dbase.set_field(self.__class__.table_name, self.pk, key, value)
        else:
            super().__setattr__(key, value)

    @classmethod
    def get_object(cls, search: dict[str, str]):
        dbase = DBConnect(db)
        data_list = dbase.get_objects(cls.table_name, search=search)
        if len(data_list) >= 1:
            object = cls(*list(data_list[0].values()))
            return object

    @classmethod
    def get_objects(cls, search: dict[str, str]):
        dbase = DBConnect(db)
        data_list = dbase.get_objects(cls.table_name, search)
        if len(data_list) >= 1:
            object_list = [cls(*list(data.values())) for data in data_list]
            return object_list

    @classmethod
    def delete(cls, delete: dict[str, str]):
        dbase = DBConnect(db)
        dbase.delete_objects(cls.table_name, delete)


@dataclass
class User(BaseClass):
    user_name: str = ''
    is_active: bool = True
    wins_num: int = 0

    table_name: str = table_name_1

    @classmethod
    def create(cls, user_name):
        dbase = DBConnect(db)
        pk = dbase.create_object(cls.table_name, ['user_name',], [user_name])
        return cls.get_object({'id': pk})

    def __repr__(self):
        return f'User_{self.pk}_{self.user_name}'


@dataclass
class Game(BaseClass):
    user_id: str = ''
    is_active: bool = True
    number: int = 0
    tries_num: int = 10
    is_win: bool = False

    table_name: str = table_name_2

    @classmethod
    def create(cls, user_id, number):
        dbase = DBConnect(db)
        pk = dbase.create_object(cls.table_name, ['user_id', 'number'], [user_id, number])
        return cls.get_object({'id': pk})

    def __repr__(self):
        return f'Game_{self.pk}_{self.user_id}'
