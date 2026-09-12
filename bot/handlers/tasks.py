from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "tasks")
async def show_tasks(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎯 <b>Available Tasks</b>\n\n"
        "• Join our channel — 0.05 USDT\n"
        "• Invite 3 friends — 0.15 USDT\n"
        "• Daily check-in — 0.02 USDT\n\n"
        "More tasks coming soon!",
        parse_mode="HTML",
    )
    await callback.answer()
