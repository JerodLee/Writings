from __future__ import annotations

from typing import Any

from app.services.qa import sanitize_text



def _fit_script_length(text: str, duration: int) -> str:
    target_words = max(90, min(220, int(duration * 2.3)))
    words = text.split()
    if len(words) > target_words:
        return " ".join(words[:target_words]).rstrip(".,;:!?") + "."
    return text


def _fallback_script(
    topic: str,
    tone: str,
    duration: int,
    hook_bank: list[str],
    template_order: list[str] | None = None,
) -> dict[str, Any]:
    hook = hook_bank[0] if hook_bank else "Nobody talks about this money pattern."
    sections = {
        "hook": sanitize_text(hook),
        "problem": sanitize_text(f"{topic} is usually a behavior trap, not just a paycheck problem."),
        "emotion_example": "You work all week. Then stress hits. One tap. One order. Another month feels gone.",
        "insight": (
            "The real shift starts when you stop using money to numb emotion and start using it to build identity."
        ),
        "ending": (
            f"Choose {tone} today: track one leak, cut one impulse, and move one dollar toward future freedom."
        ),
        "cta": "Comment 'RESET' if you're done with survival mode.",
    }

    order = template_order or ["hook", "problem", "emotion_example", "insight", "ending", "cta"]
    full_script = " ".join(sections[k] for k in order if k in sections)
    full_script = _fit_script_length(sanitize_text(full_script), duration)

    return {
        "duration_target_seconds": duration,
        "hook": sections["hook"],
        "problem": sections["problem"],
        "emotion_example": sections["emotion_example"],
        "insight": sections["insight"],
        "ending": sections["ending"],
        "cta": sections["cta"],
        "full_script": full_script,
    }


def generate_script(
    llm: Any,
    topic: str,
    tone: str,
    duration: int,
    hook_bank: list[str],
    template_order: list[str] | None = None,
) -> dict[str, Any]:
    prompt = (
        "Write a US YouTube Shorts script in JSON with keys "
        "hook, problem, emotion_example, insight, ending, cta, full_script, duration_target_seconds. "
        f"Topic: {topic}. Tone: {tone}. Duration: {duration}. "
        "Short sentences. Emotional. No buy/sell advice."
    )
    model_out = llm.ask_json(prompt)
    if model_out and all(k in model_out for k in ["hook", "problem", "emotion_example", "insight", "ending"]):
        model_out["duration_target_seconds"] = duration
        model_out["full_script"] = _fit_script_length(sanitize_text(model_out.get("full_script", "")), duration)
        for key in ["hook", "problem", "emotion_example", "insight", "ending", "cta"]:
            if key in model_out and isinstance(model_out[key], str):
                model_out[key] = sanitize_text(model_out[key])
        return model_out
    return _fallback_script(topic, tone, duration, hook_bank, template_order)


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
    return "\n".join([p.strip() for p in parts if p and p.strip()]).strip() + "\n"
