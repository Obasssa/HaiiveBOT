import asyncio

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.database.session import init_db
from bot.handlers import admin, profile, referral, start, tasks, wallet
from bot.utils.logger import logger


async def main():
    logger.info("Starting HaiiveBOT...")
    await init_db()

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(wallet.router)
    dp.include_router(tasks.router)
    dp.include_router(referral.router)
    dp.include_router(profile.router)
    dp.include_router(admin.router)

    logger.info("🐝 HaiiveBOT is live!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
