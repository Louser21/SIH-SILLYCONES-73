from __future__ import annotations

from typing import Any

from app.ml.inference.predictor import PredictorFactory


class MLService:
    def __init__(self) -> None:
        self.predictor = PredictorFactory.get_predictor()

    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = self.predictor.predict(payload)
        return {
            "anomaly": result.anomaly,
            "score": result.score,
            "reason": result.reason,
        }
