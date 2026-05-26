from __future__ import annotations

from typing import Dict


def get_market_regime() -> Dict[str, float | str]:
    vix = 17.0
    qqq_5d = 0.02
    spy_5d = 0.015
    iwm_5d = 0.012
    btc_1d = 0.01

    score = 0
    score += 1 if vix < 20 else -1
    score += 1 if qqq_5d > 0 else -1
    score += 1 if spy_5d > 0 else -1
    score += 1 if iwm_5d > 0 else -1
    score += 1 if btc_1d > 0 else -1

    regime = "RISK_ON" if score >= 3 else "RISK_OFF" if score <= -2 else "NEUTRAL"
    return {"regime": regime, "vix": vix, "qqq_5d": qqq_5d, "spy_5d": spy_5d, "iwm_5d": iwm_5d, "btc_1d": btc_1d}


def type_multiplier(regime: str, t: str) -> float:
    table = {
        "RISK_ON": {"TYPE A": 1.05, "TYPE D": 1.2, "TYPE F": 1.05},
        "NEUTRAL": {"TYPE A": 1.0, "TYPE D": 1.0, "TYPE F": 1.0},
        "RISK_OFF": {"TYPE A": 0.95, "TYPE D": 0.75, "TYPE F": 0.95},
    }
    return table.get(regime, {}).get(t, 1.0)
