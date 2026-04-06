from __future__ import annotations

import re
from typing import Any

BANNED_PHRASES = [
    "buy this now",
    "guaranteed profit",
    "risk-free money",
    "secret trick",
    "double your money overnight",
]

STRUCTURE_KEYS = ["hook", "problem", "emotion_example", "insight", "ending"]


def estimate_speech_duration_seconds(text: str, wpm: int = 150) -> float:
    words = len(text.split())
    return round((words / max(wpm, 1)) * 60, 2)


def find_banned_phrases(text: str) -> list[str]:
    lower = text.lower()
    return [phrase for phrase in BANNED_PHRASES if phrase in lower]


def sanitize_text(text: str) -> str:
    out = text
    replacements = {
        "buy this now": "start this now",
        "guaranteed profit": "possible upside",
        "risk-free money": "lower-risk approach",
        "secret trick": "practical habit",
        "double your money overnight": "build wealth over time",
    }
    for src, dst in replacements.items():
        out = re.sub(re.escape(src), dst, out, flags=re.IGNORECASE)
    return out


def qa_report(*, titles: list[dict[str, Any]], script: dict[str, Any], duration: int) -> dict[str, Any]:
    warnings: list[str] = []

    if len(titles) < 5:
        warnings.append("Less than 5 titles generated")

    if script.get("duration_target_seconds") != duration:
        warnings.append("Script duration metadata mismatch")

    missing = [k for k in STRUCTURE_KEYS if not script.get(k)]
    if missing:
        warnings.append(f"Missing structure blocks: {', '.join(missing)}")

    full_text = script.get("full_script", "")
    estimated = estimate_speech_duration_seconds(full_text)
    delta = abs(estimated - duration)
    if delta > 15:
        warnings.append(f"Estimated speech duration drift is high ({estimated}s vs target {duration}s)")

    combined_text = " ".join([t.get("title", "") for t in titles]) + " " + full_text
    banned_hits = find_banned_phrases(combined_text)
    if banned_hits:
        warnings.append(f"Banned phrases found: {', '.join(banned_hits)}")

    return {
        "checks": {
            "title_count": len(titles),
            "duration_target_seconds": duration,
            "estimated_duration_seconds": estimated,
            "duration_delta_seconds": round(delta, 2),
            "structure_valid": len(missing) == 0,
            "banned_phrases_found": banned_hits,
        },
        "warnings": warnings,
        "status": "pass" if not warnings else "warn",
    }
