import asyncio
from datetime import datetime, timedelta
import random
import string
from typing import Optional

def format_time(seconds: int) -> str:
    """Format seconds to MM:SS"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def format_balance(amount: int) -> str:
    """Format balance with currency symbol"""
    return f"₹{amount}"

def generate_random_id(length: int = 8) -> str:
    """Generate random ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def format_datetime(dt: datetime) -> str:
    """Format datetime to readable string"""
    return dt.strftime("%d %b %Y, %I:%M %p")

def calculate_expiry_time(duration_seconds: int) -> tuple:
    """Calculate expiry time and remaining seconds"""
    expiry_time = datetime.now() + timedelta(seconds=duration_seconds)
    remaining = (expiry_time - datetime.now()).seconds
    return expiry_time, remaining

async def safe_reply(client, message, text: str, **kwargs):
    """Safely reply to a message, handling errors"""
    try:
        return await message.reply(text, **kwargs)
    except Exception as e:
        try:
            return await client.send_message(message.chat.id, text, **kwargs)
        except:
            return None

async def delete_message_after(client, chat_id: int, message_id: int, delay: int):
    """Delete message after delay"""
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, message_id)
    except:
        pass
