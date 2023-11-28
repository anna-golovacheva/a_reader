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
        create_script = f'INSERT INTO {table_name} ({fields_names}) VALUES ({values_names})'
        the_id = self.db_name.execute(create_script)
        return the_id

    def set_field(self, table_name: str, object_id: int, field: str, value: Any):
        if not isinstance(value, int):
            value = '"' + str(value) + '"'
        set_script = f'UPDATE {table_name} SET {field} = {value} WHERE id="{object_id}"'
        self.db_name.execute(set_script)

    def get_objects(self, table_name: str, search: dict[str, str | int | bool] = None):
        if search is None:
            select_script = f'SELECT * FROM {table_name}'
        else:
            searching = ' AND '.join([f'{key}={value}' for key, value in search.items()])
            select_script = f'SELECT * FROM {table_name} WHERE {searching}'
        the_ids = self.db_name.execute(select_script)
        return the_ids

    def delete_objects(self, table_name:str, delete: dict[str, str | int | bool]):
        deleting = ' AND '.join([f'{key}="{value}"' for key, value in delete.items()])
        delete_script = f'DELETE FROM {table_name} WHERE {deleting}'
        self.db_name.execute(delete_script)
