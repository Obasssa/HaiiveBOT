from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Activity, User


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    referred_by: int | None = None,
) -> tuple[User, bool]:
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    if user:
        return user, False

    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        referred_by=referred_by,
    )
    session.add(user)
    await session.flush()

    if referred_by and referred_by != telegram_id:
        ref = (
            await session.execute(
                select(User).where(User.telegram_id == referred_by)
            )
        ).scalar_one_or_none()
        if ref:
            from bot.config import settings

            ref.invited_count += 1
            ref.referral_earned += settings.REFERRAL_BONUS
            ref.balance += settings.REFERRAL_BONUS
            ref.today_earned += settings.REFERRAL_BONUS
            session.add(
                Activity(
                    user_id=ref.telegram_id,
                    icon="👥",
                    label=f"Referral joined — @{username or 'user'}",
                    amount=settings.REFERRAL_BONUS,
                )
            )

    await session.commit()
    await session.refresh(user)
    return user, True


async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    return (
        await session.execute(select(User).where(User.telegram_id == telegram_id))
    ).scalar_one_or_none()


async def add_balance(
    session: AsyncSession,
    telegram_id: int,
    amount: float,
    icon: str = "🪙",
    label: str = "Reward",
):
    user = await get_user(session, telegram_id)
    if not user:
        return
    user.balance += amount
    user.today_earned += amount
    session.add(
        Activity(user_id=telegram_id, icon=icon, label=label, amount=amount)
    )
    await session.commit()
