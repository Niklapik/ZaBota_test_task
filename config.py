import os
import logging
from collections import defaultdict

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from openai import OpenAI


def configure_bot():
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    user_contexts = defaultdict(list)

    client = OpenAI(
        base_url="https://neuroapi.host/v1",
        api_key=OPENAI_API_KEY,
    )

    return bot, dp, client, user_contexts
