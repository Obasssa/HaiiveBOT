from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User


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
    await session.commit()
    await session.refresh(user)
    return user, True


async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def add_balance(session: AsyncSession, telegram_id: int, amount: float):
    user = await get_user(session, telegram_id)
    if not user:
        return
    user.balance += amount
    await session.commit()
