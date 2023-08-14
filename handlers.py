from aiogram import types
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
        await self.update_last_activity(user_id)
        markup = await self.generate_main_menu_markup()
        await message.answer("Привіт! Цей бот показує актуальний курс фіатних валют і криптовалют.", reply_markup=markup)

    async def generate_main_menu_markup(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in [("🇺🇦Курс валют", "currency_rates"), ("🤑Курс криптовалют", "crypto"), ("📊Статистика", "stats"),
                     ("✉️Реклама", "ads"), ]:
            markup.insert(KeyboardButton(item[0]))
        return markup

    async def currency_rates(self, message: types.Message):
        usd_uah = await get_exchange_rate(840)  # USD
        eur_uah = await get_exchange_rate(978)  # EUR

        if usd_uah is None or eur_uah is None:
            await message.answer("Вибачте, не вдалося отримати курси валют. Спробуйте пізніше.")
            return

        await message.answer(
            f"<b>🇺🇦 Українська гривня</b>\n\n 🇺🇸USD/UAH <b>{usd_uah} </b> \n🇪🇺 EUR/UAH <b>{eur_uah}</b>\n\n"
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

    async def get_active_user_count(self):
        async with self.pool.acquire() as connection:
            query = """
            SELECT COUNT(*)
            FROM users
            WHERE last_activity > NOW() - INTERVAL '7 days'
            """
            active_user_count = await connection.fetchval(query)
            return active_user_count

    async def stats(self, message: types.Message):
        if message.from_user.id != ADMIN_ID:
            await message.answer("У вас нет прав доступа к этой команде.")
            return

        user_count = await get_user_count(self.pool)
        active_user_count = await get_active_user_count(self.pool)

        response = (
            f"Кількість користувачів: {user_count}\n"
            f"Кількість активних користувачів: {active_user_count}"
        )
        await message.answer(response)

    async def update_last_activity(self, user_id):
        async with self.pool.acquire() as connection:
            query = """
            UPDATE users
            SET last_activity = NOW()
            WHERE id = $1
            """
            await connection.execute(query, user_id)

    async def start_broadcast(self, message: types.Message):
        if not await is_admin(self.pool, message.from_user.id):
            await message.reply("Ви не є адміністратором!")
            return
        await message.reply("Будь ласка, напишіть повідомлення, яке потрібно розіслати:")

    async def process_broadcast_message(self, message: types.Message):
        text_to_broadcast = message.text

        user_ids = await get_all_users(self.pool)
        for user_id in user_ids:
            try:
                await self.bot.send_message(user_id, text_to_broadcast)
            except Exception as e:
                print(f"Не вдалося відправити повідомлення на адресу {user_id}: {e}")

        await message.reply("Повідомлення успішно відправлено всім користувачам!")



