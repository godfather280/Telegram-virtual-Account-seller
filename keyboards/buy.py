from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.countries import CountryDB
from database.numbers import NumberDB
from config import COUNTRY_RATES

class BuyKeyboards:
    @staticmethod
    def countries_menu():
        countries = CountryDB.get_all_countries()
        keyboard = []
        
        for country in countries:
            numbers = NumberDB.get_available_numbers(country['id'], limit=1)
            price = COUNTRY_RATES.get(country['name'], 10)
            btn_text = f"{country['flag']} {country['name']} - ₹{price} ({len(numbers)} available)"
            keyboard.append([
                InlineKeyboardButton(btn_text, callback_data=f"country_{country['id']}")
            ])
        
        keyboard.append([
            InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def numbers_menu(country_id):
        numbers = NumberDB.get_available_numbers(country_id, limit=15)
        country = CountryDB.get_country(country_id)
        price = COUNTRY_RATES.get(country['name'], 10)
        
        keyboard = []
        for number in numbers:
            keyboard.append([
                InlineKeyboardButton(
                    f"📞 {number['number']} - ₹{price}",
                    callback_data=f"select_number_{number['id']}"
                )
            ])
        
        keyboard.append([
            InlineKeyboardButton("🔙 Back to Countries", callback_data="buy_number")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirm_purchase(number_id, price):
        keyboard = [
            [
                InlineKeyboardButton(f"✅ Buy - ₹{price}", callback_data=f"confirm_buy_{number_id}"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_buy")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)