from __future__ import annotations

import json
import logging
from typing import Any

try:
    from openai import OpenAI
except Exception:  # noqa: BLE001
    OpenAI = None


logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, api_key: str | None, model: str, dry_run: bool = False):
        self.dry_run = dry_run
        self.model = model
        self.client = OpenAI(api_key=api_key) if (OpenAI and api_key and not dry_run) else None

    def ask_json(self, prompt: str) -> dict[str, Any] | None:
        if self.client is None:
            return None
        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": "Return valid JSON only."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            return json.loads(response.output_text.strip())
        except Exception as exc:  # noqa: BLE001
            logger.warning("LLM call failed, using fallback: %s", exc)
            return None
