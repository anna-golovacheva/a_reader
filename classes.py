from typing import Any
from data import DBConnect
from settings import db

class User:
    table_name = 'users'
    id_count = 0

    id = 0
    user_name = ''
    is_active = True
    wins_num = 0

    def __init__(self, name):
        print(User.id_count)

        self.id = self.__count_ids()
        print(self.id)
        self.user_name = name
        dbase = DBConnect(db)
        dbase.create_object(User.table_name, ['id', 'user_name',], [self.id, name])

    @classmethod
    def __count_ids(cls):
        print(cls.id_count)
        cls.id_count += 1
        print(cls.id_count)
        return cls.id_count

    def __setattr__(self, key: str, value: Any) -> None:
        print(key)
        print(value)
        print(User.__dict__)
        print(key in User.__dict__)
        if key in User.__dict__ and key != 'id':
            self.__dict__[key] = value
            dbase = DBConnect(db)
            dbase.set_field(User.table_name, self.id, key, value)
        else:
            print('!')
            super().__setattr__(key, value)
