from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class AdminKeyboards:
    @staticmethod
    def admin_menu():
        keyboard = [
            [InlineKeyboardButton("📊 Dashboard", callback_data="admin_dashboard")],
            [
                InlineKeyboardButton("👥 Users", callback_data="admin_users"),
                InlineKeyboardButton("🌍 Countries", callback_data="admin_countries")
            ],
            [
                InlineKeyboardButton("📱 Accounts", callback_data="admin_accounts"),
                InlineKeyboardButton("🔢 Numbers", callback_data="admin_numbers")
            ],
            [
                InlineKeyboardButton("💰 Payments", callback_data="admin_payments"),
                InlineKeyboardButton("📈 Stats", callback_data="admin_stats")
            ],
            [InlineKeyboardButton("➕ Add Resources", callback_data="admin_add")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_add_menu():
        keyboard = [
            [InlineKeyboardButton("➕ Add Country", callback_data="add_country")],
            [InlineKeyboardButton("➕ Add Account", callback_data="add_account")],
            [InlineKeyboardButton("🔢 Generate Numbers", callback_data="generate_numbers")],
            [InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_panel")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def countries_list(countries):
        keyboard = []
        for country in countries[:15]:  # Show first 15
            keyboard.append([
                InlineKeyboardButton(
                    f"{country['flag']} {country['name']}",
                    callback_data=f"view_country_{country['id']}"
                )
            ])
        
        keyboard.append([
            InlineKeyboardButton("➕ Add New", callback_data="add_country"),
            InlineKeyboardButton("🔙 Back", callback_data="admin_panel")
        ])
        
        return InlineKeyboardMarkup(keyboard)
