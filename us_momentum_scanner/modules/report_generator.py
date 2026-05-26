from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import pytz

DIVERSITY_LIMIT = {"same_theme": 3, "same_sector": 4}


def _grade(score: float) -> str:
    if score >= 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    return "C"


def _confidence(row: Dict[str, Any]) -> str:
    flags = row.get("data_quality_flags", "")
    if "UNAVAILABLE" in flags:
        return "LOW"
    if row.get("is_adr"):
        return "MEDIUM"
    if "FALLBACK" in flags or "APPROXIMATE" in flags:
        return "MEDIUM"
    return "HIGH"


def build_report(rows: List[Dict[str, Any]], output_csv: Path, daily_dir: Path) -> pd.DataFrame:
    kept = []
    theme_count = {}
    sector_count = {}
    for row in sorted(rows, key=lambda x: x.get("score", 0), reverse=True):
        theme = row.get("theme", "UNKNOWN")
        sector = row.get("sector", "UNKNOWN")
        if theme_count.get(theme, 0) >= DIVERSITY_LIMIT["same_theme"]:
            continue
        if sector_count.get(sector, 0) >= DIVERSITY_LIMIT["same_sector"]:
            continue
        theme_count[theme] = theme_count.get(theme, 0) + 1
        sector_count[sector] = sector_count.get(sector, 0) + 1
        row["grade"] = _grade(row["score"])
        row["confidence"] = _confidence(row)
        kept.append(row)

    df = pd.DataFrame(kept)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    daily_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    eastern = pytz.timezone("US/Eastern")
    ts = datetime.now(eastern).strftime("%Y%m%d")
    df.to_csv(daily_dir / f"candidates_{ts}.csv", index=False)
    return df
