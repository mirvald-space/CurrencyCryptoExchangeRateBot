import os
from dotenv import load_dotenv

load_dotenv()


# URL API
MONOBANK_URL = 'https://api.monobank.ua/bank/currency'

# Таймаут для кеширования
CACHE_TIMEOUT = 60 * 60  # Примерное время жизни кеша, в секундах


# Загрузка переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# Загрузка переменных окружения
DATABASE_URL= os.getenv("DATABASE_URL")
ADMIN_ID=os.getenv("ADMIN_ID")