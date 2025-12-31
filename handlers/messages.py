from telegram import Update
from telegram.ext import ContextTypes
from database.users import UserDB
from database.payments import PaymentDB
from config import ADMIN_IDS, UPI_ID
from keyboards.main import MainKeyboards
from keyboards.deposit import DepositKeyboards

class MessageHandler:
    @staticmethod
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user = update.effective_user
        text = update.message.text.strip()
        
        # Check if user is in deposit state
        if 'awaiting_deposit_amount' in context.user_data:
            try:
                amount = int(text)
                from config import MIN_DEPOSIT
                if amount < MIN_DEPOSIT:
                    await update.message.reply_text(
                        f"❌ Minimum deposit is ₹{MIN_DEPOSIT}\n"
                        f"Please enter a valid amount:",
                        reply_markup=MainKeyboards.back_button("deposit")
                    )
                    return
                
                # Process payment creation
                user_data = UserDB.get_user(user.id)
                if not user_data:
                    await update.message.reply_text("Please use /start first.")
                    return
                
                payment_id = PaymentDB.create_payment(user_data['id'], amount)
                if not payment_id:
                    await update.message.reply_text(
                        "❌ Failed to create payment. Please try again.",
                        reply_markup=DepositKeyboards.deposit_amounts()
                    )
                    return
                
                # Generate QR code
                from services.payment import PaymentService
                qr_image = PaymentService.generate_qr_code(amount, payment_id)
                instructions = PaymentService.get_payment_instructions(payment_id, amount)
                
                # Send QR code
                await update.message.reply_photo(
                    photo=qr_image,
                    caption=instructions,
                    parse_mode="Markdown"
                )
                
                await update.message.reply_text(
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
                del context.user_data['awaiting_deposit_amount']
                
            except ValueError:
                await update.message.reply_text(
                    "❌ Please enter a valid number (e.g., 100, 500)",
                    reply_markup=MainKeyboards.back_button("deposit")
                )
            return
        
        # Check if user has payment info (awaiting UTR)
        if 'payment_info' in context.user_data:
            payment_info = context.user_data['payment_info']
            payment_id = payment_info['payment_id']
            
            # Verify payment with UTR
            success, message = PaymentDB.verify_payment(payment_id, text)
            
            if success:
                user_data = UserDB.get_user_by_id(payment_info['user_id'])
                await update.message.reply_text(
                    f"✅ **Payment Verified!**\n\n"
                    f"**Amount:** ₹{payment_info['amount']}\n"
                    f"**New Balance:** ₹{user_data['balance']}\n\n"
                    f"Thank you for your payment!",
                    parse_mode="Markdown",
                    reply_markup=MainKeyboards.main_menu()
                )
                
                # Notify admin
                for admin_id in ADMIN_IDS:
                    try:
                        await context.bot.send_message(
                            admin_id,
                            f"💰 Payment Verified\n"
                            f"User: @{user.username or user.id}\n"
                            f"Amount: ₹{payment_info['amount']}\n"
                            f"UTR: {text}"
                        )
                    except:
                        pass
            else:
                await update.message.reply_text(
                    f"❌ **Payment Verification Failed**\n\n{message}",
                    reply_markup=MainKeyboards.main_menu()
                )
            
            del context.user_data['payment_info']
            return
        
        # Handle other messages
        await update.message.reply_text(
            "Please use the menu buttons or commands.\n"
            "Type /help for assistance.",
            reply_markup=MainKeyboards.main_menu()
        )