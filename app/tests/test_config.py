from app.config import _parse_chat_id


def test_parse_chat_id_valid_int():
    assert _parse_chat_id("12345") == 12345


def test_parse_chat_id_invalid_token_like():
    assert _parse_chat_id("123:ABC") is None
