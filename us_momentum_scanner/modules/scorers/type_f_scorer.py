from .base_scorer import BaseScorer


class TypeFScorer(BaseScorer):
    type_name = "TYPE F"

    def score(self, row):
        score = 15
        score += 40 if row.get("float_shares", 1e9) < 20_000_000 else 0
        score += 25 if row.get("premarket_gap", 0) > 0.2 else 0
        score += min(20, row.get("float_rotation", 0) * 2)
        return self.clamp(score)
