# database.py
import asyncpg
from config import DATABASE_URL

async def create_pool():
    return await asyncpg.create_pool(DATABASE_URL)
async def create_tables():
    connection = await asyncpg.connect(DATABASE_URL)
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE
        )
    ''')
    await connection.close()

# database.py
async def add_new_user(pool, user_id):
    async with pool.acquire() as connection:
        await connection.execute("INSERT INTO users (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)


async def get_user_count(pool):
    async with pool.acquire() as connection:
        user_count = await connection.fetchval("SELECT COUNT(*) FROM users")
        return user_count
