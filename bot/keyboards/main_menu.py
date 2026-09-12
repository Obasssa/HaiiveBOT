from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💰 Wallet", callback_data="wallet"),
                InlineKeyboardButton(text="🎯 Tasks", callback_data="tasks"),
            ],
            [
                InlineKeyboardButton(text="🎁 Referral", callback_data="referral"),
                InlineKeyboardButton(text="👤 Profile", callback_data="profile"),
            ],
        ]
    )
