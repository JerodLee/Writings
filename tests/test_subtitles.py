from app.services.subtitles import generate_srt


def test_generate_srt_format():
    srt = generate_srt("Line one. Line two.", duration=60)
    assert "1\n00:00:00,000 --> 00:00:30,000" in srt
    assert "2\n00:00:30,000 --> 00:01:00,000" in srt
