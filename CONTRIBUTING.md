# Contributing Guide

## Branching

- Protected branch: `main`
- Working branches:
  - `feature/backend`
  - `feature/ml-baseline`
  - `feature/ml-model`
  - `feature/dashboard`
  - `feature/mqtt`
  - `feature/esp32`

## Workflow

1. Pull latest main:
   ```bash
   git checkout main
   git pull origin main
   ```
2. Create or switch to your feature branch:
   ```bash
   git checkout -b feature/<name>
   ```
3. Commit small, meaningful changes:
   ```bash
   git add .
   git commit -m "<clear message>"
   ```
4. Push and create PR:
   ```bash
   git push -u origin feature/<name>
   ```

## Pull Request Rules

- At least 1 reviewer before merge.
- Keep PRs small and focused.
- Do not mix backend API changes with frontend UI work in one PR.
- Do not mix ML logic and ingestion changes in one PR unless they are tightly coupled.

## Contract-First Rule

The baseline contract is:

- Input: `contracts/sensor-reading.schema.json`
- Output: `contracts/anomaly-prediction.schema.json`
- API spec: `contracts/openapi.yaml`

If a contract changes, update the relevant schema and OpenAPI spec in the same PR.

## Backend + ML Rule

For this repo, ML inference belongs under the backend. Do not create a separate ML API/server during the foundation phase.

The expected route is:

```text
POST /api/v1/predict
   ↓
backend
   ↓
backend/app/ml/service.py
   ↓
backend/app/ml/inference/predictor.py
   ↓
response model
```

This keeps the API stable while the real ML model is introduced later.

## Local Validation Checklist

Before creating a PR, make sure:

- backend health route works
- prediction route returns a valid anomaly payload
- input/output contract matches the schema
- no secrets are committed
- the feature branch can run on a fresh clone
