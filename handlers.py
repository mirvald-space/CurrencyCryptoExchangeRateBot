from aiogram import types
import database
from config import ADMIN_ID
from api import get_exchange_rate, get_crypto_rate
from database import add_new_user, get_user_count, get_all_users, is_admin
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Handlers:
    def __init__(self, pool, bot):
        self.pool = pool
        self.bot = bot

    async def start_command(self, message: types.Message):
        user_id = message.from_user.id
        await add_new_user(self.pool, user_id)
        markup = await self.generate_main_menu_markup()
        await message.answer("Привіт! Цей бот показує актуальний курс фіатних валют і криптовалют.", reply_markup=markup)

    async def generate_main_menu_markup(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in [("🇺🇦Курс валют", "currency_rates"), ("🤑Курс криптовалют", "crypto"), ("📊Статистика", "stats"),
                     ("✉️Реклама", "ads"), ]:
            markup.insert(KeyboardButton(item[0]))
        return markup

    async def currency_rates(self, message: types.Message):
        usd_uah = await get_exchange_rate('USD')
        eur_uah = await get_exchange_rate('EUR')
        await message.answer(
            f"<b>🇺🇦 Українська гривня</b>\n\n🇺🇸 USD/UAH <b>{usd_uah} </b> \n🇪🇺 EUR/UAH <b>{eur_uah}</b>\n\n" 
            f"Актуальні курси: @ExchangeMonitorBot",
            parse_mode='HTML')

    async def crypto(self, message: types.Message):
        btc_rate = await get_crypto_rate('BTC')
        eth_rate = await get_crypto_rate('ETH')
        xrp_rate = await get_crypto_rate('XRP')
        doge_rate = await get_crypto_rate('DOGE')
        ada_rate = await get_crypto_rate('ADA')
        sol_rate = await get_crypto_rate('SOL')

        response = f"<b>Поточні курси криптовалют:</b>\n\n" \
                   f"🔹 Bitcoin (BTC): ${btc_rate}\n" \
                   f"🔹 Ethereum (ETH): ${eth_rate}\n" \
                   f"🔹 XRP (XRP): ${xrp_rate}\n" \
                   f"🔹 Dogecoin (DOGE): ${doge_rate}\n" \
                   f"🔹 Cardano (ADA): ${ada_rate}\n" \
                   f"🔹 Solana (ETH): ${sol_rate}\n\n"\
                    f"Актуальні курси: @ExchangeMonitorBot"
        await message.answer(response, parse_mode='HTML')

    async def ads(self, message: types.Message):
        contact_admin_text = (
            "Якщо у вас є питання або пропозиції щодо реклами, будь ласка, зв'яжіться з адміністратором."
            "\n\n👤 [Зв'язатися з адміном](tg://user?id={admin_id})"
        )
        await message.answer(contact_admin_text.format(admin_id=ADMIN_ID), parse_mode="Markdown")

    async def stats(self, message: types.Message):
        user_count = await get_user_count(self.pool)
        await message.answer(f"Количество пользователей: {user_count}")

    async def start_broadcast(self, message: types.Message):
        if not await is_admin(self.pool, message.from_user.id):
            await message.reply("Вы не являетесь администратором!")
            return
        await message.reply("Пожалуйста, напишите сообщение, которое нужно разослать:")

    async def process_broadcast_message(self, message: types.Message):
        text_to_broadcast = message.text

        user_ids = await get_all_users(self.pool)
        for user_id in user_ids:
            try:
                await self.bot.send_message(user_id, text_to_broadcast)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")

        await message.reply("Сообщение успешно отправлено всем пользователям!")



