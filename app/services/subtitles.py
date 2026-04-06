from __future__ import annotations

from app.utils.text import split_sentences
from app.utils.timecode import to_srt_time



def generate_srt(narration: str, duration: int) -> str:
    sentences = split_sentences(narration)
    if not sentences:
        sentences = ["Stay focused. Build your financial discipline."]

    segment = duration / len(sentences)
    lines: list[str] = []
    current = 0.0
    for idx, sentence in enumerate(sentences, start=1):
        start = current
        end = duration if idx == len(sentences) else current + segment
        current = end
        lines.extend(
            [
                str(idx),
                f"{to_srt_time(start)} --> {to_srt_time(end)}",
                sentence,
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"
