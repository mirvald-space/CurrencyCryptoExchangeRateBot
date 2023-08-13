import logging
import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TELEGRAM_TOKEN
from handlers import Handlers
from database import create_pool

async def init(dp):
    pool = await create_pool()
    handlers = Handlers(pool)

    dp.register_message_handler(handlers.start_command, commands=["start"])
    # Регистрация других обработчиков на основе пунктов меню
    dp.register_message_handler(handlers.currency_rates, lambda message: message.text == "🇺🇦Курс валют")
    dp.register_message_handler(handlers.stats, lambda message: message.text == "📊Статистика")
    dp.register_message_handler(handlers.crypto, lambda message: message.text == "🤑Курс криптовалют")
    dp.register_message_handler(handlers.help, lambda message: message.text == "ℹ️Помощь")


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(dp))
    executor.start_polling(dp, skip_updates=True)
