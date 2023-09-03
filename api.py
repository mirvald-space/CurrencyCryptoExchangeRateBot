import aiohttp
import logging
import time
from config import MONOBANK_URL, CACHE_TIMEOUT

# Глобальные переменные для кеширования
cached_rates = None
last_updated = 0


# Обратите внимание, что тип изменился на int
async def get_exchange_rate(currency_code: int) -> float:
    global cached_rates, last_updated

    if cached_rates is None or time.time() - last_updated >= CACHE_TIMEOUT:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(MONOBANK_URL) as response:
                    data = await response.json()

            if not data:
                logging.error("Получены пустые данные от API Monobank")
                return None

            cached_rates = data
            last_updated = time.time()
        except Exception as e:
            logging.error(f"Ошибка при получении курсов валют. {e}")
            return None

    for rate in cached_rates:
        if rate['currencyCodeA'] == currency_code:  # Ищем по коду валюты
            return float(rate['rateBuy'])  # Возвращаем курс покупки

    logging.error(f"Курс валюты {currency_code} не найден")
    return None


# Функция обработки курса криптовалют
async def get_crypto_rate(symbol, fiat="USDT"):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            for item in data:
                if item['symbol'] == f"{symbol}{fiat}":
                    return float(item['lastPrice'])
    return None
