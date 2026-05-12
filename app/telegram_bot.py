from __future__ import annotations

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


class AgentTelegramBot:
    def __init__(self, settings, state):
        self.settings = settings
        self.state = state
        self.application = Application.builder().token(settings.telegram_bot_token).build()
        self._register_handlers()

    async def _guard(self, update: Update) -> bool:
        if self.settings.telegram_allowed_chat_id is None:
            return True
        return bool(update.effective_chat and update.effective_chat.id == self.settings.telegram_allowed_chat_id)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._guard(update):
            return
        await update.message.reply_text("Real estate agent ready.")

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._guard(update):
            return
        await update.message.reply_text(f"Paused: {self.state['paused']}")

    async def criteria(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._guard(update):
            return
        s = self.settings
        await update.message.reply_text(f"Cities: {', '.join(s.target_cities)} | Max: {s.max_price} | Min m2: {s.min_surface}")

    async def last(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._guard(update):
            return
        await update.message.reply_text(self.state.get("last_notification", "No matches yet."))

    async def pause(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._guard(update):
            return
        self.state["paused"] = True
        await update.message.reply_text("Paused.")

    async def resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._guard(update):
            return
        self.state["paused"] = False
        await update.message.reply_text("Resumed.")

    async def test(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._guard(update):
            return
        await update.message.reply_text("Test OK.")

    def _register_handlers(self) -> None:
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("criteria", self.criteria))
        self.application.add_handler(CommandHandler("last", self.last))
        self.application.add_handler(CommandHandler("pause", self.pause))
        self.application.add_handler(CommandHandler("resume", self.resume))
        self.application.add_handler(CommandHandler("test", self.test))

    async def notify_listing(self, listing: dict, reason: str):
        chat_id = self.settings.telegram_allowed_chat_id
        if not chat_id:
            return
        message = (
            f"✅ Match\n{listing['title']}\nPrice: {listing.get('price')}€\n"
            f"Location: {listing.get('location')}\nSurface: {listing.get('surface')}m²\n"
            f"Source: {listing.get('source')}\nURL: {listing.get('url')}\nReason: {reason}"
        )
        self.state["last_notification"] = message
        await self.application.bot.send_message(chat_id=chat_id, text=message)
