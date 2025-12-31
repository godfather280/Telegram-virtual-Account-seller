from .db import db
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timedelta
from config import NUMBER_DURATION

logger = logging.getLogger(__name__)

class OrdersDB:
    @staticmethod
    async def create_order(user_id: int, number_id: int, account_id: int, price: int) -> Optional[int]:
        """Create a new order"""
        try:
            expires_at = datetime.now() + timedelta(seconds=NUMBER_DURATION)
            cursor = await db.execute(
                """INSERT INTO orders 
                (user_id, number_id, account_id, price, expires_at) 
                VALUES (?, ?, ?, ?, ?)""",
                (user_id, number_id, account_id, price, expires_at)
            )
            await db.conn.commit()
            order_id = cursor.lastrowid
            logger.info(f"Created order #{order_id} for user {user_id}")
            return order_id
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return None

    @staticmethod
    async def get_order(order_id: int) -> Optional[Dict[str, Any]]:
        """Get order by ID"""
        try:
            row = await db.fetch_one(
                "SELECT * FROM orders WHERE order_id = ?",
                (order_id,)
            )
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting order: {e}")
            return None

    @staticmethod
    async def update_otp(order_id: int, otp_code: str) -> bool:
        """Update OTP code for order"""
        try:
            await db.execute(
                "UPDATE orders SET otp_code = ? WHERE order_id = ?",
                (otp_code, order_id)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating OTP: {e}")
            return False

    @staticmethod
    async def get_active_orders(user_id: int) -> list:
        """Get user's active orders"""
        try:
            rows = await db.fetch_all(
                """SELECT * FROM orders 
                WHERE user_id = ? AND status = 'active' 
                AND expires_at > datetime('now') 
                ORDER BY created_at DESC""",
                (user_id,)
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting active orders: {e}")
            return []

    @staticmethod
    async def mark_expired(order_id: int) -> bool:
        """Mark order as expired"""
        try:
            await db.execute(
                "UPDATE orders SET status = 'expired' WHERE order_id = ?",
                (order_id,)
            )
            await db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error marking order expired: {e}")
            return False

    @staticmethod
    async def get_expired_orders() -> list:
        """Get all expired orders"""
        try:
            rows = await db.fetch_all(
                """SELECT * FROM orders 
                WHERE status = 'active' AND expires_at <= datetime('now')""",
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting expired orders: {e}")
            return []

    @staticmethod
    async def get_order_by_number(number_id: int) -> Optional[Dict[str, Any]]:
        """Get active order by number ID"""
        try:
            row = await db.fetch_one(
                """SELECT * FROM orders 
                WHERE number_id = ? AND status = 'active' 
                AND expires_at > datetime('now')""",
                (number_id,)
            )
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting order by number: {e}")
            return None
