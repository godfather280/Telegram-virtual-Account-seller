from datetime import datetime
from database.numbers import NumberDB
from database.payments import PaymentDB
from database.orders import OrderDB
import logging

logger = logging.getLogger(__name__)

class CleanupService:
    @staticmethod
    def run_cleanup():
        """Run all cleanup tasks"""
        try:
            # Clean expired numbers
            expired_numbers = NumberDB.expire_numbers()
            if expired_numbers > 0:
                logger.info(f"Expired {expired_numbers} numbers")
            
            # Clean expired payments
            expired_payments = PaymentDB.clean_expired_payments()
            if expired_payments > 0:
                logger.info(f"Cleaned {expired_payments} expired payments")
            
            # Clean expired orders
            expired_orders = OrderDB.expire_old_orders()
            if expired_orders > 0:
                logger.info(f"Expired {expired_orders} old orders")
            
            return {
                'expired_numbers': expired_numbers,
                'expired_payments': expired_payments,
                'expired_orders': expired_orders
            }
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            return None
