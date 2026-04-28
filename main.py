"""dual_edge_signal_bot entrypoint.

Real-time crypto signal bot for Bitget futures + Bithumb spot.
No order execution. Alerts only.
"""

from __future__ import annotations

import csv
import logging
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from config import settings
from exchanges.bitget import BitgetClient
from exchanges.bithumb import BithumbClient
from notifier.telegram import TelegramNotifier
from strategy.indicators import add_indicators
from strategy.m1 import evaluate_m1_break_retest
from strategy.spring import evaluate_spring_reversal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("dual_edge_signal_bot")

SIGNAL_LOG_PATH = Path("storage/signal_log.csv")


class CVDState:
    """In-memory CVD accumulator."""

    def __init__(self):
        self.value = 0.0
        self.lock = threading.Lock()

    def update(self, signed_volume: float):
        with self.lock:
            self.value += signed_volume

    def get(self) -> float:
        with self.lock:
            return self.value


def ensure_signal_log() -> None:
    SIGNAL_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SIGNAL_LOG_PATH.exists():
        with SIGNAL_LOG_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "timestamp_utc",
                    "exchange",
                    "symbol",
                    "strategy",
                    "grade",
                    "entry",
                    "stop",
                    "target1",
                    "target2",
                    "meta",
                ]
            )


def append_signal_log(exchange: str, symbol: str, signal: dict) -> None:
    with SIGNAL_LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                datetime.now(timezone.utc).isoformat(),
                exchange,
                symbol,
                signal["strategy"],
                signal["grade"],
                signal["entry"],
                signal["stop"],
                signal["target1"],
                signal["target2"],
                str(signal.get("meta", {})),
            ]
        )


def format_signal_message(exchange: str, symbol: str, signal: dict) -> str:
    return (
        f"*{signal['strategy']}* ({exchange} {symbol})\n"
        f"Grade: *{signal['grade']}*\n"
        f"Entry: `{signal['entry']:.4f}`\n"
        f"Invalidation Stop: `{signal['stop']:.4f}`\n"
        f"Target1 (2R): `{signal['target1']:.4f}`\n"
        f"Target2 (3R): `{signal['target2']:.4f}`\n"
        f"Meta: `{signal.get('meta', {})}`\n"
        "_Alert only. No auto-trading._"
    )


def run_bot() -> None:
    ensure_signal_log()

    notifier = TelegramNotifier(settings.telegram_bot_token, settings.telegram_chat_id)
    cvd_state = CVDState()

    bitget = BitgetClient(settings.bitget_base_url, settings.default_symbol_bitget)
    bithumb = BithumbClient(settings.bithumb_base_url, settings.default_symbol_bithumb)

    # Optional Bitget websocket for CVD approximation (non-blocking thread).
    ws_thread = threading.Thread(target=bitget.stream_trades, args=(cvd_state.update,), daemon=True)
    ws_thread.start()

    last_sent_key: set[str] = set()

    while True:
        try:
            for name, client, symbol in [
                ("BITGET", bitget, settings.default_symbol_bitget),
                ("BITHUMB", bithumb, settings.default_symbol_bithumb),
            ]:
                candles = client.fetch_candles(settings.timeframe, settings.max_candles)
                if candles.empty:
                    logger.warning("No candles from %s", name)
                    continue

                # Inject OI and CVD for strategy use.
                oi_value = client.fetch_open_interest()
                candles["oi"] = oi_value if oi_value is not None else 0.0
                candles["cvd"] = cvd_state.get()

                df = add_indicators(
                    candles,
                    rsi_period=settings.rsi_period,
                    cci_period=settings.cci_period,
                    atr_period=settings.atr_period,
                    vol_ma_period=settings.vol_ma_period,
                    box_lookback=settings.box_lookback,
                )

                signals = [
                    evaluate_m1_break_retest(df),
                    evaluate_spring_reversal(df),
                ]

                for signal in [s for s in signals if s is not None]:
                    signal_key = f"{name}:{symbol}:{signal['strategy']}:{df.iloc[-1]['ts']}"
                    if signal_key in last_sent_key:
                        continue
                    last_sent_key.add(signal_key)

                    msg = format_signal_message(name, symbol, signal)
                    notifier.send_message(msg)
                    append_signal_log(name, symbol, signal)
                    logger.info("Signal sent: %s", signal_key)

            time.sleep(settings.poll_interval_seconds)

        except Exception as exc:
            logger.exception("Main loop error (recovering): %s", exc)
            time.sleep(5)


if __name__ == "__main__":
    run_bot()
