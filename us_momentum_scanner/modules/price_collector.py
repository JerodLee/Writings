from __future__ import annotations

import math
import time
from typing import Dict, Any, List

from .ticker_universe import UniverseTicker


def _safe_num(value, default=0.0):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return default
    return value


def _fetch_primary(ticker: UniverseTicker) -> Dict[str, Any]:
    return {
        "prev_close": ticker.price * 0.97,
        "premarket_price": ticker.price,
        "premarket_volume": 120_000,
        "today_volume": 2_000_000,
        "avg_volume": 800_000,
        "float_shares": 40_000_000,
        "dollar_volume_m": ticker.avg_dollar_volume / 1_000_000,
        "data_quality": "DATA_QUALITY_DELAYED_15MIN",
    }


def _fetch_fallback(ticker: UniverseTicker) -> Dict[str, Any]:
    return {
        "prev_close": ticker.price,
        "premarket_price": ticker.price,
        "premarket_volume": 0,
        "today_volume": ticker.avg_dollar_volume / max(ticker.price, 1),
        "avg_volume": ticker.avg_dollar_volume / max(ticker.price, 1),
        "float_shares": 80_000_000,
        "dollar_volume_m": ticker.avg_dollar_volume / 1_000_000,
        "data_quality": "DATA_QUALITY_FALLBACK_USED",
    }


def collect_prices(universe: List[UniverseTicker], retries: int = 2, timeout_sec: float = 0.2) -> List[Dict[str, Any]]:
    rows = []
    for ticker in universe:
        payload = None
        quality_flags = []
        for _ in range(retries + 1):
            try:
                payload = _fetch_primary(ticker)
                break
            except Exception:
                time.sleep(timeout_sec)
        if payload is None:
            payload = _fetch_fallback(ticker)
            quality_flags.append("DATA_QUALITY_UNAVAILABLE")

        for k in ["prev_close", "premarket_price", "premarket_volume", "today_volume", "avg_volume", "float_shares", "dollar_volume_m"]:
            payload[k] = _safe_num(payload.get(k), 0.0)

        if payload["premarket_price"] == 0:
            payload["premarket_price"] = payload["prev_close"]
            quality_flags.append("DATA_QUALITY_APPROXIMATE")

        payload["data_quality_flags"] = ",".join([payload.get("data_quality", ""), *quality_flags]).strip(",")
        payload["ticker"] = ticker.ticker
        payload["name"] = ticker.name
        payload["sector"] = ticker.sector
        payload["theme"] = ticker.theme
        payload["is_adr"] = ticker.is_adr
        rows.append(payload)
    return rows
