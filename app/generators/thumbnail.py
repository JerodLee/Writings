from __future__ import annotations

from typing import Any



def generate_thumbnail_copy(llm: Any, topic: str, tone: str) -> dict[str, Any]:
    prompt = (
        "Return JSON {phrases:[...]} with 5-8 short thumbnail phrases (2-6 words), emotional, "
        f"topic={topic}, tone={tone}, US audience."
    )
    out = llm.ask_json(prompt)
    if out and isinstance(out.get("phrases"), list) and len(out["phrases"]) >= 5:
        return out
    return {
        "phrases": [
            "Broke By Design?",
            "Wake Up Financially",
            "Stop Leaking Money",
            "Your Habits Are Expensive",
            "Escape Survival Mode",
            "Future You Is Watching",
        ]
    }
