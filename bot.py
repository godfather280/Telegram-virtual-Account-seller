#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

# Import handlers
from handlers.start import StartHandler
from handlers.menu import MenuHandler
from handlers.buy import BuyHandler
from handlers.deposit import DepositHandler
from handlers.balance import BalanceHandler
from handlers.my_numbers import MyNumbersHandler
from handlers.admin import AdminHandler
from handlers.messages import MessageHandler

# Import config
from config import BOT_TOKEN, ADMIN_IDS, UPI_ID
from utils.logger import logger
from services.cleanup import CleanupService

class VirtualNumbersBot:
    def __init__(self):
        self.application = None
    
    def setup_handlers(self):
        """Setup all bot handlers"""
        
        # Command handlers
        self.application.add_handler(CommandHandler("start", StartHandler.handle_start))
        self.application.add_handler(CommandHandler("help", self.handle_help))
        self.application.add_handler(CommandHandler("admin", self.handle_admin_command))
        
        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(MenuHandler.handle_main_menu, pattern="^main_menu$"))
        self.application.add_handler(CallbackQueryHandler(MenuHandler.handle_buy_menu, pattern="^buy_number$"))
        self.application.add_handler(CallbackQueryHandler(MenuHandler.handle_deposit_menu, pattern="^deposit$"))
        self.application.add_handler(CallbackQueryHandler(BalanceHandler.handle_balance, pattern="^balance$"))
        self.application.add_handler(CallbackQueryHandler(MyNumbersHandler.handle_my_numbers, pattern="^my_numbers$"))
        self.application.add_handler(CallbackQueryHandler(self.handle_help_callback, pattern="^help$"))
        
        # Buy flow handlers
        self.application.add_handler(CallbackQueryHandler(BuyHandler.handle_country_selection, pattern="^country_"))
        self.application.add_handler(CallbackQueryHandler(BuyHandler.handle_number_selection, pattern="^select_number_"))
        self.application.add_handler(CallbackQueryHandler(BuyHandler.handle_purchase_confirmation, pattern="^confirm_buy_"))
        self.application.add_handler(CallbackQueryHandler(BuyHandler.handle_cancel_buy, pattern="^cancel_buy$"))
        
        # Deposit flow handlers
        self.application.add_handler(CallbackQueryHandler(DepositHandler.handle_deposit_amount, pattern="^deposit_"))
        
        # Admin handlers
        self.application.add_handler(CallbackQueryHandler(AdminHandler.handle_admin_panel, pattern="^admin_panel$"))
        self.application.add_handler(CallbackQueryHandler(AdminHandler.handle_admin_dashboard, pattern="^admin_dashboard$"))
        self.application.add_handler(CallbackQueryHandler(AdminHandler.handle_admin_add_menu, pattern="^admin_add$"))
        self.application.add_handler(CallbackQueryHandler(AdminHandler.handle_countries_list, pattern="^admin_countries$"))
        
        # Message handler
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, MessageHandler.handle_message))
        
        logger.info("All handlers setup completed")
    
    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        from config import HELP_MESSAGE, UPI_ID, SUPPORT_CHAT
        await update.message.reply_text(
            HELP_MESSAGE.format(upi_id=UPI_ID, support_chat=SUPPORT_CHAT),
            parse_mode="Markdown"
        )
    
    async def handle_help_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle help callback"""
        query = update.callback_query
        await query.answer()
        
        from config import HELP_MESSAGE, UPI_ID, SUPPORT_CHAT
        from keyboards.main import MainKeyboards
        
        await query.edit_message_text(
            HELP_MESSAGE.format(upi_id=UPI_ID, support_chat=SUPPORT_CHAT),
            parse_mode="Markdown",
            reply_markup=MainKeyboards.back_button()
        )
    
    async def handle_admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command"""
        from config import ADMIN_IDS
        from keyboards.admins import AdminKeyboards
        
        if update.effective_user.id in ADMIN_IDS:
            await update.message.reply_text(
                "**Admin Panel**\n\nSelect an option:",
                parse_mode="Markdown",
                reply_markup=AdminKeyboards.admin_menu()
            )
        else:
            await update.message.reply_text("❌ Access denied.")
    
    async def cleanup_task(self, context: ContextTypes.DEFAULT_TYPE):
        """Periodic cleanup task"""
        logger.info("Running cleanup task...")
        result = CleanupService.run_cleanup()
        if result:
            logger.info(f"Cleanup completed: {result}")
    
    def run(self):
        """Run the bot"""
        # Check if bot token is set
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("❌ ERROR: Please set your BOT_TOKEN in config.py!")
            print("Get it from @BotFather and replace 'YOUR_BOT_TOKEN_HERE'")
            return
        
        # Create application
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Setup handlers
        self.setup_handlers()
        
        # Setup periodic cleanup
        job_queue = self.application.job_queue
        if job_queue:
            from config import NUMBER_EXPIRY_CHECK_INTERVAL
            job_queue.run_repeating(
                self.cleanup_task,
                interval=NUMBER_EXPIRY_CHECK_INTERVAL,
                first=10
            )
            logger.info(f"Cleanup scheduled every {NUMBER_EXPIRY_CHECK_INTERVAL} seconds")
        
        # Initialize database
        from database.db import db
        logger.info("Database initialized")
        
        # Start the bot
        logger.info("🤖 Bot starting...")
        print(f"👑 Admin IDs: {ADMIN_IDS}")
        print(f"💰 UPI ID: {UPI_ID}")
        print("🚀 Bot is running. Press Ctrl+C to stop.")
        
       