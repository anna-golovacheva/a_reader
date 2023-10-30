from settings import db
from data import DBConnect


if __name__ == '__main__':
    bot_db = DBConnect(db)
    # check types and default values
    table_name_1 = 'users'
    table_name_2 = 'games'
    bot_db.create_table(table_name_1, ['id INTEGER PRIMARY KEY', 'user_name VARCHAR(30)', 'is_active BOOLEAN DEFAULT true', 'wins_num INTEGER DEFAULT 0'])
    bot_db.create_table(table_name_2, ['id INTEGER PRIMARY KEY', 'user_id INTEGER CONSTRAINT user_id_fk REFERENCES users(id)', 'is_active BOOLEAN DEFAULT true', 'number INTEGER', 'tries_num INTEGER DEFAULT 0', 'is_win BOOLEAN DEFAULT false'])