from telegram import Update
from telegram.ext import ContextTypes
from database.users import UserDB
from database.payments import PaymentDB
from config import MIN_DEPOSIT, UPI_ID
from keyboards.deposit import DepositKeyboards
from keyboards.main import MainKeyboards
from services.payment import PaymentService

class DepositHandler:
    @staticmethod
    async def handle_deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle deposit amount selection"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "deposit_other":
            await query.edit_message_text(
                f"**Enter Deposit Amount**\n\n"
                f"Please enter the amount in INR (Minimum ₹{MIN_DEPOSIT})\n"
                f"Example: `100` or `500`\n\n"
                f"UPI ID: `{UPI_ID}`",
                parse_mode="Markdown",
                reply_markup=MainKeyboards.back_button("deposit")
            )
            context.user_data['awaiting_deposit_amount'] = True
        else:
            amount = int(query.data.split("_")[1])
            await DepositHandler.create_payment(update, context, amount)
    
    @staticmethod
    async def create_payment(update: Update, context: ContextTypes.DEFAULT_TYPE, amount):
        """Create payment for selected amount"""
        query = update.callback_query
        user = query.from_user
        user_data = UserDB.get_user(user.id)
        
        if not user_data:
            await query.edit_message_text("Please use /start first.")
            return
        
        if amount < MIN_DEPOSIT:
            await query.edit_message_text(
                f"❌ Minimum deposit is ₹{MIN_DEPOSIT}",
                reply_markup=DepositKeyboards.deposit_amounts()
            )
            return
        
        # Create payment record
        payment_id = PaymentDB.create_payment(user_data['id'], amount)
        
        if not payment_id:
            await query.edit_message_text(
                "❌ Failed to create payment. Please try again.",
                reply_markup=DepositKeyboards.deposit_amounts()
            )
            return
        
        # Generate QR code
        qr_image = PaymentService.generate_qr_code(amount, payment_id)
        instructions = PaymentService.get_payment_instructions(payment_id, amount)
        
        # Send QR code
        await query.message.reply_photo(
            photo=qr_image,
            caption=instructions,
            parse_mode="Markdown"
        )
        
        await query.edit_message_text(
            f"**Payment Created**\n\n"
            f"**Payment ID:** `{payment_id}`\n"
            f"**Amount:** ₹{amount}\n"
            f"**UPI ID:** `{UPI_ID}`\n\n"
            f"Scan the QR code or send ₹{amount} to the UPI ID above.\n"
            f"After payment, send your UTR here.",
            parse_mode="Markdown",
            reply_markup=MainKeyboards.back_button("main_menu")
        )
        
        # Store payment info
        context.user_data['payment_info'] = {
            'payment_id': payment_id,
            'amount': amount,
            'user_id': user_data['id']
        }