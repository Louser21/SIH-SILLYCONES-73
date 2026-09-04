from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PredictionResult:
    anomaly: bool
    score: float
    reason: str


class BaselinePredictor:
    """Temporary baseline model used before real ML model is ready."""

    def predict(self, payload: dict[str, Any]) -> PredictionResult:
        temperature = float(payload.get("temperature", 0.0))
        humidity = float(payload.get("humidity", 0.0))

        # Simple rule-based baseline for demo and contract validation.
        score = 0.87 if temperature > 34 and humidity > 70 else 0.15
        anomaly = score > 0.8
        reason = (
            "Temperature-humidity inconsistency"
            if anomaly
            else "Within expected operating range"
        )

        return PredictionResult(anomaly=anomaly, score=score, reason=reason)


class PredictorFactory:
    _instance: BaselinePredictor | None = None

    @classmethod
    def get_predictor(cls) -> BaselinePredictor:
        if cls._instance is None:
            cls._instance = BaselinePredictor()
        return cls._instance
