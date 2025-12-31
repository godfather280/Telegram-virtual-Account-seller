from .db import db
from datetime import datetime

class UserDB:
    @staticmethod
    def get_user(telegram_id):
        """Get user by Telegram ID"""
        return db.fetch_one(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
    
    @staticmethod
    def create_user(telegram_id, username):
        """Create new user"""
        db.execute_query(
            "INSERT INTO users (telegram_id, username) VALUES (?, ?)",
            (telegram_id, username)
        )
        return UserDB.get_user(telegram_id)
    
    @staticmethod
    def update_balance(user_id, amount):
        """Update user balance"""
        db.execute_query(
            "UPDATE users SET balance = balance + ? WHERE id = ?",
            (amount, user_id)
        )
        
        if amount > 0:
            db.execute_query(
                "UPDATE users SET total_deposits = total_deposits + ? WHERE id = ?",
                (amount, user_id)
            )
        else:
            db.execute_query(
                "UPDATE users SET total_spent = total_spent + ? WHERE id = ?",
                (abs(amount), user_id)
            )
        
        return True
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by database ID"""
        return db.fetch_one(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
    
    @staticmethod
    def get_all_users(limit=100):
        """Get all users"""
        return db.fetch_all(
            "SELECT * FROM users ORDER BY id DESC LIMIT ?",
            (limit,)
        )
    
    @staticmethod
    def get_users_count():
        """Get total users count"""
        result = db.fetch_one("SELECT COUNT(*) as count FROM users")
        return result['count'] if result else 0
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user fields"""
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(user_id)
        
        db.execute_query(
            f"UPDATE users SET {set_clause} WHERE id = ?",
            values
        )
        return True