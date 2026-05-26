from .base_scorer import BaseScorer


class TypeBScorer(BaseScorer):
    type_name = "TYPE B"

    def score(self, row):
        score = 10
        score += 45 if "earnings" in row.get("news_summary", "").lower() else 0
        score += 20 if row.get("premarket_gap", 0) > 0.08 else 0
        score += min(25, row.get("dollar_volume_m", 0) / 2)
        return self.clamp(score)
