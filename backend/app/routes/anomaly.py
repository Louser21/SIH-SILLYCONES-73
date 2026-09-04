from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1", tags=["anomaly"])


class SensorReading(BaseModel):
    station_id: str = Field(..., examples=["S01"])
    timestamp: datetime
    temperature: float
    humidity: float


class AnomalyResponse(BaseModel):
    anomaly: bool
    score: float = Field(..., ge=0.0, le=1.0)
    reason: str


@router.post("/anomaly", response_model=AnomalyResponse)
def detect_anomaly(payload: SensorReading) -> AnomalyResponse:
    # Baseline placeholder so frontend/ingestion can integrate immediately.
    score = 0.87 if payload.temperature > 34 and payload.humidity > 70 else 0.15
    is_anomaly = score > 0.8
    reason = (
        "Temperature-humidity inconsistency"
        if is_anomaly
        else "Within expected operating range"
    )
    return AnomalyResponse(anomaly=is_anomaly, score=score, reason=reason)
