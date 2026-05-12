# real-estate-agent-spain

Safe, Dockerized real estate prospecting agent focused on Spain.

## What it does
- Uses a built-in OpenClaw adapter in the matching workflow (mandatory).
- Reads property alert emails from a **secondary mailbox** via IMAP.
- Parses candidate listings from email content (HTML/text).
- Applies rule-based filtering from `.env` criteria.
- Deduplicates listings by URL/hash.
- Stores processed emails and listings in SQLite.
- Sends Telegram notifications for each match.
- Sends summary emails **only** to `PRIMARY_EMAIL_ADDRESS` from the secondary mailbox.
- Never sends emails to sellers/third parties.

## Setup (all-in-one Docker package)
1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Fill `.env` values.
3. Run (everything starts inside Docker):
   ```bash
   docker compose up --build
   ```
4. Optional legacy command:
   ```bash
   docker-compose up --build
   ```

After this, the app will:
- Poll the secondary mailbox via IMAP
- Parse/filter/deduplicate listings
- Send Telegram match alerts
- Send summary emails only to `PRIMARY_EMAIL_ADDRESS`

## One-time requirements
- Create the two email accounts (primary + secondary).
- Ensure IMAP/SMTP are enabled on the **secondary** mailbox.
- Put credentials in `.env`.

## Telegram bot token
1. Open Telegram and chat with **@BotFather**.
2. Create bot using `/newbot`.
3. Paste token into `TELEGRAM_BOT_TOKEN`.
4. Get your chat ID (for example via @userinfobot) and set `TELEGRAM_ALLOWED_CHAT_ID`.

## Email configuration
### Free.fr (recommended for your use case)
- Use `imap.free.fr:993` and `smtp.free.fr:587` (already set in `.env.example`).
- Set:
  - `SECONDARY_EMAIL_ADDRESS` = mailbox used for alerts + sending summary.
  - `PRIMARY_EMAIL_ADDRESS` = your private mailbox receiving summaries.
  - `IMAP_USERNAME` / `SMTP_USERNAME` = secondary email login.
  - `IMAP_PASSWORD` / `SMTP_PASSWORD` = secondary email password.
- No MFA is required by your stated setup.

### Gmail (optional alternative)
- Override host values in `.env` to `imap.gmail.com` and `smtp.gmail.com`.
- Gmail usually requires 2FA + App Password.

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

## OpenClaw
OpenClaw is included and used directly by the scheduler for listing summaries, so no extra service is required.
