"""Spring Reversal strategy logic."""

from __future__ import annotations

from typing import Any

import pandas as pd


def _grade_signal(score: int) -> str:
    if score >= 6:
        return "A+"
    if score == 5:
        return "A"
    if score >= 3:
        return "B"
    return "reject"


def evaluate_spring_reversal(df: pd.DataFrame) -> dict[str, Any] | None:
    """Evaluate latest candles for spring reversal setup."""
    if len(df) < 40:
        return None

    last = df.iloc[-1]
    c1 = df.iloc[-2]
    c2 = df.iloc[-3]
    c3 = df.iloc[-4]

    box_low = c1["box_low"]
    if pd.isna(box_low):
        return None

    swept_low = min(c3["low"], c2["low"], c1["low"]) < box_low
    reclaimed = last["close"] >= box_low and (c1["close"] >= box_low or c2["close"] >= box_low)

    body = abs(last["close"] - last["open"])
    lower_wick = min(last["open"], last["close"]) - last["low"]
    long_wick = lower_wick > body * 1.5

    vol_spike = last["volume"] > 1.8 * last["volume_ma20"] if pd.notna(last["volume_ma20"]) else False
    oi_down = last.get("oi_delta", 0) < 0

    price_not_lower_low = last["low"] >= c1["low"]
    cvd_negative = last.get("cvd", 0) <= c1.get("cvd", 0)
    cvd_improving = last.get("cvd_delta", 0) > 0
    cvd_condition = cvd_negative and price_not_lower_low and cvd_improving

    checks = [swept_low, reclaimed, long_wick, vol_spike, oi_down, cvd_condition]
    score = sum(bool(x) for x in checks)
    grade = _grade_signal(score)

    if grade == "reject":
        return None

    entry = last["close"]
    stop = min(last["low"], box_low - 0.5 * last["atr"])
    risk = max(entry - stop, 1e-9)

    return {
        "strategy": "Spring Reversal",
        "grade": grade,
        "entry": float(entry),
        "stop": float(stop),
        "target1": float(entry + 2 * risk),
        "target2": float(entry + 3 * risk),
        "meta": {
            "swept_low": bool(swept_low),
            "reclaimed": bool(reclaimed),
            "long_wick": bool(long_wick),
            "vol_spike": bool(vol_spike),
            "oi_down": bool(oi_down),
            "cvd_condition": bool(cvd_condition),
        },
    }
