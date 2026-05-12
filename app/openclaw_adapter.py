from __future__ import annotations


def interpret_command(text: str) -> dict:
    return {"enabled": False, "reason": "OpenClaw adapter placeholder", "input": text}


def summarize_listing(listing) -> str:
    return f"{listing.title} | {listing.price}€ | {listing.location}"
