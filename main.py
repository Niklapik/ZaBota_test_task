import os
from collections import defaultdict

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from openai import OpenAI

from keyboards import kb_new_request

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

client = OpenAI(
    base_url="https://neuroapi.host/v1",
    api_key=OPENAI_API_KEY,
)

user_contexts = defaultdict(list)


@dp.startup()
async def startup() -> None:
    print('Бот успешно запущен!')


async def reset_context(user_id: int, message: Message, answer_text: str) -> None:
    user_contexts[user_id] = []
    await message.answer(text=answer_text, reply_markup=kb_new_request)


@dp.message(Command('start'))
async def start_command(message: Message) -> None:
    await reset_context(user_id=message.from_user.id, message=message, answer_text='Бот успешно запущен')


@dp.message(F.text == "Новый запрос")
async def new_request(message: Message) -> None:
    await reset_context(user_id=message.from_user.id, message=message, answer_text='Контекст успешно сброшен')


@dp.message(Command('help'))
async def help_command(message: Message) -> None:
    await message.answer(text='Тут пока ничего нет, но скоро тут будет текст-подсказка')


@dp.message()
async def message_processing(message: Message) -> None:
    user_id = message.from_user.id

    user_contexts[user_id].append({"role": "user", "content": message.text})

    completion = client.chat.completions.create(
        model="gpt-5-mini",
        messages=user_contexts[user_id]
    )

    response_text = completion.choices[0].message.content
    user_contexts[user_id].append({"role": "assistant", "content": response_text})

    await message.answer(text=response_text, reply_markup=kb_new_request)


if __name__ == '__main__':
    dp.run_polling(bot)
