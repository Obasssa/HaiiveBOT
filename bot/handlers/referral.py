from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "referral")
async def show_referral(callback: CallbackQuery):
    bot_info = await callback.bot.get_me()
    link = f"https://t.me/{bot_info.username}?start=ref{callback.from_user.id}"

    await callback.message.edit_text(
        f"🎁 <b>Referral Program</b>\n\n"
        f"Earn <b>0.10 USDT</b> for each friend you invite!\n\n"
        f"Your link:\n<code>{link}</code>",
        parse_mode="HTML",
    )
    await callback.answer()
