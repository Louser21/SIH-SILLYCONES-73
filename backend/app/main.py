from fastapi import FastAPI

from app.routes.anomaly import router as anomaly_router
from app.routes.health import router as health_router

app = FastAPI(title="SIH SILLYCONES API", version="0.1.0")

app.include_router(health_router)
app.include_router(anomaly_router)
