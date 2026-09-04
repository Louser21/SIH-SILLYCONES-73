# SIH-SILLYCONES-73 Repo Flow

## What This Repo Is

This repository is a 48-hour hackathon monorepo for one team of 6 contributors.

It combines:

- Data ingestion (simulated or MQTT)
- Backend API (FastAPI)
- ML anomaly logic (baseline now, improved model later)
- Frontend dashboard (Next.js)
- Edge placeholder (ESP32 integration later)

The main objective is to deliver a stable end-to-end anomaly detection demo within 48 hours.

## Complete Folder and Subfolder Map

This is what each folder does and how it should be used.

### Root

- README.md: team playbook and setup.
- REPO_FLOW.md: architecture and flow reference.
- CONTRIBUTING.md: branch and PR rules.
- .env.example: shared environment variable template.
- .gitignore: ignored files.
- docker-compose.yml: local multi-service runtime.

### backend/

- backend/app/: FastAPI source code.
- backend/app/routes/: HTTP endpoints.
   - health.py: service status endpoint.
   - anomaly.py: anomaly API endpoint and response contract enforcement.
- backend/app/services/: business logic layer (model call wrappers, orchestration).
- backend/app/models/: request/response and domain models (expand here as app grows).
- backend/requirements.txt: backend Python dependencies.
- backend/Dockerfile: backend container image definition.

### frontend/

- frontend/app/: Next.js app routes/pages.
- frontend/components/: UI components.
- frontend/lib/: API client, helpers, shared frontend utilities.
- frontend/package.json: frontend dependencies and scripts.

### ml/

- ml/preprocessing/: cleaning, normalization, seasonal baseline prep.
- ml/features/: feature engineering pipeline.
- ml/models/: model implementations.
   - ml/models/isolation_forest/: Isolation Forest artifacts/code.
   - ml/models/autoencoder/: Autoencoder artifacts/code.
- ml/anomaly_detection/: inference, score calibration, reason generation.
- ml/requirements.txt: ML Python dependencies.

### ingestion/

- ingestion/simulator/: synthetic payload generators.
- ingestion/mqtt/: MQTT publisher/subscriber connectors.
- ingestion/README.md: ingestion usage notes.

### edge/

- edge/esp32/: future ESP32 firmware/integration stubs.

### contracts/

- contracts/anomaly.schema.json: JSON schema contract.
- contracts/openapi.yaml: API contract for backend/frontend integration.

## System Flow (End-to-End)

1. Sensor payload is generated or received.
2. Ingestion sends payload to backend endpoint.
3. Backend validates payload against contract.
4. Backend computes or requests anomaly score.
5. Backend returns standardized response.
6. Frontend displays reading, anomaly status, score, and reason.

## Folder-to-Folder Runtime Flow

Use this as the source of truth for who sends what to whom.

1. ingestion/simulator or ingestion/mqtt -> backend/app/routes/anomaly.py
   - Sends sensor payload in contract format.
2. backend/app/routes/anomaly.py -> backend/app/services/
   - Route validates input and delegates scoring logic.
3. backend/app/services/ -> ml/anomaly_detection/
   - Service calls ML inference logic (or baseline fallback).
4. ml/anomaly_detection/ -> ml/features/ and ml/models/
   - Uses engineered features and selected model.
5. ml/* result -> backend/app/services/ -> backend/app/routes/anomaly.py
   - Returns anomaly, score, reason.
6. backend/app/routes/anomaly.py -> frontend/lib/
   - Frontend fetches standardized API response.
7. frontend/lib/ -> frontend/components/ and frontend/app/
   - Dashboard renders live state for demo.

Contract boundary:

- All cross-folder runtime traffic must match contracts/anomaly.schema.json.
- Backend OpenAPI must stay aligned in contracts/openapi.yaml.

## Development Ownership Flow (Who Touches What)

1. FS-3 owns ingestion/simulator and ingestion/mqtt.
2. FS-1 owns backend/app/routes plus backend app wiring.
3. ML-1/ML-2/ML-3 own ml/preprocessing, ml/features, ml/models, ml/anomaly_detection.
4. FS-2 owns frontend/app, frontend/components, frontend/lib.
5. Contract edits in contracts/ require all streams to recheck compatibility.

## Data Contract

All components must follow the same payload shape.

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

- contracts/anomaly.schema.json
- contracts/openapi.yaml

## Folder Responsibilities

- backend/: API routes, request validation, orchestration
- frontend/: dashboard UI and API consumption
- ml/: preprocessing, features, anomaly models, evaluation
- ingestion/: data simulation and MQTT pipeline
- edge/: optional hardware integration
- contracts/: shared interface definitions

## Why `backend/app/routes/anomaly.py` Exists

`anomaly.py` is the stable API layer for integration.

- It lets frontend and ingestion integrate from day one.
- It keeps the response shape fixed while ML improves internally.
- It can start with a deterministic baseline and later call real ML logic.

This prevents cross-team blocking during a short hackathon.

## 48-Hour Execution Flow

1. Hour 0-6:
   - Freeze contract.
   - Ensure backend endpoint runs.
   - Build frontend with mock/real toggle.
2. Hour 6-30:
   - Connect ingestion to backend.
   - Replace baseline scoring with ML output.
   - Connect dashboard to live backend response.
3. Hour 30-40:
   - Stabilize errors, logging, and latency.
   - Improve reason text quality.
4. Hour 40-48:
   - Freeze features.
   - Rehearse demo.
   - Keep fallback path ready.

## Fallback Path (If Anything Breaks)

- If MQTT fails: replay sample JSON payloads.
- If ML model fails: return deterministic baseline score.
- If frontend integration fails: switch to local mock mode with recorded API responses.

Rule: a working fallback is better than a broken advanced feature.

## Git and Merge Flow

1. Work only in feature branches.
2. Commit small units with clear messages.
3. Open PR to main.
4. Get at least one review.
5. Merge only if contract compatibility is preserved.

Never push directly to main.

## Definition of Success

The repo is successful for this hackathon if:

1. A valid sensor payload enters the system.
2. Backend returns anomaly response in contract format.
3. Frontend shows live status and reason.
4. Demo works reliably on demand.
