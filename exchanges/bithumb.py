"""Bithumb public market data client.

This module only uses public endpoints and never places orders.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


@dataclass
class BithumbClient:
    base_url: str
    symbol: str  # Example: BTC_KRW

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def fetch_candles(self, interval: str = "1m", limit: int = 200) -> pd.DataFrame:
        # Public candle endpoint naming can differ by market; keep this configurable/easy to adjust.
        data = self._get("/public/candlestick/{}/{}".format(self.symbol, interval), {})
        rows = data.get("data", [])
        if not rows:
            return pd.DataFrame()

        # Common format: [ts, open, close, high, low, volume]
        df = pd.DataFrame(rows, columns=["ts", "open", "close", "high", "low", "volume"])
        df["ts"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms", utc=True)
        return df.sort_values("ts").tail(limit).reset_index(drop=True)

    def fetch_ticker(self) -> dict[str, Any]:
        # Ticker all endpoint with KRW market compatibility.
        return self._get("/public/ticker/{}".format(self.symbol), {})

    def fetch_open_interest(self) -> float | None:
        # Spot exchanges usually do not provide OI. We keep None for shared strategy pipeline.
        logger.info("Bithumb spot does not provide open interest; using None.")
        return None
