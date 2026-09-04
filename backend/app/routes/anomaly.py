from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["deprecated"])


@router.get("/anomaly")
def deprecated_anomaly_route() -> dict[str, str]:
    return {"message": "This route is deprecated. Use /api/v1/predict instead."}
