from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseScorer(ABC):
    type_name: str

    @abstractmethod
    def score(self, row: Dict[str, Any]) -> float:
        """Return score in range 0~100."""

    def clamp(self, value: float) -> float:
        return max(0.0, min(100.0, float(value)))
