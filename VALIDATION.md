# Validation record

Verified in this workspace:

- Backend: 22 pytest tests passed, using isolated SQLite databases.
- Frontend: Vue/TypeScript production build passed; 2 Vitest tests passed.
- Live HTTP smoke test: created and uploaded a consistent synthetic case, ran all analysis nodes, retrieved persisted dashboard counts and a current CAM. DSCR was 4.0607 for the supplied consistent fixture.
- OpenAPI JSON and Vite HTML returned HTTP 200.
- Docker Compose YAML parsed successfully.
- Chromium browser flow passed: token login, persisted dashboard, case analysis, CAM print-to-PDF, reviewer approval and mock-ledger display. Mobile viewport had no page-level horizontal overflow; no browser page errors were observed.
- Desktop/mobile screenshots and the first printed CAM page were visually inspected. The sample CAM printed to 5 pages with its evidence appendix.
- The actual Agno/Ollama adapter was instantiated against an unavailable endpoint; graceful fallback passed.

Covered backend behavior: EMI/amortization and zero-interest handling, unknown/zero DSCR denominators, period/tolerance rules, all six adverse financial/document scenarios, authorized atomic approval, unauthorized review (403), duplicate approval prevention (409), additional evidence and stale-CAM invalidation, checkpoint retry, crash recovery, append-only audit protection, document prompt injection isolation, missing debt, rejected file input, strict dates/amounts, template-PDF source extraction, unrecognized PDF rejection, failed document approval blocking, reviewer request resolution, and unavailable LLM fallback.

Not verified here: a Docker image build or PostgreSQL runtime (Docker unavailable), successful inference on an installed Ollama model (no model/hardware supplied), and real-world document accuracy. General document formats intentionally require manual mapping. OCR support is implemented but scanned-page extraction quality has not been evaluated.

To run PostgreSQL integration tests in the target Compose environment, use a separate test database (never production data):

```powershell
docker compose exec db createdb -U msme msme_test
docker compose exec -e TEST_DATABASE_URL=postgresql+psycopg://msme:local-db-change-me@db:5432/msme_test api python -m pytest -q
```

Substitute your configured database password, URL-encoded if necessary. Tests append synthetic records to that dedicated database.

All thresholds are demo configuration. No measured extraction accuracy, predictive credit performance, token savings, latency or cost claims are made.
