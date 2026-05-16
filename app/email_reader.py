from __future__ import annotations

import email
import imaplib
from email.header import decode_header


def _decode_header(value: str | None) -> str:
    if not value:
        return ""
    output: list[str] = []
    for content, encoding in decode_header(value):
        if isinstance(content, bytes):
            output.append(content.decode(encoding or "utf-8", errors="ignore"))
        else:
            output.append(content)
    return "".join(output)


def fetch_emails(settings) -> list[dict]:
    mails: list[dict] = []
    with imaplib.IMAP4_SSL(settings.imap_host, settings.imap_port) as imap:
        imap.login(settings.imap_username, settings.imap_password)
        imap.select(settings.imap_folder)

        status, ids = imap.search(None, settings.imap_search_query)
        if status != "OK":
            return mails

        for msg_id in ids[0].split():
            status, data = imap.fetch(msg_id, "(RFC822)")
            if status != "OK" or not data or not data[0]:
                continue

            msg = email.message_from_bytes(data[0][1])
            body_text, body_html = "", ""
            if msg.is_multipart():
                for part in msg.walk():
                    payload = part.get_payload(decode=True) or b""
                    ctype = part.get_content_type()
                    charset = part.get_content_charset() or "utf-8"
                    text = payload.decode(charset, errors="ignore")
                    if ctype == "text/plain":
                        body_text += text
                    elif ctype == "text/html":
                        body_html += text
            else:
                payload = msg.get_payload(decode=True) or b""
                body_text = payload.decode(msg.get_content_charset() or "utf-8", errors="ignore")

            mails.append(
                {
                    "message_id": msg.get("Message-ID", str(msg_id)),
                    "subject": _decode_header(msg.get("Subject")),
                    "from": _decode_header(msg.get("From")),
                    "body_text": body_text,
                    "body_html": body_html,
                }
            )
    return mails
