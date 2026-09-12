import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.user_service import get_user


async def get_balance(session: AsyncSession, telegram_id: int) -> float:
    user = await get_user(session, telegram_id)
    return user.balance if user else 0.0


async def generate_deposit_address(telegram_id: int) -> str:
    """
    Placeholder: In production, integrate Tron/EVM wallet generation.
    Never generate real keys in plain text without encryption.
    """
    return "T" + secrets.token_hex(16).upper()[:33]
