from __future__ import annotations


def apply_filters(listing: dict, settings) -> tuple[bool, str]:
    reasons = []
    text_blob = f"{listing.get('title', '')} {listing.get('location', '')} {listing.get('raw_text', '')}".lower()

    if listing.get("price") is None or listing["price"] > settings.max_price:
        return False, "price too high or missing"
    reasons.append(f"price <= {settings.max_price:.0f}")

    if listing.get("surface") is None or listing["surface"] < settings.min_surface:
        return False, "surface too low or missing"
    reasons.append(f"surface >= {settings.min_surface:.0f}")

    if settings.target_cities and not any(city.lower() in text_blob for city in settings.target_cities):
        return False, "city mismatch"
    reasons.append("city matched")

    if settings.required_keywords:
        missing = [k for k in settings.required_keywords if k.lower() not in text_blob]
        if missing:
            return False, f"missing required keywords: {', '.join(missing)}"
        reasons.append("required keywords matched")

    blocked = [k for k in settings.excluded_keywords if k.lower() in text_blob]
    if blocked:
        return False, f"excluded keywords present: {', '.join(blocked)}"

    return True, "; ".join(reasons)
