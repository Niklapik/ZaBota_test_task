from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram.enums import ChatAction
import logging

from keyboards import kb_new_request
from constants import HELP_TEXT, START_TEXT, NEW_REQUEST_TEXT
from config import configure_bot
from exceptions import BaseConfigException

try:
    bot, dp, client, user_contexts = configure_bot()
except BaseConfigException as error:
    logging.critical(f'Ошибка конфигурации бота: {error}')
    exit(1)


@dp.startup()
async def startup() -> None:
    logging.info('Бот успешно запущен!')


def get_user_id(message: Message) -> int:
    user_id = message.from_user.id
    return user_id


async def reset_context(user_id: int, message: Message, answer_text: str) -> None:
    logging.info(f'Сброс контекста для пользователя {user_id}')
    user_contexts[user_id] = []
    await message.answer(text=answer_text, reply_markup=kb_new_request)


@dp.message(Command('start'))
async def start_command(message: Message) -> None:
    user_id = get_user_id(message)
    logging.info(f'Пользователь {user_id} вызвал /start')
    await reset_context(user_id=user_id, message=message,
                        answer_text=START_TEXT)


@dp.message(F.text == "Новый запрос")
async def new_request(message: Message) -> None:
    user_id = get_user_id(message)
    logging.info(f'Пользователь {user_id} нажал кнопку нового запроса')
    await reset_context(user_id=user_id, message=message,
                        answer_text=NEW_REQUEST_TEXT)


@dp.message(Command('help'))
async def help_command(message: Message) -> None:
    user_id = get_user_id(message)
    logging.info(f'Пользователь {user_id} вызвал /help')
    await message.answer(text=HELP_TEXT, parse_mode='HTML', reply_markup=kb_new_request)


@dp.message(F.content_type == ContentType.TEXT)
async def message_processing(message: Message) -> None:
    try:
        user_id = get_user_id(message)

        logging.info('Эмуляция набора теста ботом')
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

        user_contexts[user_id].append({"role": "user", "content": message.text})

        logging.info(f'Отправка запроса к AI для пользователя {user_id}')
        completion = client.chat.completions.create(
            model="gpt-5-mini",
            messages=user_contexts[user_id]
        )

        logging.info('Парсинг ответа AI')
        response_text = completion.choices[0].message.content
        user_contexts[user_id].append({"role": "assistant", "content": response_text})

        logging.info(f'Отправка ответа пользователю {user_id}')
        await message.answer(text=response_text, reply_markup=kb_new_request)

    except Exception as error:
        logging.error(f'Ошибка запроса для {user_id}: {error}')
        await message.answer('Ошибка при обработке запроса', reply_markup=kb_new_request)


@dp.message(F.content_type != ContentType.TEXT)
async def not_text_handler(message: Message):
    await message.answer("❌Я работаю только с текстовыми сообщениями ❌")


if __name__ == '__main__':
    dp.run_polling(bot)
