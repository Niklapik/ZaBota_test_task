import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

client = OpenAI(
    base_url="https://neuroapi.host/v1",
    api_key=OPENAI_API_KEY,
)
user_contexts = {}


@dp.startup()
async def startup():
    print('Бот успешно запущен!')


@dp.message(Command('start'))
async def start_command(message: Message) -> None:
    user_contexts[message.from_user.id] = []
    await message.answer('Бот успешно запущен!')


@dp.message()
async def message_processing(message: Message) -> None:
    user_id = message.from_user.id

    # Можно добавить defaultdict
    if user_id not in user_contexts:
        user_contexts[user_id] = []

    user_contexts[user_id].append({"role": "user", "content": message.text})

    completion = client.chat.completions.create(
        model="gpt-5-mini",
        messages=user_contexts[user_id]
    )

    response_text = completion.choices[0].message.content
    user_contexts[user_id].append({"role": "assistant", "content": response_text})

    await message.answer(response_text)


if __name__ == '__main__':
    dp.run_polling(bot)
