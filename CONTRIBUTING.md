# Contributing Guide

## Branching

- Protected branch: `main`
- Working branches:
  - `feature/ml-anomaly`
  - `feature/ml-seasonality`
  - `feature/backend`
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
- Do not mix ML model logic and frontend UI changes in one PR.

## Contract-First Rule

- API payloads must follow `contracts/anomaly.schema.json`.
- If contract changes, update both:
  - `contracts/anomaly.schema.json`
  - `contracts/openapi.yaml`
