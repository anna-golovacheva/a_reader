from settings import DB, TABLE_NAME_1, TABLE_NAME_2, TRIES
from data import DBConnect


if __name__ == '__main__':
    bot_db = DBConnect(DB)

    bot_db.create_table(TABLE_NAME_1, ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'tg_id INTEGER', 'user_name VARCHAR(30)', 'is_active BOOLEAN DEFAULT false', 'wins_num INTEGER DEFAULT 0', 'games_num INTEGER DEFAULT 0'])
    bot_db.create_table(TABLE_NAME_2, ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'user_id INTEGER CONSTRAINT user_id_fk REFERENCES users(id)', 'is_active BOOLEAN DEFAULT true', 'number INTEGER', f'tries_num INTEGER DEFAULT {TRIES}', 'is_win BOOLEAN DEFAULT false'])
    