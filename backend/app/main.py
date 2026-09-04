from __future__ import annotations

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.predict import router as predict_router
from app.ml.service import MLService

app = FastAPI(
    title="SIH SILLYCONES Backend",
    version="0.1.0",
    description="Minimal backend for anomaly prediction during a 48-hour hackathon.",
)

app.state.ml_service = MLService()

app.include_router(health_router)
app.include_router(predict_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "SIH SILLYCONES backend is running"}
