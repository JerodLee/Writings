from __future__ import annotations

from typing import Any

from app.utils.text import split_sentences


TRANSITIONS = ["cut", "zoom", "flash", "swipe up", "glitch", "fade"]



def generate_scenes(
    llm: Any,
    script: dict[str, Any],
    n_scenes: int,
    duration: int,
) -> list[dict[str, Any]]:
    n_scenes = max(6, min(10, n_scenes))
    prompt = (
        "Return JSON {scenes:[...]} for YouTube Shorts edit plan with fields narration,on_screen_text,"
        "stock_keywords,ai_image_prompt,duration,emotion,transition. "
        f"Scenes={n_scenes} duration={duration}. Narration: {script['full_script']}"
    )
    model_out = llm.ask_json(prompt)
    if model_out and isinstance(model_out.get("scenes"), list) and len(model_out["scenes"]) >= 6:
        return model_out["scenes"][:n_scenes]

    chunks = split_sentences(script["full_script"])
    while len(chunks) < n_scenes:
        chunks.append(chunks[-1])
    per_scene = round(duration / n_scenes, 2)
    scenes = []
    for i in range(n_scenes):
        narration = chunks[i % len(chunks)]
        scenes.append(
            {
                "scene": i + 1,
                "narration": narration,
                "on_screen_text": narration[:64],
                "stock_keywords": ["money stress", "city night", "thinking person", "discipline"],
                "ai_image_prompt": "cinematic portrait, financial pressure, moody lighting, vertical 9:16",
                "duration": per_scene,
                "emotion": "intense" if i < 3 else "determined",
                "transition": TRANSITIONS[i % len(TRANSITIONS)],
            }
        )
    return scenes


def build_edit_plan(scenes: list[dict[str, Any]], srt_file: str) -> dict[str, Any]:
    timeline = []
    cursor = 0.0
    for scene in scenes:
        start = cursor
        end = round(cursor + float(scene["duration"]), 2)
        cursor = end
        timeline.append(
            {
                "scene": scene["scene"],
                "start": start,
                "end": end,
                "voiceover": scene["narration"],
                "subtitle_source": srt_file,
                "visual": {
                    "stock_keywords": scene["stock_keywords"],
                    "ai_image_prompt": scene["ai_image_prompt"],
                    "transition": scene["transition"],
                },
                "format": "9:16",
            }
        )
    return {
        "project": "shorts-mvp",
        "aspect_ratio": "9:16",
        "timeline": timeline,
        "export_notes": "Compatible with FFmpeg, CapCut, and manual NLE workflows.",
    }
