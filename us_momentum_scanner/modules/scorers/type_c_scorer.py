from .base_scorer import BaseScorer


class TypeCScorer(BaseScorer):
    type_name = "TYPE C"

    def score(self, row):
        score = 5
        news = row.get("news_summary", "").lower()
        score += 55 if any(k in news for k in ["fda", "phase", "trial", "clinical"]) else 0
        score += 20 if row.get("premarket_gap", 0) > 0.1 else 0
        score += min(20, row.get("volume_velocity", 0) * 3)
        return self.clamp(score)
