"""Configuration module for dual_edge_signal_bot.

Loads environment variables and central runtime settings.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")

    bitget_base_url: str = os.getenv("BITGET_BASE_URL", "https://api.bitget.com")
    bithumb_base_url: str = os.getenv("BITHUMB_BASE_URL", "https://api.bithumb.com")

    # Runtime controls
    default_symbol_bitget: str = "BTCUSDT"
    default_symbol_bithumb: str = "BTC_KRW"
    timeframe: str = "1m"
    poll_interval_seconds: int = 15
    max_candles: int = 300

    # Strategy tuning
    box_lookback: int = 30
    vol_ma_period: int = 20
    rsi_period: int = 14
    cci_period: int = 14
    atr_period: int = 14


settings = Settings()
