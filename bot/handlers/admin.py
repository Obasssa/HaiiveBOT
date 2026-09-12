from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select

from bot.config import settings
from bot.database.models import User, Withdrawal
from bot.database.session import SessionLocal

router = Router()


def _is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not _is_admin(message.from_user.id):
        await message.answer("⛔ Not admin.")
        return
    await message.answer(
        "🛠 <b>Admin</b>\n\n"
        "/stats — bot stats\n"
        "/withdrawals — pending withdrawals\n"
        "/broadcast &lt;msg&gt; — send to all\n"
        "/seed — create default tasks",
        parse_mode="HTML",
    )


@router.message(Command("stats"))
async def stats(message: Message):
    if not _is_admin(message.from_user.id):
        return
    async with SessionLocal() as session:
        users = (await session.execute(select(User))).scalars().all()
    total = sum(u.balance for u in users)
    await message.answer(
        f"👥 Users: <b>{len(users)}</b>\n💰 Total balance: <b>{total:.2f} USDT</b>",
        parse_mode="HTML",
    )


@router.message(Command("withdrawals"))
async def withdrawals(message: Message):
    if not _is_admin(message.from_user.id):
        return
    async with SessionLocal() as session:
        rows = (
            await session.execute(
                select(Withdrawal)
                .where(Withdrawal.status == "pending")
                .order_by(Withdrawal.created_at.desc())
                .limit(20)
            )
        ).scalars().all()

    if not rows:
        await message.answer("No pending withdrawals.")
        return

    text = "💸 <b>Pending withdrawals</b>\n\n"
    for w in rows:
        text += (
            f"#{w.id} • <code>{w.user_id}</code>\n"
            f"   {w.amount:.2f} USDT → <code>{w.address}</code>\n"
            f"   {w.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
        )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("seed"))
async def seed(message: Message):
    if not _is_admin(message.from_user.id):
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
