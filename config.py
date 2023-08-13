import os

from dotenv import load_dotenv

load_dotenv()


# URL API
PRIVAT_BANK_URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

# Таймаут для кеширования
CACHE_TIMEOUT = 3600  # Примерное время жизни кеша, в секундах

# Загрузка переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# Загрузка переменных окружения
DATABASE_URL= os.getenv("DATABASE_URL")