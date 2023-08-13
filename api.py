import aiohttp
import logging
import time
import json
from config import PRIVAT_BANK_URL, CACHE_TIMEOUT

# Глобальные переменные для кеширования
cached_rates = None
last_updated = 0


async def get_exchange_rate(currency_code: str) -> float:
    global cached_rates, last_updated

    if cached_rates is None or time.time() - last_updated >= CACHE_TIMEOUT:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(PRIVAT_BANK_URL) as response:
                    data = await response.json()

            if not data:
                logging.error("Получены пустые данные от API ПриватБанка")
                return None

            cached_rates = data
            last_updated = time.time()
        except Exception as e:
            logging.error(f"Ошибка при получении курсов валют. {e}")
            return None

    for rate in cached_rates:
        if rate['ccy'] == currency_code:
            return float(rate['buy'])

    logging.error(f"Курс валюты {currency_code} не найден")
    return None


async def get_crypto_rate(symbol, fiat="USDT"):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            for item in data:
                if item['symbol'] == f"{symbol}{fiat}":
                    return float(item['lastPrice'])
    return None
