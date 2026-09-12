from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.database.session import SessionLocal
from bot.keyboards.main_menu import referral_inline
from bot.services.user_service import get_user

router = Router()


@router.message(F.text == "👥 Invite")
async def invite_msg(message: Message):
    await _render(message, message.answer)


@router.callback_query(F.data == "referral")
async def invite_cb(callback: CallbackQuery):
    await _render(callback, callback.message.edit_text)
    await callback.answer()


async def _render(event, sender):
    user_id = event.from_user.id
    bot_info = await event.bot.get_me()

    async with SessionLocal() as session:
        user = await get_user(session, user_id)

    link = f"https://t.me/{bot_info.username}?start=ref{user.telegram_id}"
    text = (
        "👥 <b>Invite friends</b>\n"
        "Earn 10% of what your referrals make, forever.\n\n"
        f"🔗 <code>{link}</code>\n\n"
        f"👥 <b>{user.invited_count}</b>      💰 <b>{user.referral_earned:.2f}</b>\n"
        f"     Invited           Earned"
    )

    markup = referral_inline(bot_info.username, user.telegram_id)
    await sender(text, reply_markup=markup, parse_mode="HTML")
