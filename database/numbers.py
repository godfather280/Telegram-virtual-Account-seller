from .db import db
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timedelta
from config import NUMBER_DURATION

logger = logging.getLogger(__name__)

class NumbersDB:
    @staticmethod
    async def generate_number(country_code: str, phone_number: str) -> bool:
        """Generate a new virtual number"""
        try:
            await db.execute(
                """INSERT OR IGNORE INTO numbers 
                (country_code, phone_number) 
                VALUES (?, ?)""",
                (country_code, phone_number)
            )
            await db.conn.commit()
            logger.info(f"Generated number: {phone_number} ({country_code})")
            return True
        except Exception as e:
            logger.error(f"Error generating number: {e}")
            return False

    @staticmethod
    async def get_available_number(country_code: str) -> Optional[Dict[str, Any]]:
        """Get an available number for a country"""
        try:
            row = await db.fetch_one(
                """SELECT * FROM numbers 
                WHERE country_code = ? AND is_assigned = 0 
                ORDER BY RANDOM() LIMIT 1""",
                (country_code,)
            )
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting available number: {e}")
            return None

    @staticmethod
    async def assign_number(number_id: int, user_id: int) -> bool:
        """Assign number to user"""
        try:
            expires_at = datetime.now() + timedelta(seconds=NUMBER_DURATION)
            await db.execute(
                """UPDATE numbers 
                SET is_assigned = 1, 
                    assigned_to = ?,
                    assigned_at = CURRENT_TIMESTAMP,
                    expires_at = ? 
                WHERE number_id = ?""",
                (user_id, expires_at, number_id)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error assigning number: {e}")
            return False

    @staticmethod
    async def expire_number(number_id: int) -> bool:
        """Expire a number"""
        try:
            await db.execute(
                """UPDATE numbers 
                SET is_assigned = 0, 
                    assigned_to = NULL,
                    assigned_at = NULL,
                    expires_at = NULL 
                WHERE number_id = ?""",
                (number_id,)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error expiring number: {e}")
            return False

    @staticmethod
    async def get_user_numbers(user_id: int) -> list:
        """Get all numbers assigned to user"""
        try:
            rows = await db.fetch_all(
                """SELECT * FROM numbers 
                WHERE assigned_to = ? AND is_assigned = 1 
                ORDER BY assigned_at DESC""",
                (user_id,)
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting user numbers: {e}")
            return []

    @staticmethod
    async def get_number(number_id: int) -> Optional[Dict[str, Any]]:
        """Get number by ID"""
        try:
            row = await db.fetch_one(
                "SELECT * FROM numbers WHERE number_id = ?",
                (number_id,)
            )
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting number: {e}")
            return None

    @staticmethod
    async def recycle_number(number_id: int) -> bool:
        """Recycle a number (make it available again)"""
        try:
            await db.execute(
                """UPDATE numbers 
                SET is_assigned = 0, 
                    assigned_to = NULL,
                    assigned_at = NULL,
                    expires_at = NULL 
                WHERE number_id = ?""",
                (number_id,)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error recycling number: {e}")
            return False

    @staticmethod
    async def get_expired_numbers() -> list:
        """Get all expired numbers"""
        try:
            rows = await db.fetch_all(
                """SELECT * FROM numbers 
                WHERE is_assigned = 1 AND expires_at <= datetime('now')""",
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting expired numbers: {e}")
            return []
