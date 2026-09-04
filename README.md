# SIH-SILLYCONES-73

This repository is the foundation for the 48-hour SIH 2026 hackathon project.

The architecture is intentionally simple: the backend owns the API and the production ML inference path, and the ML logic lives inside the backend instead of as a separate service.

The goal is to keep the system easy to extend by 6 developers without adding unnecessary infrastructure.

For the full architecture and execution flow, read [REPO_FLOW.md](REPO_FLOW.md).

## 1) Repo Philosophy

- One monorepo, clear contracts, independent workstreams.
- Contract-first development: define the interface before implementation.
- Small PRs and frequent reviews.
- Every branch should stay runnable even while a feature is incomplete.
- No separate ML server for the initial phase.

## 2) Current Monorepo Layout

```text
SIH-SILLYCONES-73/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── ml/
│   │   │   ├── inference/
│   │   │   │   └── predictor.py
│   │   │   ├── model/
│   │   │   └── service.py
│   │   ├── main.py
│   │   └── __init__.py
│   ├── .env.example
│   ├── requirements.txt
│   └── .venv/    # local environment, not committed
├── frontend/
├── ingestion/
│   ├── mqtt/
│   └── simulator/
├── contracts/
│   ├── sensor-reading.schema.json
│   ├── anomaly-prediction.schema.json
│   ├── anomaly.schema.json
│   └── openapi.yaml
├── README.md
├── REPO_FLOW.md
├── CONTRIBUTING.md
├── docker-compose.yml
├── .gitignore
├── .github/
└── edge/
```

## 3) Architecture Summary

The system is designed as:

```text
Frontend
   ↓
Backend API
   ├── /health
   └── /api/v1/predict
       ↓
   Backend ML inference layer
       ↓
   Baseline predictor / future real model
```

This is intentional: the backend owns the inference path and exposes a stable API contract. Later, the baseline predictor can be replaced with a trained ML model without changing the API contract.

## 4) Backend + ML Design

The production ML path is embedded under the backend, not as a separate service.

Relevant files:

- backend/app/main.py
- backend/app/api/routes/health.py
- backend/app/api/routes/predict.py
- backend/app/ml/inference/predictor.py
- backend/app/ml/service.py

### Responsibilities

- backend/app/api/routes/: request handling and HTTP endpoints
- backend/app/ml/inference/: detector logic and predictor implementations
- backend/app/ml/model/: future trained model artifacts or model wrappers
- backend/app/ml/service.py: interface used by the API layer

The model is loaded once at startup and reused for requests instead of reinitializing it per request.

## 5) Current API Contract

### Input payload

```json
{
  "station_id": "S01",
  "timestamp": "2026-09-05T12:30:00Z",
  "temperature": 35.0,
  "humidity": 75.0
}
```

### Output payload

```json
{
  "anomaly": true,
  "score": 0.87,
  "reason": "Temperature-humidity inconsistency"
}
```

Contract files:

- contracts/sensor-reading.schema.json
- contracts/anomaly-prediction.schema.json
- contracts/openapi.yaml

The legacy file contracts/anomaly.schema.json remains as a compatibility placeholder and should be treated as a legacy contract until the team decides whether to rename or replace it.

## 6) Health and Prediction Endpoints

### Health

```bash
GET /health
```

Response:

```json
{"status": "ok"}
```

### Prediction

```bash
POST /api/v1/predict
```

Example body:

```json
{
  "station_id": "S01",
  "timestamp": "2026-09-05T12:30:00Z",
  "temperature": 35.0,
  "humidity": 75.0
}
```

Example response:

```json
{
  "anomaly": true,
  "score": 0.87,
  "reason": "Temperature-humidity inconsistency"
}
```

## 7) Baseline Predictor

The initial implementation uses a simple rule-based baseline predictor in [backend/app/ml/inference/predictor.py](backend/app/ml/inference/predictor.py).

This is intentionally temporary and meant to satisfy the following conditions:

- the API works immediately
- frontend and ingestion can integrate early
- the real ML team can replace the logic later
- the contract remains stable

The real model should later replace the baseline logic without changing the backend route shape.

## 8) Local Run Guide

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker (optional for quick demo startup)

```bash
docker compose up --build
```

Stop it using:

```bash
docker compose down
```

## 9) Git Workflow

Never push directly to main.

Recommended flow:

```bash
git checkout main
git pull origin main
git checkout -b feature/backend
git add .
git commit -m "Add backend anomaly API"
git push -u origin feature/backend
```

Then create a PR, get review, and merge into main.

## 10) Team Ownership

- Backend / API: FastAPI and route logic
- ML: model logic and predictor replacement inside backend/ml/
- Frontend: dashboard UI and API consumption
- Ingestion: sensor simulation and MQTT payload generation
- Edge: ESP32 or hardware integration later

## 11) Definition of Done

A task is only done when:

1. It works locally.
2. It follows the data contract.
3. The change stays in a feature branch.
4. The PR has a reviewer and a brief summary.
5. Another teammate can run it with a fresh clone.

## 12) 48-Hour Hackathon Mode

Use this mode to stay focused:

1. Freeze the contract.
2. Get a working backend endpoint.
3. Integrate minimal ingestion.
4. Connect frontend to the backend response.
5. Replace the baseline predictor with real ML later.

This keeps the project demo-ready without overengineering.

npm install
npm run dev
```

ML:

```bash
cd ml
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 11) Definition of Done (Per Feature)

A task is done only if:

1. Contract compatibility is preserved.
2. Code is in feature branch with clear commits.
3. PR has reviewer and summary of changes.
4. Another teammate can run it from fresh pull.

If these are not true, the task is not done.

## 12) 48-Hour Hackathon Mode (Time-Boxed)

Use this mode to avoid overengineering and guarantee a demo in 48 hours.

### Must-Have Demo Flow

1. Ingestion sends one valid sensor payload every few seconds.
2. Backend receives payload and returns anomaly response.
3. Frontend shows live readings + anomaly badge + score.
4. One explainability field (reason) is visible in UI.

If this flow works end-to-end, you have a presentable MVP.

### Suggested 48-Hour Time Plan

1. Hour 0-6:
   - Freeze contract in contracts.
   - Confirm branch ownership.
   - Start backend mock + frontend mock view.
2. Hour 6-30:
   - Implement real ingestion path.
   - Replace mock backend response with model/baseline response.
   - Connect frontend to real API.
3. Hour 30-40:
   - Stabilize: bug fixes, latency cleanup, error handling.
   - Improve model reason quality and dashboard clarity.
4. Hour 40-48:
   - Demo script rehearsal.
   - Prepare fallback path (recorded data replay).
   - Freeze new features.

### Hard Rules For Fast Delivery

1. No schema changes after midpoint unless critical.
2. No major refactor in last phase.
3. Every stream must keep a fallback:
   - ML fallback: deterministic score logic.
   - Ingestion fallback: replay JSON payload file.
   - Frontend fallback: local mock data toggle.
4. Stop adding features when the full pipeline works once.

### Demo-First Priorities

1. Reliability over perfect model accuracy.
2. Clear anomaly explanation over fancy UI effects.
3. End-to-end integration over isolated module quality.