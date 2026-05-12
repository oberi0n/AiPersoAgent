from __future__ import annotations


class SafetyError(Exception):
    pass


class OutboundSafety:
    def __init__(self, primary_email: str):
        self.allowed_recipients = {primary_email.strip().lower()}

    def validate_recipient(self, recipient: str) -> None:
        normalized = recipient.strip().lower()
        if normalized not in self.allowed_recipients:
            raise SafetyError(
                f"Blocked outbound email to '{recipient}'. Only PRIMARY_EMAIL_ADDRESS is permitted."
            )
