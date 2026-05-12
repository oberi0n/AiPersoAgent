from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _csv_env(name: str) -> list[str]:
    return [item.strip() for item in os.getenv(name, "").split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    telegram_allowed_chat_id: int | None
    secondary_email_address: str
    primary_email_address: str
    imap_host: str
    imap_port: int
    imap_username: str
    imap_password: str
    imap_folder: str
    imap_search_query: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    check_interval_minutes: int
    database_url: str
    target_country: str
    target_cities: list[str]
    max_price: float
    min_surface: float
    required_keywords: list[str]
    excluded_keywords: list[str]
    paused: bool


def load_settings() -> Settings:
    chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID", "").strip()
    return Settings(
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        telegram_allowed_chat_id=int(chat_id) if chat_id else None,
        secondary_email_address=os.getenv("SECONDARY_EMAIL_ADDRESS", ""),
        primary_email_address=os.getenv("PRIMARY_EMAIL_ADDRESS", ""),
        imap_host=os.getenv("IMAP_HOST", "imap.gmail.com"),
        imap_port=int(os.getenv("IMAP_PORT", "993")),
        imap_username=os.getenv("IMAP_USERNAME", ""),
        imap_password=os.getenv("IMAP_PASSWORD", ""),
        imap_folder=os.getenv("IMAP_FOLDER", "INBOX"),
        imap_search_query=os.getenv("IMAP_SEARCH_QUERY", "UNSEEN"),
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_username=os.getenv("SMTP_USERNAME", ""),
        smtp_password=os.getenv("SMTP_PASSWORD", ""),
        check_interval_minutes=max(1, int(os.getenv("CHECK_INTERVAL_MINUTES", "10"))),
        database_url=os.getenv("DATABASE_URL", "sqlite:////data/agent.db"),
        target_country=os.getenv("TARGET_COUNTRY", "Spain"),
        target_cities=_csv_env("TARGET_CITIES"),
        max_price=float(os.getenv("MAX_PRICE", "100000")),
        min_surface=float(os.getenv("MIN_SURFACE", "20")),
        required_keywords=_csv_env("REQUIRED_KEYWORDS"),
        excluded_keywords=_csv_env("EXCLUDED_KEYWORDS"),
        paused=os.getenv("PAUSED", "false").strip().lower() == "true",
    )
