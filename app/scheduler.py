from __future__ import annotations

import asyncio
import hashlib

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from app.email_reader import fetch_emails
from app.email_sender import send_summary_email
from app.filters import apply_filters
from app.models import Listing, ProcessedEmail
from app.parser import extract_listings


class AgentScheduler:
    def __init__(self, settings, db, bot, safety, state):
        self.settings = settings
        self.db = db
        self.bot = bot
        self.safety = safety
        self.state = state
        self.scheduler = BackgroundScheduler()

    @staticmethod
    def _dedupe_key(listing: dict) -> str:
        base = listing.get("url") or listing.get("title", "") + listing.get("raw_text", "")
        return hashlib.sha256(base.encode("utf-8", errors="ignore")).hexdigest()

    def run_cycle(self) -> None:
        if self.state.get("paused"):
            return

        emails = fetch_emails(self.settings)
        matched_for_summary = []

        with self.db.session() as session:
            for mail in emails:
                existing = session.scalar(
                    select(ProcessedEmail).where(ProcessedEmail.message_id == mail["message_id"])
                )
                if existing:
                    continue

                session.add(
                    ProcessedEmail(
                        message_id=mail["message_id"],
                        subject=mail["subject"],
                        sender=mail["from"],
                    )
                )

                listings = extract_listings(mail["subject"], mail["body_html"], mail["body_text"], mail["from"])
                for listing in listings:
                    key = self._dedupe_key(listing)
                    if session.scalar(select(Listing).where(Listing.dedupe_key == key)):
                        continue
                    matched, reason = apply_filters(listing, self.settings)
                    db_listing = Listing(dedupe_key=key, matched=matched, match_reason=reason, **listing)
                    session.add(db_listing)
                    if matched:
                        matched_for_summary.append(listing | {"reason": reason})

        if matched_for_summary:
            for listing in matched_for_summary:
                asyncio.run(self.bot.notify_listing(listing, listing["reason"]))
            send_summary_email(self.settings, self.safety, matched_for_summary)

    def start(self) -> None:
        self.scheduler.add_job(self.run_cycle, "interval", minutes=self.settings.check_interval_minutes)
        self.scheduler.start()
