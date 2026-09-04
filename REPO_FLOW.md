# SIH-SILLYCONES-73 Repo Flow

## What This Repo Is

This repository is the foundation for a 48-hour SIH 2026 hackathon project.

It combines:

- ingestion (simulated or MQTT input)
- FastAPI backend
- production ML inference embedded inside the backend
- frontend dashboard
- optional edge integration later

The main objective is to make the system work end-to-end with a stable API contract and a baseline model before the real model is added.

## Complete Folder and Subfolder Map

### Root

- README.md: team playbook and setup
- REPO_FLOW.md: architecture and flow reference
- CONTRIBUTING.md: branch and PR rules
- docker-compose.yml: local multi-service runtime
- .github/: CI/CD workflows
- .env.example: shared environment template
- .gitignore: ignored files

### backend/

- backend/app/: FastAPI app source
- backend/app/main.py: app entrypoint and startup configuration
- backend/app/api/routes/: HTTP endpoints
  - health.py: health check
  - predict.py: anomaly prediction request/response route
- backend/app/ml/: production ML logic inside backend
  - inference/predictor.py: temporary baseline predictor
  - model/: future model wrappers or artifacts
  - service.py: backend-facing ML interface
- backend/requirements.txt: backend Python dependencies
- backend/.env.example: local environment config

### frontend/

- frontend/app/: Next.js routes/pages
- frontend/components/: UI components
- frontend/lib/: shared helpers and API client logic
- frontend/package.json: frontend dependencies and scripts

### ingestion/

- ingestion/simulator/: synthetic payload generator
- ingestion/mqtt/: MQTT publisher/subscriber code

### edge/

- edge/esp32/: future hardware/integration stubs

### contracts/

- contracts/sensor-reading.schema.json: input contract
- contracts/anomaly-prediction.schema.json: output contract
- contracts/openapi.yaml: OpenAPI contract
- contracts/anomaly.schema.json: legacy compatibility placeholder

## System Flow (End-to-End)

1. Sensor data is generated or received.
2. Ingestion sends sensor payload to backend.
3. Backend validates input against the contract.
4. Backend calls the ML predictor inside backend/app/ml/.
5. Backend returns anomaly, score, and reason.
6. Frontend renders the response for demo purposes.

## Runtime Flow

1. ingestion/simulator or ingestion/mqtt -> backend/app/api/routes/predict.py
   - sends sensor payload in contract format
2. backend/app/api/routes/predict.py -> backend/app/ml/service.py
   - route delegates to ML service
3. backend/app/ml/service.py -> backend/app/ml/inference/predictor.py
   - loads and uses predictor logic
4. predictor -> backend response
   - returns anomaly, score, and reason
5. backend response -> frontend
   - dashboard displays score and anomaly status

Contract boundary:

- All runtime traffic must match the sensor-reading and anomaly-prediction schema.
- OpenAPI must stay aligned with contracts/openapi.yaml.

## ML Placement Rule

The ML code is intentionally not a separate service in this phase.

This repository follows:

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

This avoids unnecessary infrastructure and keeps the system easy to maintain during a short hackathon.

## Development Ownership Flow

1. FS-3 owns ingestion/simulator and ingestion/mqtt.
2. FS-1 owns backend app wiring and API contracts.
3. ML owners work inside backend/app/ml/.
4. FS-2 owns frontend/app, frontend/components, frontend/lib.
5. Contract edits in contracts/ require all streams to recheck compatibility.

## Data Contract

Input:

```json
{
  "station_id": "S01",
  "timestamp": "2026-09-05T12:30:00Z",
  "temperature": 34.2,
  "humidity": 71.0
}
```

Output:

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

## Folder Responsibilities

- backend/: API routes, validation, orchestration, and ML integration
- frontend/: dashboard UI and API consumption
- ingestion/: data simulation and MQTT pipeline
- edge/: future hardware integration
- contracts/: shared interface definitions

## Why the Backend Owns ML for Now

Keeping ML inside the backend ensures:

- no extra server to manage
- no added deployment complexity during a 48-hour sprint
- a stable API for all teams
- easier future replacement of the baseline predictor with the real model

## 48-Hour Execution Flow

1. Hour 0-6:
   - freeze input/output contract
   - ensure backend endpoint runs
   - build frontend with mock or live toggle
2. Hour 6-30:
   - connect ingestion to backend
   - replace rule-based predictor with real model later
   - connect dashboard to live backend response
3. Hour 30-40:
   - stabilize logging, errors, and latency
4. Hour 40-48:
   - rehearse demo
   - keep fallback baseline ready

## Fallback Path

- If ingestion fails: replay sample JSON payloads
- If ML fails: return a deterministic baseline score
- If frontend fails: use a local mock mode with recorded responses

Rule: a working fallback is better than a broken advanced feature.

## Git and Merge Flow

1. Work only in feature branches.
2. Commit small units with clear messages.
3. Open PR to main.
4. Get at least one review.
5. Merge only if contract compatibility is preserved.

Never push directly to main.

## Definition of Success

The repo is successful if:

1. A valid payload enters the system.
2. Backend returns a contract-compliant anomaly response.
3. Frontend displays live status and reason.
4. The demo works reliably on demand.
