import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Telegram
    BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")  # e.g. https://apextrade-bot.railway.app
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "apextrade_secure_2024")

    # Groq AI
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"   # سریع‌ترین و قوی‌ترین مدل رایگان
    GROQ_MAX_TOKENS: int = 1024

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # Admin
    ADMIN_IDS: list[int] = [
        int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
    ]

    # Rate limiting
    RATE_LIMIT_PER_HOUR: int = 30        # حداکثر پیام در ساعت
    MAX_CONVERSATION_HISTORY: int = 12   # تعداد پیام‌های تاریخچه

    # CoinGecko (رایگان)
    COINGECKO_API: str = "https://api.coingecko.com/api/v3"

    TELEGRAM_API: str = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN', '')}"


settings = Settings()
