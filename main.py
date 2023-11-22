from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from random import randint
from settings import BOT_TOKEN, db
from data import DBConnect
from classes import User, Game


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer('Привет! Хочешь сыграть в игру "Угадай число"? \n'
                         'чтобы начать игру, напиши "давай" \n'
                         'чтобы прочитать подробные правила, отправь команду /help')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        'правила игры и описание команд'
    )


# Этот хэндлер будет срабатывать на любые сообщения,
# кроме команд "/start" и "/help"
@dp.message(F.text.lower() == "давай")
async def start_game(message: Message):

        await message.send_copy(chat_id=message.chat.id)



if __name__ == '__main__':
    # bot_db = DBConnect(db)
    name = 'Jim'
    user = User.create(name)
    number = randint(1, 100)
    game = Game.create(user.pk, number)


    # dp.run_polling(bot)
