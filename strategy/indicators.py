"""Indicator helpers for strategy modules.

All methods return pandas Series to keep things simple for beginners.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def ensure_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Convert OHLCV columns to numeric if needed."""
    out = df.copy()
    for col in ["open", "high", "low", "close", "volume", "oi", "cvd"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def vwap(df: pd.DataFrame) -> pd.Series:
    typical_price = (df["high"] + df["low"] + df["close"]) / 3.0
    cumulative_tpv = (typical_price * df["volume"]).cumsum()
    cumulative_vol = df["volume"].replace(0, np.nan).cumsum()
    return cumulative_tpv / cumulative_vol


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def cci(df: pd.DataFrame, period: int = 14) -> pd.Series:
    typical = (df["high"] + df["low"] + df["close"]) / 3.0
    sma = typical.rolling(period).mean()
    mad = typical.rolling(period).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    return (typical - sma) / (0.015 * mad.replace(0, np.nan))


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            (df["high"] - df["low"]).abs(),
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def volume_ma(df: pd.DataFrame, period: int = 20) -> pd.Series:
    return df["volume"].rolling(period).mean()


def box_levels(df: pd.DataFrame, lookback: int = 30) -> tuple[pd.Series, pd.Series]:
    return df["high"].rolling(lookback).max(), df["low"].rolling(lookback).min()


def oi_delta(df: pd.DataFrame) -> pd.Series:
    if "oi" not in df.columns:
        return pd.Series(index=df.index, dtype=float)
    return df["oi"].diff()


def add_indicators(df: pd.DataFrame, *, rsi_period: int, cci_period: int, atr_period: int, vol_ma_period: int, box_lookback: int) -> pd.DataFrame:
    out = ensure_numeric(df)
    out["vwap"] = vwap(out)
    out["rsi"] = rsi(out["close"], rsi_period)
    out["cci"] = cci(out, cci_period)
    out["atr"] = atr(out, atr_period)
    out["volume_ma20"] = volume_ma(out, vol_ma_period)
    out["box_high"], out["box_low"] = box_levels(out, box_lookback)
    out["oi_delta"] = oi_delta(out)
    out["cvd_delta"] = out["cvd"].diff() if "cvd" in out.columns else np.nan
    return out
