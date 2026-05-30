from __future__ import annotations

from datetime import datetime
from difflib import SequenceMatcher
from typing import Dict, Any, List


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def dedupe_news(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for item in sorted(items, key=lambda x: x.get("published_at", ""), reverse=True):
        duplicate = False
        for kept in out:
            same_url = item.get("url") and item.get("url") == kept.get("url")
            near_title = _similar(item.get("title", ""), kept.get("title", "")) > 0.88
            t1 = datetime.fromisoformat(item.get("published_at")) if item.get("published_at") else None
            t2 = datetime.fromisoformat(kept.get("published_at")) if kept.get("published_at") else None
            close_time = t1 and t2 and abs((t1 - t2).total_seconds()) < 3600
            if same_url or (near_title and close_time):
                duplicate = True
                break
        if not duplicate:
            out.append(item)
    return out


def collect_news_for_ticker(ticker: str) -> List[Dict[str, Any]]:
    now = datetime.utcnow().replace(microsecond=0).isoformat()
    raw = [
        {"title": f"{ticker} gains on AI partnership", "url": f"https://example.com/{ticker}/1", "published_at": now},
        {"title": f"{ticker} gains on AI partnership update", "url": f"https://example.com/{ticker}/1", "published_at": now},
    ]
    return dedupe_news(raw)
