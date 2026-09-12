from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select

from bot.config import settings
from bot.database.models import User
from bot.database.session import SessionLocal

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        await message.answer("⛔ Not admin.")
        return
    await message.answer(
        "🛠 <b>Admin</b>\n\n"
        "/stats — bot stats\n"
        "/broadcast &lt;msg&gt; — send to all\n"
        "/seed — create default tasks",
        parse_mode="HTML",
    )


@router.message(Command("stats"))
async def stats(message: Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        return
    async with SessionLocal() as session:
        users = (await session.execute(select(User))).scalars().all()
    total = sum(u.balance for u in users)
    await message.answer(
        f"👥 Users: <b>{len(users)}</b>\n💰 Total balance: <b>{total:.2f} USDT</b>",
        parse_mode="HTML",
    )


@router.message(Command("seed"))
async def seed(message: Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        return
    from bot.database.models import Task

    default = [
        dict(code="join", icon="📢", title="Join our announcement",
             subtitle="Stay updated on new features",
             url="https://sharexosialx.com/g1LXEr6xw", reward=0.50),
        dict(code="ad", icon="📺", title="Watch a rewarded ad",
             subtitle="15 second video", url="", reward=0.10, once_per_day=True),
        dict(code="rate", icon="⭐", title="Rate the bot",
             subtitle="One-time bonus", url="", reward=0.30),
        dict(code="checkin", icon="✅", title="Daily check-in",
             subtitle="Come back every 24h", url="", reward=0.25,
             once_per_day=True),
    ]
    async with SessionLocal() as session:
        existing = (await session.execute(select(Task))).scalars().all()
        codes = {t.code for t in existing}
        for d in default:
            if d["code"] not in codes:
                session.add(Task(**d))
        await session.commit()
    await message.answer("✅ Tasks seeded.")
