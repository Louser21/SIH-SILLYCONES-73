from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ml.service import MLService

router = APIRouter(prefix="/api/v1", tags=["predict"])
service = MLService()


class SensorReading(BaseModel):
    station_id: str = Field(..., min_length=1, examples=["S01"])
    timestamp: datetime
    temperature: float
    humidity: float


class PredictionResponse(BaseModel):
    anomaly: bool
    score: float = Field(..., ge=0.0, le=1.0)
    reason: str


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: SensorReading) -> PredictionResponse:
    try:
        result = service.predict(
            {
                "station_id": payload.station_id,
                "timestamp": payload.timestamp.isoformat(),
                "temperature": payload.temperature,
                "humidity": payload.humidity,
            }
        )
        return PredictionResponse(
            anomaly=bool(result["anomaly"]),
            score=float(result["score"]),
            reason=str(result["reason"]),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc
