from __future__ import annotations

import logging

from app.config import load_settings
from app.db import Database
from app.safety import OutboundSafety
from app.scheduler import AgentScheduler
from app.telegram_bot import AgentTelegramBot

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def main() -> None:
    settings = load_settings()
    db = Database(settings.database_url)
    db.init_db()

    state = {"paused": settings.paused, "last_notification": "No matches yet."}
    safety = OutboundSafety(settings.primary_email_address)
    bot = AgentTelegramBot(settings, state)
    scheduler = AgentScheduler(settings, db, bot, safety, state)
    scheduler.start()

    bot.application.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
