from __future__ import annotations

import re
from typing import Iterable



def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]



def chunk_words(words: Iterable[str], n: int) -> list[list[str]]:
    bucket: list[list[str]] = []
    cur: list[str] = []
    for w in words:
        cur.append(w)
        if len(cur) >= n:
            bucket.append(cur)
            cur = []
    if cur:
        bucket.append(cur)
    return bucket
