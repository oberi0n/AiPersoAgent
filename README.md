# real-estate-agent-spain

Safe, Dockerized real estate prospecting agent focused on Spain.

## What it does
- Reads property alert emails from a **secondary mailbox** via IMAP.
- Parses candidate listings from email content (HTML/text).
- Applies rule-based filtering from `.env` criteria.
- Deduplicates listings by URL/hash.
- Stores processed emails and listings in SQLite.
- Sends Telegram notifications for each match.
- Sends summary emails **only** to `PRIMARY_EMAIL_ADDRESS` from the secondary mailbox.
- Never sends emails to sellers/third parties.

## Setup
1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Fill `.env` values.
3. Run:
   ```bash
   docker compose up --build
   ```

## Telegram bot token
1. Open Telegram and chat with **@BotFather**.
2. Create bot using `/newbot`.
3. Paste token into `TELEGRAM_BOT_TOKEN`.
4. Get your chat ID (e.g. using @userinfobot) and set `TELEGRAM_ALLOWED_CHAT_ID`.

## Email configuration
### Gmail
- Enable 2FA.
- Create an App Password.
- Use app password in `IMAP_PASSWORD` and `SMTP_PASSWORD`.
- Typical hosts: `imap.gmail.com:993`, `smtp.gmail.com:587`.

### Generic IMAP/SMTP
- Set provider host/port/user/pass values in `.env`.
- Keep `SECONDARY_EMAIL_ADDRESS` as the sender mailbox.
- Optional `IMAP_SEARCH_QUERY` lets you use a different IMAP search expression (default `UNSEEN`).

## .env configuration
See `.env.example` for all variables, including:
- Filtering: `TARGET_CITIES`, `MAX_PRICE`, `MIN_SURFACE`, `REQUIRED_KEYWORDS`, `EXCLUDED_KEYWORDS`
- Runtime: `CHECK_INTERVAL_MINUTES`, `DATABASE_URL`, `PAUSED`

## Telegram commands
- `/start`
- `/status`
- `/criteria`
- `/last`
- `/pause`
- `/resume`
- `/test`

## Local tests
```bash
pytest -q
```

## Safety limitations
- Recipient allowlist contains **only** `PRIMARY_EMAIL_ADDRESS`.
- Any other outbound recipient raises an exception.
- No seller-contact feature exists.
- Telegram has no command to send arbitrary emails.

## Legal note
This system does **not** scrape websites by default. It processes only emails already received by the user.
