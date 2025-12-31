from telegram import Update
from telegram.ext import ContextTypes
from database.countries import CountryDB
from database.numbers import NumberDB
from database.accounts import AccountDB
from database.users import UserDB
from database.orders import OrderDB
from config import COUNTRY_RATES
from keyboards.buy import BuyKeyboards
from keyboards.main import MainKeyboards

class BuyHandler:
    @staticmethod
    async def handle_country_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle country selection"""
        query = update.callback_query
        await query.answer()
        
        country_id = int(query.data.split("_")[1])
        country = CountryDB.get_country(country_id)
        
        if not country:
            await query.edit_message_text("Country not found.")
            return
        
        await query.edit_message_text(
            f"**{country['flag']} {country['name']} - Available Numbers**\n\n"
            f"Price per number: ₹{COUNTRY_RATES.get(country['name'], 10)}\n"
            f"Duration: 10 minutes\n\n"
            f"Select a number:",
            parse_mode="Markdown",
            reply_markup=BuyKeyboards.numbers_menu(country_id)
        )
    
    @staticmethod
    async def handle_number_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle number selection"""
        query = update.callback_query
        await query.answer()
        
        number_id = int(query.data.split("_")[2])
        number = NumberDB.get_number(number_id)
        
        if not number:
            await query.edit_message_text("Number not found.")
            return
        
        country = CountryDB.get_country(number['country_id'])
        price = COUNTRY_RATES.get(country['name'], 10)
        
        await query.edit_message_text(
            f"**Number Details**\n\n"
            f"📞 **Number:** `{number['number']}`\n"
            f"🌍 **Country:** {country['flag']} {country['name']}\n"
            f"💰 **Price:** ₹{price}\n"
            f"⏰ **Duration:** 10 minutes\n\n"
            f"**Note:** You will receive OTPs automatically.\n"
            f"Number expires 10 minutes after purchase.",
            parse_mode="Markdown",
            reply_markup=BuyKeyboards.confirm_purchase(number_id, price)
        )
    
    @staticmethod
    async def handle_purchase_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle purchase confirmation"""
        query = update.callback_query
        await query.answer()
        
        number_id = int(query.data.split("_")[2])
        user = query.from_user
        user_data = UserDB.get_user(user.id)
        
        if not user_data:
            await query.edit_message_text("Please use /start first.")
            return
        
        number = NumberDB.get_number(number_id)
        if not number:
            await query.edit_message_text("Number not found.")
            return
        
        country = CountryDB.get_country(number['country_id'])
        price = COUNTRY_RATES.get(country['name'], 10)
        
        # Check balance
        if user_data['balance'] < price:
            from keyboards.deposit import DepositKeyboards
            await query.edit_message_text(
                f"❌ **Insufficient Balance**\n\n"
                f"Required: ₹{price}\n"
                f"Your Balance: ₹{user_data['balance']}\n\n"
                f"Please deposit first.",
                reply_markup=DepositKeyboards.deposit_amounts()
            )
            return
        
        # Find available account
        account = AccountDB.get_available_account(country['id'])
        if not account:
            await query.edit_message_text(
                f"❌ **Temporarily Unavailable**\n\n"
                f"No accounts available for {country['name']}.\n"
                f"Please try another country or contact support.",
                reply_markup=BuyKeyboards.countries_menu()
            )
            return
        
        # Process purchase
        price = NumberDB.purchase_number(number_id, user_data['id'], account['id'])
        
        if price:
            # Update user balance
            UserDB.update_balance(user_data['id'], -price)
            
            # Create order
            OrderDB.create_order(user_data['id'], number_id, price)
            
            # Get updated user data
            user_data = UserDB.get_user(user.id)
            
            await query.edit_message_text(
                f"✅ **Purchase Successful!**\n\n"
                f"📞 **Number:** `{number['number']}`\n"
                f"🌍 **Country:** {country['flag']} {country['name']}\n"
                f"💰 **Amount:** ₹{price}\n"
                f"⏰ **Expires:** In 10 minutes\n"
                f"💳 **New Balance:** ₹{user_data['balance']}\n\n"
                f"**OTPs will be forwarded here automatically.**\n"
                f"Keep this chat open to receive OTPs.",
                parse_mode="Markdown",
                reply_markup=MainKeyboards.main_menu()
            )
        else:
            await query.edit_message_text(
                "❌ **Purchase Failed**\n\n"
                "An error occurred. Please try again or contact support.",
                reply_markup=MainKeyboards.main_menu()
            )
    
    @staticmethod
    async def handle_cancel_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle purchase cancellation"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "Purchase cancelled.",
            reply_markup=MainKeyboards.main_menu()
        )