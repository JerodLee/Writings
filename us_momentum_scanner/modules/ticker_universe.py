from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class UniverseTicker:
    ticker: str
    name: str
    exchange: str
    security_type: str
    is_adr: bool
    price: float
    avg_dollar_volume: float
    sector: str
    theme: str


def _seed_universe() -> List[UniverseTicker]:
    return [
        UniverseTicker("AAPL", "Apple Inc.", "NASDAQ", "Common Stock", False, 190, 95000000, "Technology", "AI"),
        UniverseTicker("SOUN", "SoundHound AI", "NASDAQ", "Common Stock", False, 6.1, 15000000, "Technology", "AI"),
        UniverseTicker("BBAI", "BigBear.ai", "NYSE", "Common Stock", False, 2.6, 4500000, "Technology", "AI"),
        UniverseTicker("ABCDW", "Example Warrant", "NASDAQ", "Warrant", False, 1.2, 5000000, "Other", "Other"),
        UniverseTicker("SPY", "SPDR S&P 500 ETF", "NYSE", "ETF", False, 520, 500000000, "ETF", "Index"),
        UniverseTicker("XYZ", "Small Illiquid", "NASDAQ", "Common Stock", False, 0.4, 200000, "Healthcare", "Bio"),
    ]


def build_universe() -> List[UniverseTicker]:
    allowed_exchanges = {"NASDAQ", "NYSE"}
    blocked_types = {"ETF", "Warrant", "Preferred", "SPAC"}
    universe = []
    for item in _seed_universe():
        if item.exchange not in allowed_exchanges:
            continue
        if item.security_type in blocked_types:
            continue
        if item.price < 0.5 or item.avg_dollar_volume < 1_000_000:
            continue
        universe.append(item)
    return universe
