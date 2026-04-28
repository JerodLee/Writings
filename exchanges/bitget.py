"""Bitget public market data client.

This module only uses public endpoints and never places orders.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Any

import pandas as pd
import requests
import websocket
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


@dataclass
class BitgetClient:
    base_url: str
    symbol: str
    product_type: str = "USDT-FUTURES"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def fetch_candles(self, granularity: str = "1m", limit: int = 200) -> pd.DataFrame:
        data = self._get(
            "/api/v2/mix/market/candles",
            {
                "symbol": self.symbol,
                "productType": self.product_type,
                "granularity": granularity,
                "limit": limit,
            },
        )
        rows = data.get("data", [])
        if not rows:
            return pd.DataFrame()

        # Expected row format: [ts, open, high, low, close, baseVol, quoteVol]
        df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume", "quote_volume"])
        df["ts"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms", utc=True)
        return df.sort_values("ts").reset_index(drop=True)

    def fetch_open_interest(self) -> float | None:
        try:
            data = self._get(
                "/api/v2/mix/market/open-interest",
                {"symbol": self.symbol, "productType": self.product_type},
            )
            return float(data.get("data", {}).get("openInterest", 0))
        except Exception as exc:
            logger.warning("Bitget open interest fetch failed: %s", exc)
            return None

    def fetch_ticker(self) -> dict[str, Any]:
        return self._get(
            "/api/v2/mix/market/ticker",
            {"symbol": self.symbol, "productType": self.product_type},
        )

    def stream_trades(self, on_trade_callback):
        """Optional WebSocket trade stream for approximate CVD.

        Callback receives signed volume (+buy, -sell).
        """
        ws_url = "wss://ws.bitget.com/v2/ws/public"

        def on_open(ws):
            logger.info("Bitget websocket connected")
            sub = {
                "op": "subscribe",
                "args": [{"instType": "mc", "channel": "trade", "instId": self.symbol}],
            }
            ws.send(json.dumps(sub))

        def on_message(_ws, message: str):
            payload = json.loads(message)
            if payload.get("action") != "snapshot" and payload.get("action") != "update":
                return
            for row in payload.get("data", []):
                side = str(row.get("side", "")).lower()
                size = float(row.get("size", 0))
                signed = size if side == "buy" else -size
                on_trade_callback(signed)

        def on_error(_ws, error):
            logger.warning("Bitget websocket error: %s", error)

        def on_close(_ws, close_status_code, close_msg):
            logger.warning("Bitget websocket closed (%s): %s", close_status_code, close_msg)

        while True:
            try:
                app = websocket.WebSocketApp(
                    ws_url,
                    on_open=on_open,
                    on_message=on_message,
                    on_error=on_error,
                    on_close=on_close,
                )
                app.run_forever(ping_interval=20, ping_timeout=10)
            except Exception as exc:
                logger.exception("Bitget websocket reconnecting after error: %s", exc)
            time.sleep(5)
