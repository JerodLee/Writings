from .base_scorer import BaseScorer


class TypeDScorer(BaseScorer):
    type_name = "TYPE D"

    def score(self, row):
        score = 10
        news = row.get("news_summary", "").lower()
        score += 50 if any(k in news for k in ["ai", "nvidia", "datacenter", "theme"]) else 0
        score += min(20, row.get("volume_velocity", 0) * 2)
        score += 20 if row.get("regime", "NEUTRAL") == "RISK_ON" else 0
        return self.clamp(score)
