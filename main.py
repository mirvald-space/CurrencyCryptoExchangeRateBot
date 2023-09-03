import logging
import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TELEGRAM_TOKEN
from handlers import Handlers
import database


class SingletonBot:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.bot = Bot(token=TELEGRAM_TOKEN)
            cls._instance.dp = Dispatcher(
                cls._instance.bot, storage=MemoryStorage())
            cls._instance.init_handlers()
        return cls._instance

    def init_handlers(self):
        pool = asyncio.get_event_loop().run_until_complete(database.create_pool())
        handlers = Handlers(pool, self.bot)

        self.dp.register_message_handler(
            handlers.start_command, commands=["start"])
        self.dp.register_message_handler(
            handlers.currency_rates, lambda message: message.text == "🇺🇦Курс валют")
        self.dp.register_message_handler(
            handlers.stats, lambda message: message.text == "📊Статистика")
        self.dp.register_message_handler(
            handlers.crypto, lambda message: message.text == "🤑Курс криптовалют")
        self.dp.register_message_handler(
            handlers.ads, lambda message: message.text == "✉️Реклама")
        self.dp.register_message_handler(
            handlers.start_broadcast, lambda message: message.text.startswith("/broadcast"))
        self.dp.register_message_handler(handlers.process_broadcast_message)


class BotSingleton(SingletonBot):
    pass


def main():
    logging.basicConfig(level=logging.INFO)
    bot_instance = BotSingleton()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(database.create_tables())
    executor.start_polling(bot_instance.dp, skip_updates=True)


if __name__ == '__main__':
    main()
