# LLM-Assisted Security Testing Framework (MVP)

This repository contains an MVP scaffold for a safe, auditable security testing framework with discovery, safe probe engine, LLM planning/analysis, escalation, and a simple dashboard.

## Quickstart (Epic 0)

1. Copy `.env.example` to `.env` and adjust as needed.
2. Build and run services:

```bash
docker compose up --build
```

Services:
- API: http://localhost:8000/health
- Frontend placeholder: http://localhost:5173/health
- Redis: localhost:6379
- Postgres: localhost:5432

## API (stubs)

- `GET /health` -> status ok
- `POST /api/v1/scan` -> queue a scan
- `GET /api/v1/inventory` -> list inventory
- `GET /api/v1/endpoint/{id}` -> endpoint details
- `POST /api/v1/probe` -> run a probe
- `GET /api/v1/findings` -> list findings
- `POST /api/v1/findings/{id}/approve` -> approve
- `GET /api/v1/report/{finding_id}` -> download report

## Next steps

- Implement discovery (crawler + Playwright), parameter extraction, and baseline probes.
- Add LLM planner/analyzer adapters with safety logging.
- Build React + Tailwind dashboard replacing the placeholder frontend.
