import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite+aiosqlite:///./haiive.db"
    )
    ADMIN_IDS: list[int] = [
        int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
    ]
    REFERRAL_BONUS: float = float(os.getenv("REFERRAL_BONUS", "0.10"))

    def validate(self):
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is missing in environment variables")


settings = Settings()
settings.validate()
