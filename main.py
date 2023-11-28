from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from settings import BOT_TOKEN, TRIES
from classes import User, Game
from utils import get_random_number


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Привет! Хочешь сыграть в игру "Угадай число"? \n'
                         'чтобы начать игру, напиши "давай" \n'
                         'чтобы прочитать подробные правила, отправь команду /help')
    User.get_or_create(message.from_user)


@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {TRIES} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )
    User.get_or_create(message.from_user)


@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    user = User.get_or_create(message.from_user)

    if user.is_active:
        user.is_active = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы итак с вами не играем. '
            'Может, сыграем разок?'
        )


@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    user = User.get_or_create(message.from_user)
    if not user.is_active:
        user.is_active = True
        number = get_random_number()
        Game.create(user.pk, number)
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    user = User.get_or_create(message.from_user)
    if not user.is_active:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    user = User.get_or_create(message.from_user)
    if user.is_active:
        game = Game.get_object({'user_id': user.pk, 'is_active': 'True'})
        print(game)
        if int(message.text) == game.number:
            user.is_active = False
            game.is_win = True
            game.is_active = False
            user.games_num += 1
            user.wins_num += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > game.number:
            game.tries_num -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < game.number:
            game.tries_num -= 1
            await message.answer('Мое число больше')

        if game.tries_num == 0:
            game.is_active = False
            user.is_active = False
            user.games_num += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {game.number}\n\nДавайте '
                f'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    user = User.get_or_create(message.from_user)
    all_users = User.get_all()
    if all_users:
        sorted_users = sorted(all_users, key=lambda x: x.wins_num, reverse=True)
        place = sorted_users.index(user) + 1
    await message.answer(
        f'Всего игр сыграно: '
        f'{user.games_num}\n'
        f'Игр выиграно: {user.wins_num}\n'
        f'Вы на {place} месте!'
    )


@dp.message()
async def process_other_answers(message: Message):
    user = User.get_or_create(message.from_user)
    if user.is_active:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )


if __name__ == '__main__':

    dp.run_polling(bot)
