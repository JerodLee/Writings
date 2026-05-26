from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytz

from .market_regime import get_market_regime, type_multiplier
from .news_collector import collect_news_for_ticker
from .premarket_scanner import enrich_premarket
from .price_collector import collect_prices
from .report_generator import build_report
from .risk_filter import apply_risk_filters
from .ticker_universe import build_universe
from .type_classifier import classify_and_score


def run_screener(base_dir: Path):
    eastern = pytz.timezone("US/Eastern")
    asof_date = datetime.now(eastern).date()
    universe = build_universe()  # Gate 0 first
    rows = collect_prices(universe)
    regime_info = get_market_regime()

    out = []
    for row in rows:
        row = enrich_premarket(row)
        news = collect_news_for_ticker(row["ticker"])
        row["news_count"] = len(news)
        row["news_summary"] = "; ".join([n["title"] for n in news][:2])
        row["regime"] = regime_info["regime"]
        row = apply_risk_filters(row)
        row = classify_and_score(row)
        mult = type_multiplier(row["regime"], row["type"])
        row["regime_multiplier"] = mult
        row["score"] = round(row["type_score"] * mult, 2)
        row["entry_ban_reason"] = row.get("avoid_reason", "")
        if row["kill_switch"] == "BLOCK":
            continue
        out.append(row)

    return build_report(out, base_dir / "data" / "candidates.csv", base_dir / "data" / "daily_reports"), asof_date
