from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OpenClawAdapter:
    """Built-in OpenClaw-compatible adapter used by the core workflow."""

    model_name: str = "openclaw-rule-engine"

    def interpret_command(self, text: str) -> dict:
        lowered = (text or "").strip().lower()
        if lowered in {"pause", "/pause"}:
            return {"action": "pause", "confidence": 1.0}
        if lowered in {"resume", "/resume"}:
            return {"action": "resume", "confidence": 1.0}
        if lowered in {"status", "/status"}:
            return {"action": "status", "confidence": 1.0}
        return {"action": "unknown", "confidence": 0.0, "raw": text}

    def summarize_listing(self, listing: dict) -> str:
        title = listing.get("title", "Untitled")
        price = listing.get("price", "?")
        location = listing.get("location", "?")
        surface = listing.get("surface", "?")
        return f"{title} | {price}€ | {location} | {surface}m²"
