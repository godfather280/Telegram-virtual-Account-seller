from telegram import Update
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config import ADMIN_IDS, UPI_ID
from keyboards.admins import AdminKeyboards
from keyboards.main import MainKeyboards
from database.users import UserDB
from database.countries import CountryDB
from database.accounts import AccountDB
from database.numbers import NumberDB
from database.payments import PaymentDB

class AdminHandler:
    @staticmethod
    async def handle_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle admin panel access"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id not in ADMIN_IDS:
            await query.edit_message_text("❌ Access denied.")
            return
        
        await query.edit_message_text(
            "**Admin Panel**\n\nSelect an option:",
            parse_mode="Markdown",
            reply_markup=AdminKeyboards.admin_menu()
        )
    
    @staticmethod
    async def handle_admin_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle admin dashboard"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id not in ADMIN_IDS:
            await query.edit_message_text("❌ Access denied.")
            return
        
        # Get stats
        users_count = UserDB.get_users_count()
        countries = CountryDB.get_all_countries()
        accounts = AccountDB.get_all_accounts()
        numbers_stats = NumberDB.get_stats()
        payments_stats = PaymentDB.get_payments_stats()
        
        dashboard_text = f"""
**📊 Admin Dashboard**

👥 **Total Users:** {users_count}
🌍 **Countries:** {len(countries)}
📱 **Accounts:** {len(accounts)}
🔢 **Total Numbers:** {numbers_stats.get('total', 0)}
🟢 **Available Numbers:** {numbers_stats.get('available', 0)}
💰 **Total Revenue:** ₹{payments_stats.get('revenue', 0)}

**UPI ID:** `{UPI_ID}`
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="admin_dashboard"),
             InlineKeyboardButton("📈 Stats", callback_data="admin_stats")],
            [InlineKeyboardButton("➕ Add Resources", callback_data="admin_add")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        ]
        
        await query.edit_message_text(
            dashboard_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    @staticmethod
    async def handle_admin_add_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle admin add menu"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id not in ADMIN_IDS:
            await query.edit_message_text("❌ Access denied.")
            return
        
        await query.edit_message_text(
            "**Add Resources**\n\nWhat would you like to add?",
            parse_mode="Markdown",
            reply_markup=AdminKeyboards.admin_add_menu()
        )
    
    @staticmethod
    async def handle_countries_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle countries list"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id not in ADMIN_IDS:
            await query.edit_message_text("❌ Access denied.")
            return
        
        countries = CountryDB.get_all_countries()
        
        if not countries:
            await query.edit_message_text("No countries found.")
            return
        
        countries_text = "**Countries List:**\n\n"
        for country in countries:
            numbers = NumberDB.get_available_numbers(country['id'], limit=1000)
            from config import COUNTRY_RATES
            price = COUNTRY_RATES.get(country['name'], 10)
            countries_text += (
                f"{country['flag']} **{country['name']}**\n"
                f"Code: {country['code']}\n"
                f"Available Numbers: {len(numbers)}\n"
                f"Price: ₹{price}\n"
                f"━━━━━━━━━━━━━━\n"
            )
        
        await query.edit_message_text(
            countries_text,
            parse_mode="Markdown",
            reply_markup=AdminKeyboards.countries_list(countries)
        )
