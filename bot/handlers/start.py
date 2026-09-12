from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.database.session import SessionLocal
from bot.handlers.tasks import _render_tasks
from bot.keyboards.main_menu import bottom_menu, wallet_inline
from bot.services.user_service import get_or_create_user

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
        user, _ = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            referred_by=referrer_id,
        )

    await message.answer(
        f"🐝 <b>Welcome to HaiiveBOT</b>\n\n"
        f"<b>Available balance</b>\n"
        f"<b>{user.balance:,.2f} USDT</b>\n"
        f"▲ {user.today_earned:.2f} today",
        reply_markup=bottom_menu(),
        parse_mode="HTML",
    )

    await message.answer("Quick actions:", reply_markup=wallet_inline())

    await _render_tasks(message.from_user.id, message.answer)
