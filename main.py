import logging
import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TELEGRAM_TOKEN
from handlers import Handlers
import database

async def init(dp):
    # Создание пула соединений
    pool = await database.create_pool()

    # Создание таблиц, если они не существуют
    await database.create_tables()

    bot = Bot(token=TELEGRAM_TOKEN)  # Создаем объект bot
    handlers = Handlers(pool, bot)

    dp.register_message_handler(handlers.start_command, commands=["start"])
    dp.register_message_handler(handlers.currency_rates, lambda message: message.text == "🇺🇦Курс валют")
    dp.register_message_handler(handlers.stats, lambda message: message.text == "📊Статистика")
    dp.register_message_handler(handlers.crypto, lambda message: message.text == "🤑Курс криптовалют")
    dp.register_message_handler(handlers.ads, lambda message: message.text == "✉️Реклама")
    dp.register_message_handler(handlers.start_broadcast, lambda message: message.text.startswith("/broadcast"))
    dp.register_message_handler(handlers.process_broadcast_message)




logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)  # Эта строка должна быть удалена, так как bot уже создан выше
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(dp))
    executor.start_polling(dp, skip_updates=True)
