import asyncpg
from config import DATABASE_URL


async def create_pool():
    return await asyncpg.create_pool(DATABASE_URL)


async def create_tables():
    connection = await asyncpg.connect(DATABASE_URL)
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE,
            last_activity TIMESTAMPTZ DEFAULT now()
        )
    ''')

    await connection.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE
        )
    ''')
    await connection.close()


async def add_admin(pool, admin_id):
    async with pool.acquire() as connection:
        await connection.execute("INSERT INTO admins (user_id) VALUES ($1) ON CONFLICT DO NOTHING", int(admin_id))


async def is_admin(pool, user_id):
    async with pool.acquire() as connection:
        admin_id = await connection.fetchval("SELECT user_id FROM admins WHERE user_id = $1", int(user_id))
        return admin_id is not None


async def add_new_user(pool, user_id):
    async with pool.acquire() as connection:
        await connection.execute("INSERT INTO users (user_id) VALUES ($1) ON CONFLICT DO NOTHING", int(user_id))


async def get_user_count(pool):
    async with pool.acquire() as connection:
        user_count = await connection.fetchval("SELECT COUNT(*) FROM users")
        return user_count


async def get_all_users(pool):
    async with pool.acquire() as connection:
        user_ids = await connection.fetch("SELECT user_id FROM users")
        return [row['user_id'] for row in user_ids]


async def update_last_activity(pool, user_id):
    async with pool.acquire() as connection:
        await connection.execute("UPDATE users SET last_activity = NOW() WHERE user_id = $1", int(user_id))


async def get_active_user_count(self):
    async with self.pool.acquire() as connection:
        query = """
        SELECT COUNT(*)
        FROM users
        WHERE last_activity > NOW() - INTERVAL '7 days'
        """
        active_user_count = await connection.fetchval(query)
        return active_user_count
