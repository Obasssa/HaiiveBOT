from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.session import SessionLocal
from bot.services.user_service import get_user

router = Router()


@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery):
    async with SessionLocal() as session:
        user = await get_user(session, callback.from_user.id)

    await callback.message.edit_text(
        f"👤 <b>Profile</b>\n\n"
        f"ID: <code>{user.telegram_id}</code>\n"
        f"Username: @{user.username or '—'}\n"
        f"Balance: <b>{user.balance:.2f} USDT</b>\n"
        f"Invited: <b>{user.invited_count}</b>\n"
        f"Referral earned: <b>{user.referral_earned:.2f} USDT</b>",
        parse_mode="HTML",
    )
    await callback.answer()
