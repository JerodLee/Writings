from __future__ import annotations

import os
from typing import Dict, Any, List

import feedparser
import requests

KEYWORDS_HARD = ["reverse split", "direct offering", "delisting", "going concern", "nasdaq deficiency"]
KEYWORDS_SOFT = ["atm offering", "shelf registration", "s-3", "424b5", "convertible note"]


def fetch_sec_feed(ticker: str) -> List[str]:
    ua = os.getenv("SEC_USER_AGENT", "YourName your_email@example.com")
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=8-K&owner=exclude&count=20&output=atom"
    resp = requests.get(url, timeout=8, headers={"User-Agent": ua})
    resp.raise_for_status()
    feed = feedparser.parse(resp.text)
    return [f"{e.get('title', '')} {e.get('summary', '')}".lower() for e in feed.entries]


def apply_risk_filters(row: Dict[str, Any]) -> Dict[str, Any]:
    avoid_reasons = []
    kill_switch = "PASS"

    if row.get("premarket_gap", 0) > 0.30 and row.get("premarket_volume", 0) < 50_000:
        avoid_reasons.append("최소 프리마켓 거래량 미달")

    try:
        filings = fetch_sec_feed(row["ticker"])
    except Exception:
        filings = []
        row["data_quality_flags"] = f"{row.get('data_quality_flags','')},DATA_QUALITY_FALLBACK_USED".strip(",")

    joined = " ".join(filings)
    if any(k in joined for k in KEYWORDS_HARD):
        kill_switch = "BLOCK"
        avoid_reasons.append("SEC 고위험 공시 감지")
    elif any(k in joined for k in KEYWORDS_SOFT):
        kill_switch = "AVOID"
        avoid_reasons.append("SEC 희석성/리스크 공시 감지")

    row["kill_switch"] = kill_switch
    row["avoid_reason"] = "; ".join(avoid_reasons)
    return row
