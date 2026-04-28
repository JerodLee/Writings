"""M1 Break-Retest strategy logic."""

from __future__ import annotations

from typing import Any

import pandas as pd


def _grade_signal(score: int) -> str:
    if score >= 5:
        return "A+"
    if score == 4:
        return "A"
    if score == 3:
        return "B"
    return "reject"


def evaluate_m1_break_retest(df: pd.DataFrame) -> dict[str, Any] | None:
    """Evaluate latest candles for M1 break-retest long setup.

    Rules:
    - break above box high
    - volume spike > 1.8 * MA20
    - retest holds
    - OI increasing
    - CVD positive/improving
    """
    if len(df) < 40:
        return None

    last = df.iloc[-1]
    prev = df.iloc[-2]
    prev2 = df.iloc[-3]

    box_high = prev["box_high"]
    if pd.isna(box_high):
        return None

    broke_above = prev2["close"] <= box_high and prev["close"] > box_high
    vol_spike = last["volume"] > 1.8 * last["volume_ma20"] if pd.notna(last["volume_ma20"]) else False
    retest_hold = last["low"] <= box_high and last["close"] >= box_high
    oi_up = last.get("oi_delta", 0) > 0
    cvd_ok = (last.get("cvd_delta", 0) > 0) or (last.get("cvd", 0) >= prev.get("cvd", 0))

    checks = [broke_above, vol_spike, retest_hold, oi_up, cvd_ok]
    score = sum(bool(x) for x in checks)
    grade = _grade_signal(score)

    if grade == "reject":
        return None

    entry = max(last["close"], box_high)
    stop = min(last["low"], box_high - (0.5 * last["atr"]))
    risk = max(entry - stop, 1e-9)
    target1 = entry + 2 * risk
    target2 = entry + 3 * risk

    return {
        "strategy": "M1 Break-Retest",
        "grade": grade,
        "entry": float(entry),
        "stop": float(stop),
        "target1": float(target1),
        "target2": float(target2),
        "meta": {
            "broke_above": bool(broke_above),
            "vol_spike": bool(vol_spike),
            "retest_hold": bool(retest_hold),
            "oi_up": bool(oi_up),
            "cvd_ok": bool(cvd_ok),
        },
    }
