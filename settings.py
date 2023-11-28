import os
from pathlib import Path
from dotenv import load_dotenv

from cs50 import SQL


BASE_DIR = Path(__file__).resolve().parent

dot_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dot_env)

DB = SQL('sqlite:///database.db')

BOT_TOKEN = os.getenv('BOT_TOKEN')

TABLE_NAME_1 = 'users'
TABLE_NAME_2 = 'games'

TRIES = '10'
