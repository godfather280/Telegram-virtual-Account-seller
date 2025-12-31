from telegram import Update
from telegram.ext import ContextTypes
from config import WELCOME_MESSAGE
from keyboards.main import MainKeyboards
from keyboards.buy import BuyKeyboards
from keyboards.deposit import DepositKeyboards

class MenuHandler:
    @staticmethod
    async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle main menu callback"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            WELCOME_MESSAGE,
            parse_mode="Markdown",
            reply_markup=MainKeyboards.main_menu()
        )
    
    @staticmethod
    async def handle_buy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle buy menu callback"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "**Select Country:**\n\nChoose a country to see available numbers.",
            parse_mode="Markdown",
            reply_markup=BuyKeyboards.countries_menu()
        )
    
    @staticmethod
    async def handle_deposit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle deposit menu callback"""
        query = update.callback_query
        await query.answer()
        
        from config import MIN_DEPOSIT, UPI_ID
        
        await query.edit_message_text