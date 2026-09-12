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
        f"👤 <b>Your Profile</b>\n\n"
        f"ID: <code>{user.telegram_id}</code>\n"
        f"Username: @{user.username or 'N/A'}\n"
        f"Balance: <b>{user.balance:.2f} USDT</b>\n"
        f"Referred by: {user.referred_by or 'Nobody'}\n"
        f"Joined: {user.created_at.strftime('%Y-%m-%d')}",
        parse_mode="HTML",
    )
    await callback.answer()
