from telegram import Update
from telegram.ext import ContextTypes
from database.users import UserDB
from database.orders import OrderDB
from datetime import datetime
from keyboards.main import MainKeyboards

class MyNumbersHandler:
    @staticmethod
    async def handle_my_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle my numbers request"""
        query = update.callback_query
        await query.answer()
        
        user = query.from_user
        user_data = UserDB.get_user(user.id)
        
        if not user_data:
            await query.edit_message_text("Please use /start first.")
            return
        
        orders = OrderDB.get_user_orders(user_data['id'])
        
        if not orders:
            await query.edit_message_text(
                "📭 **No Active Numbers**\n\n"
                "You don't have any active numbers.\n"
                "Click '🛒 Buy Number' to purchase one.",
                reply_markup=MainKeyboards.main_menu()
            )
            return
        
        numbers_text = "**Your Active Numbers:**\n\n"
        for order in orders:
            expiry = datetime.fromisoformat(order['expiry_date']) if order['expiry_date'] else None
            if expiry:
                time_left = expiry - datetime.now()
                minutes_left = max(0, int(time_left.total_seconds() / 60))
                expiry_text = f"⏰ Expires in: {minutes_left} minutes"
            else:
                expiry_text = "⏰ Expiry: Unknown"
            
            numbers_text += (
                f"📞 `{order['number']}`\n"
                f"🌍 {order['country_flag']} {order['country_name']}\n"
                f"{expiry_text}\n"
                f"━━━━━━━━━━━━━━\n"
            )
        
        await query.edit_message_text(
            numbers_text,
            parse_mode="Markdown",
            reply_markup=MainKeyboards.main_menu()
        )