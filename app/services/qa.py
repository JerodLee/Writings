from __future__ import annotations

from typing import Any

BANNED_PHRASES = [
    "buy this now",
    "guaranteed profit",
    "risk-free money",
    "secret trick",
]


def qa_report(*, titles: list[dict[str, Any]], script: dict[str, Any], duration: int) -> dict[str, Any]:
    warnings: list[str] = []

    if len(titles) < 5:
        warnings.append("Less than 5 titles generated")

    if script.get("duration_target_seconds") != duration:
        warnings.append("Script duration metadata mismatch")

    structure_keys = ["hook", "problem", "emotion_example", "insight", "ending"]
    missing = [k for k in structure_keys if not script.get(k)]
    if missing:
        warnings.append(f"Missing structure blocks: {', '.join(missing)}")

    combined_text = " ".join([t["title"] for t in titles]) + " " + script.get("full_script", "")
    banned_hits = [p for p in BANNED_PHRASES if p in combined_text.lower()]
    if banned_hits:
        warnings.append(f"Banned phrases found: {', '.join(banned_hits)}")

    return {
        "checks": {
            "title_count": len(titles),
            "duration_target_seconds": duration,
            "structure_valid": len(missing) == 0,
            "banned_phrases_found": banned_hits,
        },
        "warnings": warnings,
        "status": "pass" if not warnings else "warn",
    }
