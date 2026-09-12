from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import settings

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        await message.answer("⛔ You are not an admin.")
        return

    await message.answer(
        "🛠 <b>Admin Panel</b>\n\n"
        "/stats — bot statistics\n"
        "/broadcast &lt;message&gt; — send to all users",
        parse_mode="HTML",
    )
