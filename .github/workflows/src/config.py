from zoneinfo import ZoneInfo
import os

# Timezone
IST = ZoneInfo("Asia/Kolkata")

# Domains to fetch via Google News RSS
NEWS_DOMAINS = [
    "moneycontrol.com",
    "economictimes.indiatimes.com",
    "livemint.com",
    "business-standard.com",
    "nseindia.com",
]

LOOKBACK_HOURS = int(os.getenv("LOOKBACK_HOURS", "36"))

# Email
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMAIL_TO  = os.getenv("EMAIL_TO", "")

# Telegram
ENABLE_TELEGRAM = os.getenv("ENABLE_TELEGRAM", "false").lower() in {"1", "true", "yes"}
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

DB_PATH = os.getenv("DB_PATH", "ai_agent.db")

# Scoring weights
WEIGHT_BY_DOMAIN = {
    "nseindia.com": 1.5,
    "business-standard.com": 1.2,
    "livemint.com": 1.2,
    "economictimes.indiatimes.com": 1.0,
    "moneycontrol.com": 1.0,
}
DEFAULT_DOMAIN_WEIGHT = 1.0
