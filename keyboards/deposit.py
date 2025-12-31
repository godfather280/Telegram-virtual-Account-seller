from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import MIN_DEPOSIT

class DepositKeyboards:
    @staticmethod
    def deposit_amounts():
        keyboard = [
            [InlineKeyboardButton("₹50", callback_data="deposit_50"),
             InlineKeyboardButton("₹100", callback_data="deposit_100")],
            [InlineKeyboardButton("₹200", callback_data="deposit_200"),
             InlineKeyboardButton("₹500", callback_data="deposit_500")],
            [InlineKeyboardButton("₹1000", callback_data="deposit_1000"),
             InlineKeyboardButton("Other Amount", callback_data="deposit_other")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirm_cancel():
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)