import os
from pathlib import Path
from dotenv import load_dotenv

from cs50 import SQL


BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

dot_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dot_env)

db = SQL("sqlite:///database.db")

BOT_TOKEN = os.getenv('BOT_TOKEN')
