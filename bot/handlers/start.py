from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.database.session import SessionLocal
from bot.keyboards.main_menu import main_menu
from bot.services.user_service import add_balance, get_or_create_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    args = message.text.split()
    referrer_id = None

    if len(args) > 1 and args[1].startswith("ref"):
        try:
            referrer_id = int(args[1][3:])
        except ValueError:
            referrer_id = None

    async with SessionLocal() as session:
        user, created = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            referred_by=referrer_id if referrer_id != message.from_user.id else None,
        )

        if created and referrer_id and referrer_id != message.from_user.id:
            from bot.config import settings
            await add_balance(session, referrer_id, settings.REFERRAL_BONUS)

    await message.answer(
        f"🐝 Welcome to <b>HaiiveBOT</b>, {message.from_user.first_name}!\n\n"
        f"Your balance: <b>{user.balance:.2f} USDT</b>\n\n"
        "Choose an option below:",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )
