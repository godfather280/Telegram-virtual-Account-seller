import aiosqlite
from config import DB_NAME
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db_name = DB_NAME
        self.conn = None

    async def connect(self):
        """Connect to SQLite database"""
        self.conn = await aiosqlite.connect(self.db_name)
        self.conn.row_factory = aiosqlite.Row
        await self.init_tables()
        logger.info(f"Connected to database: {self.db_name}")

    async def close(self):
        """Close database connection"""
        if self.conn:
            await self.conn.close()
            logger.info("Database connection closed")

    async def init_tables(self):
        """Initialize all tables"""
        await self.conn.executescript('''
            -- Users table
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_banned INTEGER DEFAULT 0,
                total_spent INTEGER DEFAULT 0,
                total_numbers INTEGER DEFAULT 0
            );

            -- Countries table
            CREATE TABLE IF NOT EXISTS countries (
                country_id INTEGER PRIMARY KEY AUTOINCREMENT,
                country_code TEXT UNIQUE,
                country_name TEXT,
                price INTEGER DEFAULT 50,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Session accounts table
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_string TEXT UNIQUE,
                phone_number TEXT,
                is_active INTEGER DEFAULT 1,
                is_in_use INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                total_numbers_served INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Virtual numbers table
            CREATE TABLE IF NOT EXISTS numbers (
                number_id INTEGER PRIMARY KEY AUTOINCREMENT,
                country_code TEXT,
                phone_number TEXT UNIQUE,
                is_assigned INTEGER DEFAULT 0,
                assigned_to INTEGER,
                assigned_at TIMESTAMP,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assigned_to) REFERENCES users(user_id)
            );

            -- Payments table
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                utr TEXT UNIQUE,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                verified_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            -- Orders table
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                number_id INTEGER,
                account_id INTEGER,
                otp_code TEXT,
                price INTEGER,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (number_id) REFERENCES numbers(number_id),
                FOREIGN KEY (account_id) REFERENCES accounts(account_id)
            );
        ''')
        await self.conn.commit()
        logger.info("Database tables initialized")

    async def execute(self, query: str, params: tuple = ()):
        """Execute a query"""
        return await self.conn.execute(query, params)

    async def fetch_one(self, query: str, params: tuple = ()):
        """Fetch one row"""
        cursor = await self.conn.execute(query, params)
        row = await cursor.fetchone()
        await cursor.close()
        return row

    async def fetch_all(self, query: str, params: tuple = ()):
        """Fetch all rows"""
        cursor = await self.conn.execute(query, params)
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

# Global database instance
db = Database()
