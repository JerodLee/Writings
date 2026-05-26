from __future__ import annotations

from typing import Dict, Any

from .scorers.type_a_scorer import TypeAScorer
from .scorers.type_b_scorer import TypeBScorer
from .scorers.type_c_scorer import TypeCScorer
from .scorers.type_d_scorer import TypeDScorer
from .scorers.type_e_scorer import TypeEScorer
from .scorers.type_f_scorer import TypeFScorer


SCORERS = [TypeAScorer(), TypeBScorer(), TypeCScorer(), TypeDScorer(), TypeEScorer(), TypeFScorer()]


def classify_and_score(row: Dict[str, Any]) -> Dict[str, Any]:
    scores = {s.type_name: s.score(row) for s in SCORERS}
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary_type, primary_score = ranked[0]
    secondary_type, secondary_score = ranked[1]
    final_score = primary_score * 0.7 + secondary_score * 0.3 if secondary_score > 0 else primary_score
    row.update(
        {
            "type": primary_type,
            "secondary_type": secondary_type,
            "type_score": round(final_score, 2),
            "component_scores": scores,
        }
    )
    return row
