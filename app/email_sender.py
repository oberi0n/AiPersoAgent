from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from app.safety import OutboundSafety


def _render_summary(listings: list[dict]) -> str:
    template_path = Path(__file__).parent / "templates" / "summary_email.html"
    html = template_path.read_text(encoding="utf-8")
    items = "".join(
        f"<li><b>{l['title']}</b> - {l.get('price')}€ - {l.get('location')} - "
        f"{l.get('surface')}m² - <a href='{l['url']}'>Link</a></li>"
        for l in listings
    )
    return html.replace("{{LISTINGS}}", items or "<li>No matches this cycle.</li>")


def send_summary_email(settings, safety: OutboundSafety, listings: list[dict]) -> None:
    recipient = settings.primary_email_address
    safety.validate_recipient(recipient)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Real Estate Agent Summary ({len(listings)} matches)"
    msg["From"] = settings.secondary_email_address
    msg["To"] = recipient
    msg.attach(MIMEText(_render_summary(listings), "html", "utf-8"))

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.sendmail(settings.secondary_email_address, [recipient], msg.as_string())
