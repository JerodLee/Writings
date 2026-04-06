from app.services.qa import find_banned_phrases, sanitize_text


def test_sanitize_and_banned_phrase_detection():
    raw = "This is a guaranteed profit and buy this now message"
    clean = sanitize_text(raw)
    assert "guaranteed profit" not in clean.lower()
    assert "buy this now" not in clean.lower()
    assert find_banned_phrases(clean) == []
