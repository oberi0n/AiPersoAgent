import pytest

from app.safety import OutboundSafety, SafetyError


def test_safety_allows_primary_only():
    safety = OutboundSafety("primary@example.com")
    safety.validate_recipient("primary@example.com")


def test_safety_blocks_other_recipients():
    safety = OutboundSafety("primary@example.com")
    with pytest.raises(SafetyError):
        safety.validate_recipient("seller@example.com")
