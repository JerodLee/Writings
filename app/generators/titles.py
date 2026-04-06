from __future__ import annotations

from typing import Any

from app.services.qa import sanitize_text



def _fallback_titles(topic: str, tone: str, n_titles: int) -> list[dict[str, Any]]:
    n_titles = max(5, n_titles)
    base = [
        f"The {tone.title()} Trap Keeping You Broke",
        f"Why {topic} Happens More Than You Think",
        "The Money Lie Most People Repeat Daily",
        "You’re Not Lazy. You’re Financially Conditioned",
        "This Habit Quietly Steals Your Future",
        "How Poor Thinking Becomes a Life Sentence",
        "The 60-Second Wake-Up Call for Your Wallet",
        "The Psychology Behind Staying Stuck Broke",
        "Comfort Today, Regret Tomorrow",
        "How Small Leaks Kill Big Dreams",
    ]
    results = []
    for i, text in enumerate(base[:n_titles]):
        score = round(9.1 - i * 0.24, 2)
        results.append(
            {
                "title": sanitize_text(text),
                "score": max(6.5, score),
                "reason": "Curiosity + emotional tension while staying non-scammy and safe.",
            }
        )
    return results


def _normalize_titles(raw_titles: list[dict[str, Any]], n_titles: int) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for item in raw_titles:
        title = sanitize_text(str(item.get("title", "")).strip())
        if not title:
            continue
        score = float(item.get("score", 7.5))
        reason = str(item.get("reason", "Clickable and emotionally resonant.")).strip()
        cleaned.append({"title": title, "score": round(score, 2), "reason": reason})
    if len(cleaned) < 5:
        return _fallback_titles("money mindset", "discipline", max(5, n_titles))
    return cleaned[: max(5, n_titles)]


def generate_titles(llm: Any, topic: str, tone: str, n_titles: int) -> list[dict[str, Any]]:
    n_titles = max(5, n_titles)
    prompt = (
        "Generate YouTube Shorts titles for US audience. "
        f"Topic: {topic}. Tone: {tone}. Return JSON object with key 'titles' list of "
        "{title, score, reason}. Must be 5+ items, non-scammy, no financial advice."
    )
    model_out = llm.ask_json(prompt)
    if model_out and isinstance(model_out.get("titles"), list):
        return _normalize_titles(model_out["titles"], n_titles)
    return _fallback_titles(topic, tone, n_titles)
