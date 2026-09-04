# SIH-SILLYCONES-73

Monorepo for your 6-member hackathon team building AI/ML, backend, dashboard, and ingestion in parallel.

The goal of this README is to help your team avoid blind coding, stay unblocked, and ship a stable demo within 48 hours.

For a full system overview and execution flow, read `REPO_FLOW.md`.

## 1) Repo Philosophy (Read First)

- One monorepo, clear contracts, independent streams.
- Contract-first integration: interface first, implementation second.
- Small PRs, fast reviews, frequent merges.
- Every branch should remain runnable, even if features are incomplete.

If you follow this, your team can work simultaneously without constant conflicts.

## 2) Monorepo Layout

```text
SIH-SILLYCONES-73/
├── backend/        # FastAPI and app logic
├── frontend/       # Next.js dashboard
├── ml/             # models, preprocessing, evaluation
├── ingestion/      # MQTT and simulators
├── edge/           # ESP32 (later)
├── contracts/      # shared API schemas/specs
├── docker-compose.yml
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
└── README.md
```

## 3) Team Ownership (6 Members)

- ML-1: preprocessing + seasonal baseline
- ML-2: Isolation Forest + Autoencoder
- ML-3: SHAP + evaluation + streaming integration
- FS-1: FastAPI backend + APIs
- FS-2: Next.js dashboard/UI
- FS-3: ingestion + DB + WebSocket

Rule: ownership means primary responsibility, not exclusive access.

## 4) Safe Git Workflow

Never push directly to main.

Core branches:

- main
- feature/ml-anomaly
- feature/ml-seasonality
- feature/backend
- feature/dashboard
- feature/mqtt
- feature/esp32

Typical flow:

```bash
git checkout main
git pull origin main
git checkout -b feature/dashboard
# work
git add .
git commit -m "Add live sensor chart"
git push -u origin feature/dashboard
```

Then open PR, get review, merge to main.

## 5) Shared API Contract (Single Source of Truth)

Everyone in your team must follow the same payload model.

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

Change policy:

- If contract changes, update both files in the same PR.
- Label PR title with CONTRACT CHANGE.
- Notify all stream owners before merge.

## 6) How To Code Safely (Instead of Blind Coding)

Before writing code:

1. Read contract and your folder ownership.
2. Write a tiny task note in PR description: input, output, side effects.
3. Define done criteria (example: endpoint returns valid score in [0,1]).

While coding:

1. Keep functions small and deterministic where possible.
2. Avoid hard-coding cross-team assumptions.
3. Add clear errors for invalid payloads.
4. Commit every logical step, not once at the end.

Before pushing:

1. Pull main and resolve conflicts locally.
2. Run local checks for your area.
3. Verify no secrets were committed.
4. Update docs if behavior changed.

## 7) Integration Strategy (Daily, Not Last Day)

Run short integration cycles every day:

1. Backend exposes stable endpoint and mock response.
2. Frontend consumes real endpoint or stable mock toggle.
3. ML returns contract-compliant response even with baseline model.
4. Ingestion sends contract-compliant data (real or simulated).

Do not wait for final model accuracy before integrating.

## 8) Workaround Playbook (When Blocked)

If one team is blocked by another, do not stop development.

Use one of these:

1. Mock endpoint:
   - Backend unavailable -> frontend uses local JSON/mock service.
2. Stub model:
   - ML incomplete -> backend returns deterministic placeholder score.
3. Replay data:
   - MQTT unstable -> ingestion replays recorded sample payloads.
4. Feature flag:
   - Keep incomplete features hidden but merge-ready.

Every workaround must include:

- TODO owner
- removal condition
- target removal date/time

## 9) Day-1 Setup Commands

Create GitHub repo and push scaffold:

```bash
git init -b main
git add .
git commit -m "Initial monorepo scaffold"
git remote add origin <your-github-repo-url>
git push -u origin main
```

## 10) Local Run Guide

### Docker (Recommended For 48-Hour Integration)

Use Docker during integration windows in the 48-hour sprint to keep environments consistent.

Why use it:

1. Same environment for all contributors.
2. Fast end-to-end startup for backend + frontend + MQTT.
3. Fewer local dependency issues when time is limited.

Commands:

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

When to skip Docker:

1. You are developing only one module and want fastest iteration.
2. Docker is slow or unavailable on your machine.

In that case, run services directly using the local commands below.

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
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