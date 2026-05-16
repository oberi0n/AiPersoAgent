from __future__ import annotations

import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def _to_float(value: str) -> float | None:
    cleaned = re.sub(r"[^\d,\.]", "", value).replace(".", "").replace(",", ".")
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def extract_listings(subject: str, body_html: str, body_text: str, sender: str) -> list[dict]:
    text = f"{subject}\n{body_text}"
    soup = BeautifulSoup(body_html or "", "lxml")
    urls = [a.get("href", "") for a in soup.find_all("a", href=True)]
    if not urls:
        urls = re.findall(r"https?://\S+", text)

    price_match = re.search(r"(\d{2,3}(?:[\.,]\d{3})+)\s*€", text)
    surface_match = re.search(r"(\d{1,3}(?:[\.,]\d+)?)\s*(?:m²|m2)", text, flags=re.I)

    location = ""
    loc_match = re.search(r"(?:en|in)\s+([A-Za-zÁÉÍÓÚáéíóúñÑ\s-]{3,50})", text)
    if loc_match:
        location = loc_match.group(1).strip()

    title = subject.strip() or "Property listing"
    price = _to_float(price_match.group(1)) if price_match else None
    surface = _to_float(surface_match.group(1)) if surface_match else None

    listings = []
    for url in urls:
        domain = urlparse(url).netloc or sender
        listings.append(
            {
                "title": title,
                "price": price,
                "location": location,
                "surface": surface,
                "url": url,
                "source": domain,
                "raw_text": text[:4000],
            }
        )
    return listings
