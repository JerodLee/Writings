from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import AppConfig
from app.generators.scenes import build_edit_plan, generate_scenes
from app.generators.script import generate_script, to_tts
from app.generators.thumbnail import generate_thumbnail_copy
from app.generators.titles import generate_titles
from app.services.llm import LLMService
from app.services.qa import qa_report
from app.services.subtitles import generate_srt
from app.utils.files import ensure_dir, load_json, write_json, write_text
from app.utils.slug import slugify


logger = logging.getLogger(__name__)


class ShortsPipeline:
    def __init__(self, config: AppConfig, dry_run: bool = False):
        self.config = config
        self.dry_run = dry_run
        self.llm = LLMService(config.openai_api_key, config.openai_model, dry_run=dry_run)

    def run(
        self,
        *,
        topic: str,
        tone: str,
        duration: int,
        n_titles: int,
        n_scenes: int,
        output_dir: str | None,
    ) -> Path:
        slug = slugify(topic)
        root_out = Path(output_dir) if output_dir else self.config.default_output_dir / slug
        ensure_dir(root_out)

        hooks = load_json(self.config.data_dir / "hook_library.json")
        _ = load_json(self.config.data_dir / "topic_ideas.json")
        _ = load_json(self.config.data_dir / "tone_rules.json")
        _ = load_json(self.config.data_dir / "shorts_templates.json")

        titles = generate_titles(self.llm, topic, tone, n_titles)
        script = generate_script(self.llm, topic, tone, duration, hooks)
        script_txt = script["full_script"].strip() + "\n"
        tts_narration = to_tts(script)
        scenes = generate_scenes(self.llm, script, n_scenes, duration)
        srt = generate_srt(script["full_script"], duration)
        edit_plan = build_edit_plan(scenes, "subtitles.srt")
        thumbnail = generate_thumbnail_copy(self.llm, topic, tone)
        qa = qa_report(titles=titles, script=script, duration=duration)

        metadata: dict[str, Any] = {
            "topic": topic,
            "slug": slug,
            "tone": tone,
            "duration": duration,
            "n_titles": n_titles,
            "n_scenes": len(scenes),
            "dry_run": self.dry_run,
            "model": self.config.openai_model,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "target_audience": "US",
            "genre": ["finance", "motivation", "psychology"],
        }

        write_json(root_out / "metadata.json", metadata)
        write_json(root_out / "titles.json", {"titles": titles})
        write_json(root_out / "script.json", script)
        write_text(root_out / "script.txt", script_txt)
        write_text(root_out / "tts_narration.txt", tts_narration)
        write_json(root_out / "scenes.json", {"scenes": scenes})
        write_text(root_out / "subtitles.srt", srt)
        write_json(root_out / "edit_plan.json", edit_plan)
        write_json(root_out / "thumbnail_copy.json", thumbnail)
        write_json(root_out / "qa_report.json", qa)

        logger.info("Output package generated at %s", root_out)
        return root_out
