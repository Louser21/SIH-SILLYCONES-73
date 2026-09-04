# SIH-SILLYCONES-73

Monorepo for a 6-member hackathon team building AI/ML, backend, dashboard, and ingestion in parallel.

The goal of this README is to help the team avoid blind coding and keep everyone unblocked.

## 1) Repo Philosophy (Read First)

- One monorepo, clear contracts, independent streams.
- Contract-first integration: interface first, implementation second.
- Small PRs, fast reviews, frequent merges.
- Every branch should remain runnable, even if features are incomplete.

If you follow this, 6 people can work simultaneously without constant conflicts.

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

All teams must follow the same payload model.

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