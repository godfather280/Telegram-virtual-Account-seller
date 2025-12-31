from telegram import Update
from telegram.ext import ContextTypes
from database.users import UserDB
from config import WELCOME_MESSAGE
from keyboards.main import MainKeyboards

class StartHandler:
    @staticmethod
    async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        # Register user if not exists
        existing_user = UserDB.get_user(user.id)
        if not existing_user:
            UserDB.create_user(user.id, user.username)
        
        await update.message.reply_text(
            WELCOME_MESSAGE,
            parse_mode="Markdown",
            reply_markup=MainKeyboards.main_menu()
        )