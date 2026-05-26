from .base_scorer import BaseScorer


class TypeAScorer(BaseScorer):
    type_name = "TYPE A"

    def score(self, row):
        score = 25
        score += 35 if row.get("float_shares", 1e9) < 50_000_000 else 0
        score += min(25, row.get("volume_velocity", 0) * 5)
        score += 15 if row.get("premarket_gap", 0) > 0.15 else 0
        return self.clamp(score)
