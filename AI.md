# AI Coding Rules for SIH-SILLYCONES-73

This is a 6-member, 48-hour hackathon project. Keep solutions simple, modular, and easy for teammates to understand and extend.

## 1. Inspect before changing

- Read the relevant files and existing structure before making changes.
- Do not assume code, APIs, or behavior already exist.
- Do not modify unrelated files.
- Check the current architecture and folder responsibilities before editing.

## 2. Keep the architecture intact

- Respect the repo structure and existing conventions.
- Do not introduce new frameworks, services, databases, microservices, or infrastructure unless there is a clear need.
- Keep ML inference inside `backend/app/ml/`.
- Do not create a separate ML server unless explicitly requested.
- Follow the shared contracts in `contracts/` when building or changing APIs or payloads.

## 3. Make the smallest necessary change

- Prefer the smallest clean fix that solves the task.
- Do not over-engineer for the hackathon.
- Do not rewrite working code just to use a different pattern.
- Avoid unnecessary abstractions, dependencies, and complexity.

## 4. Contracts first

- Check `contracts/` before creating or modifying request/response formats.
- If a contract must change, update the affected schema and consumers together.
- Do not silently change API/data shapes.
- Keep producers and consumers aligned with shared contract files.

## 5. Team workflow and Git safety

- Assume multiple developers are working in parallel through branches and PRs.
- Stay within the scope of the requested task.
- Avoid touching files outside the area being changed.
- Do not hardcode secrets or commit `.env` files.
- Never commit credentials, tokens, API keys, or other sensitive data.

## 6. Testing

- After making changes, run the smallest relevant checks for the affected functionality.
- Verify imports and basic execution.
- If the change touches multiple modules or an end-to-end flow, validate the relevant flow.

## 7. Major decisions

- If a requested change requires a major architectural decision, stop and ask before implementing it.
- Keep the solution practical for a hackathon sprint and understandable by teammates.

## 8. Final task report

At the end of each task, report:

- Changed: what was modified
- Tested: what was run and whether it passed
- Risks: assumptions, limitations, or remaining issues

## Core principle

Keep everything simple, modular, contract-safe, and easy for a 6-person team to understand and extend during a 48-hour sprint.
