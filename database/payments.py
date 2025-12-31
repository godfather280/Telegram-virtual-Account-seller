from .db import db
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timedelta
from config import MIN_DEPOSIT

logger = logging.getLogger(__name__)

class PaymentsDB:
    @staticmethod
    async def create_payment(user_id: int, amount: int) -> Optional[int]:
        """Create a new payment record"""
        try:
            if amount < MIN_DEPOSIT:
                return None

            expires_at = datetime.now() + timedelta(minutes=30)
            cursor = await db.execute(
                """INSERT INTO payments (user_id, amount, expires_at, status) 
                VALUES (?, ?, ?, 'pending')""",
                (user_id, amount, expires_at)
            )
            await db.conn.commit()
            payment_id = cursor.lastrowid
            logger.info(f"Created payment #{payment_id} for user {user_id}: ₹{amount}")
            return payment_id
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            return None

    @staticmethod
    async def get_payment(payment_id: int) -> Optional[Dict[str, Any]]:
        """Get payment by ID"""
        try:
            row = await db.fetch_one(
                "SELECT * FROM payments WHERE payment_id = ?",
                (payment_id,)
            )
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting payment: {e}")
            return None

    @staticmethod
    async def verify_utr(payment_id: int, utr: str) -> bool:
        """Verify UTR and mark payment as completed"""
        try:
            # Check if UTR already exists
            existing = await db.fetch_one(
                "SELECT payment_id FROM payments WHERE utr = ?",
                (utr,)
            )
            if existing:
                return False

            await db.execute(
                """UPDATE payments 
                SET utr = ?, status = 'completed', verified_at = CURRENT_TIMESTAMP 
                WHERE payment_id = ? AND status = 'pending'""",
                (utr, payment_id)
            )
            await db.conn.commit()
            logger.info(f"Verified UTR for payment #{payment_id}: {utr}")
            return True
        except Exception as e:
            logger.error(f"Error verifying UTR: {e}")
            return False

    @staticmethod
    async def check_expiry(payment_id: int) -> bool:
        """Check if payment is expired"""
        try:
            payment = await PaymentsDB.get_payment(payment_id)
            if not payment:
                return True

            if payment['status'] != 'pending':
                return True

            expires_at = datetime.fromisoformat(payment['expires_at'])
            return datetime.now() > expires_at
        except Exception as e:
            logger.error(f"Error checking expiry: {e}")
            return True

    @staticmethod
    async def get_user_payments(user_id: int, limit: int = 10) -> list:
        """Get user's payment history"""
        try:
            rows = await db.fetch_all(
                """SELECT * FROM payments 
                WHERE user_id = ? 
                ORDER BY created_at DESC LIMIT ?""",
                (user_id, limit)
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting user payments: {e}")
            return []

    @staticmethod
    async def get_all_payments(limit: int = 50) -> list:
        """Get all payments"""
        try:
            rows = await db.fetch_all(
                "SELECT * FROM payments ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all payments: {e}")
            return []

    @staticmethod
    async def get_pending_payments() -> list:
        """Get all pending payments"""
        try:
            rows = await db.fetch_all(
                """SELECT * FROM payments 
                WHERE status = 'pending' AND expires_at > datetime('now')""",
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting pending payments: {e}")
            return []
