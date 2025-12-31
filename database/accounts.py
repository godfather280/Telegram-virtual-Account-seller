from .db import db
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AccountsDB:
    @staticmethod
    async def add_account(session_string: str, phone_number: str = None) -> bool:
        """Add a new session account"""
        try:
            await db.execute(
                """INSERT INTO accounts (session_string, phone_number) 
                VALUES (?, ?)""",
                (session_string, phone_number)
            )
            await db.conn.commit()
            logger.info(f"Added account: {phone_number or 'No phone'}")
            return True
        except Exception as e:
            logger.error(f"Error adding account: {e}")
            return False

    @staticmethod
    async def get_free_account() -> Optional[Dict[str, Any]]:
        """Get a free account that's not in use"""
        try:
            row = await db.fetch_one(
                """SELECT * FROM accounts 
                WHERE is_active = 1 AND is_in_use = 0 
                ORDER BY last_used ASC, total_numbers_served ASC 
                LIMIT 1"""
            )
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting free account: {e}")
            return None

    @staticmethod
    async def mark_used(account_id: int) -> bool:
        """Mark account as in use"""
        try:
            await db.execute(
                """UPDATE accounts 
                SET is_in_use = 1, 
                    last_used = CURRENT_TIMESTAMP,
                    total_numbers_served = total_numbers_served + 1 
                WHERE account_id = ?""",
                (account_id,)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error marking account used: {e}")
            return False

    @staticmethod
    async def mark_free(account_id: int) -> bool:
        """Mark account as free"""
        try:
            await db.execute(
                "UPDATE accounts SET is_in_use = 0 WHERE account_id = ?",
                (account_id,)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error marking account free: {e}")
            return False

    @staticmethod
    async def get_account(account_id: int) -> Optional[Dict[str, Any]]:
        """Get account by ID"""
        try:
            row = await db.fetch_one(
                "SELECT * FROM accounts WHERE account_id = ?",
                (account_id,)
            )
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting account: {e}")
            return None

    @staticmethod
    async def disable_account(account_id: int) -> bool:
        """Disable an account"""
        try:
            await db.execute(
                "UPDATE accounts SET is_active = 0 WHERE account_id = ?",
                (account_id,)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error disabling account: {e}")
            return False

    @staticmethod
    async def enable_account(account_id: int) -> bool:
        """Enable an account"""
        try:
            await db.execute(
                "UPDATE accounts SET is_active = 1 WHERE account_id = ?",
                (account_id,)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error enabling account: {e}")
            return False

    @staticmethod
    async def get_all_accounts() -> list:
        """Get all accounts"""
        try:
            rows = await db.fetch_all(
                "SELECT * FROM accounts ORDER BY account_id"
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all accounts: {e}")
            return []
