from __future__ import annotations

from typing import Any



def _fallback_script(topic: str, tone: str, duration: int, hook_bank: list[str]) -> dict[str, Any]:
    hook = hook_bank[0] if hook_bank else "Nobody talks about this money pattern."
    problem = f"{topic} is rarely about income alone."
    emotion = "It feels like running hard but standing still. Bills grow. Confidence shrinks."
    insight = (
        "Most people copy emergency behavior as a lifestyle. "
        "Real progress starts when spending becomes intentional and identity-driven."
    )
    ending = (
        f"Use {tone} today: track one leak, cut one impulse, and redirect one dollar toward your future self."
    )
    full_script = " ".join([hook, problem, emotion, insight, ending])
    return {
        "duration_target_seconds": duration,
        "hook": hook,
        "problem": problem,
        "emotion_example": emotion,
        "insight": insight,
        "ending": ending,
        "cta": "Comment 'RESET' if this hit you.",
        "full_script": full_script,
    }


def generate_script(llm: Any, topic: str, tone: str, duration: int, hook_bank: list[str]) -> dict[str, Any]:
    prompt = (
        "Write a US YouTube Shorts script in JSON with keys "
        "hook, problem, emotion_example, insight, ending, cta, full_script, duration_target_seconds. "
        f"Topic: {topic}. Tone: {tone}. Duration: {duration}. "
        "Short sentences. Emotional. No buy/sell advice."
    )
    model_out = llm.ask_json(prompt)
    if model_out and all(k in model_out for k in ["hook", "problem", "emotion_example", "insight", "ending"]):
        model_out["duration_target_seconds"] = duration
        return model_out
    return _fallback_script(topic, tone, duration, hook_bank)


def to_tts(script: dict[str, Any]) -> str:
    parts = [
        script["hook"],
        "[pause 300ms]",
        script["problem"],
        "[pause 250ms]",
        script["emotion_example"],
        "[pause 350ms]",
        script["insight"],
        "[pause 300ms]",
        script["ending"],
        script.get("cta", ""),
    ]
    return "\n".join([p for p in parts if p]).strip() + "\n"
