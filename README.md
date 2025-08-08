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
- Frontend placeholder: http://localhost:5173/ (enter Gemini key and plan)
- Redis: localhost:6379
- Postgres: localhost:5432

## LLM (Gemini) setup

- Open the frontend at `/` and submit your Gemini API key.
- Programmatically, set via:

```bash
curl -X POST http://localhost:8000/api/v1/config/llm/gemini-key \
  -H 'Content-Type: application/json' \
  -d '{"api_key":"YOUR_GEMINI_API_KEY"}'
```

## Plan safe payload tests (demo)

```bash
curl -X POST http://localhost:8000/api/v1/planner/plan \
  -H 'Content-Type: application/json' \
  -d '{"method":"GET","url":"https://example.com/api/items","params":[{"name":"q","location":"query"}]}'
```

The planner asks Gemini to propose only non-destructive, low-risk probes and returns a concise JSON plan.

## Next steps

- Wire planner output to the probe engine to generate and send safe payloads.
- Implement discovery (crawler + Playwright), parameter extraction, and baseline probes.
- Add analyzer endpoint using Gemini to compare baseline/probe responses.
- Replace placeholder frontend with React + Tailwind dashboard.
