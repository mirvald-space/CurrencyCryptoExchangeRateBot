from aiogram import types
from api import get_exchange_rate, get_crypto_rate
from database import add_new_user, get_user_count
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Handlers:
    def __init__(self, pool):
        self.pool = pool

    async def start_command(self, message: types.Message):
        user_id = message.from_user.id
        await add_new_user(self.pool, user_id)
        markup = await self.generate_main_menu_markup()
        await message.answer("Выберите пункт меню:", reply_markup=markup)

    async def generate_main_menu_markup(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in [("🇺🇦Курс валют", "currency_rates"), ("🤑Курс криптовалют", "crypto"), ("📊Статистика", "stats"), ("ℹ️Помощь", "help"),]:
            markup.insert(KeyboardButton(item[0]))
        return markup

    async def currency_rates(self, message: types.Message):
        usd_uah = await get_exchange_rate('USD')
        eur_uah = await get_exchange_rate('EUR')
        await message.answer(f"<b>🇺🇦 Українська гривня</b>\n\n🇺🇸 USD/UAH <b>{usd_uah} </b> \n🇪🇺 EUR/UAH <b>{eur_uah}</b>", parse_mode='HTML')

    async def crypto(self, message: types.Message):
        btc_rate = await get_crypto_rate('BTC')
        eth_rate = await get_crypto_rate('ETH')
        xrp_rate = await get_crypto_rate('XRP')
        doge_rate = await get_crypto_rate('DOGE')
        ada_rate = await get_crypto_rate('ADA')
        sol_rate = await get_crypto_rate('SOL')

        response = f"<b>Текущие курсы криптовалют:</b>\n\n" \
                   f"🔹 Bitcoin (BTC): ${btc_rate}\n" \
                   f"🔹 Ethereum (ETH): ${eth_rate}\n" \
                   f"🔹 XRP (XRP): ${xrp_rate}\n" \
                   f"🔹 Dogecoin (DOGE): ${doge_rate}\n" \
                   f"🔹 Cardano (ADA): ${ada_rate}\n" \
                   f"🔹 Solana (ETH): ${sol_rate}"
        await message.answer(response, parse_mode='HTML')

    async def help(self, message: types.Message):
        await message.answer("Здесь будет справка и помощь.")

    async def stats(self, message: types.Message):
        user_count = await get_user_count(self.pool)
        await message.answer(f"Количество пользователей: {user_count}")
