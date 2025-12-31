from .db import db
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class CountriesDB:
    @staticmethod
    async def add_country(country_code: str, country_name: str, price: int) -> bool:
        """Add a new country"""
        try:
            await db.execute(
                """INSERT OR REPLACE INTO countries 
                (country_code, country_name, price) 
                VALUES (?, ?, ?)""",
                (country_code, country_name, price)
            )
            await db.conn.commit()
            logger.info(f"Added country: {country_name} ({country_code}) - ₹{price}")
            return True
        except Exception as e:
            logger.error(f"Error adding country: {e}")
            return False

    @staticmethod
    async def get_country(country_code: str) -> Optional[Dict[str, Any]]:
        """Get country by code"""
        try:
            row = await db.fetch_one(
                "SELECT * FROM countries WHERE country_code = ? AND is_active = 1",
                (country_code,)
            )
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting country: {e}")
            return None

    @staticmethod
    async def get_all_countries() -> List[Dict[str, Any]]:
        """Get all active countries"""
        try:
            rows = await db.fetch_all(
                "SELECT * FROM countries WHERE is_active = 1 ORDER BY country_name"
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting countries: {e}")
            return []

    @staticmethod
    async def get_price(country_code: str) -> Optional[int]:
        """Get price for a country"""
        try:
            country = await CountriesDB.get_country(country_code)
            return country['price'] if country else None
        except Exception as e:
            logger.error(f"Error getting price: {e}")
            return None

    @staticmethod
    async def enable_country(country_code: str) -> bool:
        """Enable a country"""
        try:
            await db.execute(
                "UPDATE countries SET is_active = 1 WHERE country_code = ?",
                (country_code,)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error enabling country: {e}")
            return False

    @staticmethod
    async def disable_country(country_code: str) -> bool:
        """Disable a country"""
        try:
            await db.execute(
                "UPDATE countries SET is_active = 0 WHERE country_code = ?",
                (country_code,)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error disabling country: {e}")
            return False

    @staticmethod
    async def update_price(country_code: str, price: int) -> bool:
        """Update country price"""
        try:
            await db.execute(
                "UPDATE countries SET price = ? WHERE country_code = ?",
                (price, country_code)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating price: {e}")
            return False
