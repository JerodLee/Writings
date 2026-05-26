from .base_scorer import BaseScorer


class TypeEScorer(BaseScorer):
    type_name = "TYPE E"

    def score(self, row):
        score = 20
        score += min(40, row.get("news_count", 0) * 10)
        score += 20 if row.get("premarket_gap", 0) > 0.07 else 0
        score += min(20, row.get("volume_velocity", 0) * 3)
        return self.clamp(score)
