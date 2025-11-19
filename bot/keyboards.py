from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_new_request = KeyboardButton(text='Новый запрос')

kb_new_request = ReplyKeyboardMarkup(
    keyboard=[
        [button_new_request]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)
