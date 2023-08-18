import logging
import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TELEGRAM_TOKEN
from handlers import Handlers
import database
import fcntl
import sys

# Попытка заблокировать файл


def lock_file(file):
    try:
        fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except BlockingIOError:
        return False


async def init(dp):
    # Создание пула соединений
    pool = await database.create_pool()

    # Создание таблиц, если они не существуют
    await database.create_tables()

    bot = Bot(token=TELEGRAM_TOKEN)  # Создаем объект bot
    handlers = Handlers(pool, bot)

    dp.register_message_handler(handlers.start_command, commands=["start"])
    dp.register_message_handler(
        handlers.currency_rates, lambda message: message.text == "🇺🇦Курс валют")
    dp.register_message_handler(
        handlers.stats, lambda message: message.text == "📊Статистика")
    dp.register_message_handler(
        handlers.crypto, lambda message: message.text == "🤑Курс криптовалют")
    dp.register_message_handler(
        handlers.ads, lambda message: message.text == "✉️Реклама")
    dp.register_message_handler(
        handlers.start_broadcast, lambda message: message.text.startswith("/broadcast"))
    dp.register_message_handler(handlers.process_broadcast_message)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

if __name__ == '__main__':
    lockfile = open('/tmp/bot.lock', 'w')
    if not lock_file(lockfile):
        print("Another instance is already running. Exiting.")
        sys.exit(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(dp))
    executor.start_polling(dp, skip_updates=True)

    # Освобождаем блокировку перед выходом
    lockfile.close()
