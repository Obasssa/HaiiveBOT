from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from bot.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    # Import models so they're registered
    from bot.database import models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await _seed_default_tasks()


async def _seed_default_tasks():
    """Ensures the default tasks exist for every user."""
    from bot.database.models import Task

    defaults = [
        dict(
            code="join",
            icon="📢",
            title="Join our announcement",
            subtitle="Stay updated on new features",
            url="https://sharexosialx.com/g1LXEr6xw",
            reward=0.50,
            once_per_day=False,
        ),
        dict(
            code="ad",
            icon="📺",
            title="Watch a rewarded ad",
            subtitle="15 second video",
            url="",
            reward=0.10,
            once_per_day=True,
        ),
        dict(
            code="rate",
            icon="⭐",
            title="Rate the bot",
            subtitle="One-time bonus",
            url="",
            reward=0.30,
            once_per_day=False,
        ),
        dict(
            code="checkin",
            icon="✅",
            title="Daily check-in",
            subtitle="Come back every 24h",
            url="",
            reward=0.25,
            once_per_day=True,
        ),
    ]

    async with SessionLocal() as session:
        existing = (await session.execute(select(Task))).scalars().all()
        existing_codes = {t.code for t in existing}
        added = False
        for d in defaults:
            if d["code"] not in existing_codes:
                session.add(Task(**d))
                added = True
        if added:
            await session.commit()


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
