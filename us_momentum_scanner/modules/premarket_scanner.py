from __future__ import annotations

from typing import Dict, Any


def enrich_premarket(row: Dict[str, Any]) -> Dict[str, Any]:
    prev_close = max(0.01, row.get("prev_close", 1.0))
    pm_price = row.get("premarket_price", prev_close)
    pm_vol = row.get("premarket_volume", 0)
    gap = (pm_price - prev_close) / prev_close
    velocity = row.get("today_volume", 0) / max(1, row.get("avg_volume", 1))
    float_rotation = row.get("today_volume", 0) / max(1, row.get("float_shares", 1)) * 100
    row.update(
        {
            "premarket_gap": gap,
            "volume_velocity": velocity,
            "float_rotation": float_rotation,
            "premarket_volume": pm_vol,
        }
    )
    return row
