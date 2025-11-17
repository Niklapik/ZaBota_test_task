import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.startup()
async def startup():
    print('Бот успешно запущен!')


@dp.message(Command('start'))
async def start_command(message: Message) -> None:
    await message.answer('Бот успешно запущен!')


if __name__ == '__main__':
    dp.run_polling(bot)
