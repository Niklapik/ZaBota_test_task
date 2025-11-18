from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ChatAction

from keyboards import kb_new_request
from constants import HELP_TEXT, START_TEXT, NEW_REQUEST_TEXT
from config import configure_bot

bot, dp, client, user_contexts = configure_bot()


@dp.startup()
async def startup() -> None:
    print('Бот успешно запущен!')


async def reset_context(user_id: int, message: Message, answer_text: str) -> None:
    user_contexts[user_id] = []
    await message.answer(text=answer_text, reply_markup=kb_new_request)


@dp.message(Command('start'))
async def start_command(message: Message) -> None:
    await reset_context(user_id=message.from_user.id, message=message,
                        answer_text=START_TEXT)


@dp.message(F.text == "Новый запрос")
async def new_request(message: Message) -> None:
    await reset_context(user_id=message.from_user.id, message=message,
                        answer_text=NEW_REQUEST_TEXT)


@dp.message(Command('help'))
async def help_command(message: Message) -> None:
    await message.answer(text=HELP_TEXT, parse_mode='HTML', reply_markup=kb_new_request)


@dp.message()
async def message_processing(message: Message) -> None:
    user_id = message.from_user.id

    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

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
