from typing import Any


class DBConnect:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self, table_name: str, fields: list[str]):
        fields_names = ', '.join(fields)
        create_script = f'CREATE TABLE IF NOT EXISTS {table_name} ({fields_names});'
        self.db_name.execute(create_script)

    def create_object(self, table_name: str, fields: list[str], values: list[str]):
        fields_names = ', '.join(fields)
        values = ['"' + str(val) + '"' for val in values]
        values_names = ', '.join(values)
        create_script = f'INSERT INTO {table_name} ({fields_names}) VALUES ({values_names});'
        print(create_script)
        self.db_name.execute(create_script)

    def set_field(self, table_name: str, object_id: int, field: str, value: Any):
        if not isinstance(value, int):
            value = '"' + str(value) + '"'
        set_script = f'UPDATE {table_name} SET {field} = {value} WHERE id="{object_id}"'
        self.db_name.execute(set_script)
