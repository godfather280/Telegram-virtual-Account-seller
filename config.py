import os
from typing import List

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")

# Admin Configuration
ADMIN_IDS: List[int] = []
try:
    admin_ids_str = os.getenv("ADMIN_IDS", "")
    if admin_ids_str:
        ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(",")]
except:
    pass

# Payment Configuration
UPI_ID = os.getenv("UPI_ID", "")
MIN_DEPOSIT = int(os.getenv("MIN_DEPOSIT", 100))

# Number Configuration
NUMBER_DURATION = int(os.getenv("NUMBER_DURATION", 600))  # 10 minutes in seconds
NUMBER_PRICE = int(os.getenv("NUMBER_PRICE", 50))  # Default price in INR

# Database
DB_NAME = os.getenv("DB_NAME", "virtual_numbers.db")

# Cleanup
CLEANUP_INTERVAL = int(os.getenv("CLEANUP_INTERVAL", 300))  # 5 minutes

# Regex patterns
OTP_REGEX = r'\b\d{4,6}\b'
UTR_REGEX = r'^[A-Za-z0-9]{10,20}$'

# Session settings
SESSION_FOLDER = "sessions/accounts"
