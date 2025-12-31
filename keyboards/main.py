from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class MainKeyboards:
    @staticmethod
    def main_menu():
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Number", callback_data="buy_number")],
            [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
            [InlineKeyboardButton("📊 Balance", callback_data="balance")],
            [InlineKeyboardButton("📱 My Numbers", callback_data="my_numbers")],
            [InlineKeyboardButton("🆘 Help", callback_data="help")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_button(back_to="main_menu"):
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data=back_to)]]
        return InlineKeyboardMarkup(keyboard)