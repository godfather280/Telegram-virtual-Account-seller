from pyrogram import filters
from database.users import get_user
from handlers.menu import main_menu

async def balance_callback(client, cq):
    if cq.data != "balance":
        return

    user = await get_user(cq.from_user.id)
    await cq.message.edit_text(
        f"💰 **Your Balance:** ₹{user['balance']}",
        reply_markup=main_menu()
    )

def setup(client):
    client.add_handler(filters.callback_query(balance_callback))
