from __future__ import annotations

from typing import Any



def _fallback_titles(topic: str, tone: str, n_titles: int) -> list[dict[str, Any]]:
    base = [
        f"The {tone.title()} Trap Keeping You Broke",
        f"Why {topic} Happens More Than You Think",
        "The Money Lie Most People Repeat Daily",
        "You’re Not Lazy. You’re Financially Conditioned",
        "This Habit Quietly Steals Your Future",
        "How Poor Thinking Becomes a Life Sentence",
        "The 60-Second Wake-Up Call for Your Wallet",
        "The Psychology Behind Staying Stuck Broke",
    ]
    results = []
    for i, text in enumerate(base[: max(5, n_titles)]):
        score = round(8.8 - i * 0.3, 2)
        results.append(
            {
                "title": text,
                "score": score,
                "reason": "High curiosity and emotional tension without scammy phrasing.",
            }
        )
    return results[:n_titles]


def generate_titles(llm: Any, topic: str, tone: str, n_titles: int) -> list[dict[str, Any]]:
    prompt = (
        "Generate YouTube Shorts titles for US audience. "
        f"Topic: {topic}. Tone: {tone}. Return JSON object with key 'titles' list of "
        "{title, score, reason}. Must be 5+ items, non-scammy, no financial advice."
    )
    model_out = llm.ask_json(prompt)
    if model_out and isinstance(model_out.get("titles"), list) and len(model_out["titles"]) >= 5:
        return model_out["titles"][:n_titles]
    return _fallback_titles(topic, tone, n_titles)
