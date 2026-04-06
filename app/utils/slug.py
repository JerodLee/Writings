from __future__ import annotations

import re


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", text.strip().lower())
    slug = re.sub(r"[\s_-]+", "-", cleaned).strip("-")
    return slug or "short-topic"
