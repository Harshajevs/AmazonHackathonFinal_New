# Execution Plan — Fire TV Enhanced Experience Modernization

Each phase is small, independently testable, and lands as one or more logical commits. Rollback for every phase: revert the phase's commits — phases are additive and the UI keeps a bundled-data fallback until final wiring, so the app remains demoable between phases.

## Phase 0 — Repository restructure
- **Objective**: monorepo layout without losing history.
- **Scope**: `git mv "FireTV(UI)_Website" frontend`, `Statement-{1,2,3}` → `research/statement-{1,2,3}`, images → `frontend/public/images`, drop `images.zip`, move PDF → `docs/`.
- **Files**: top-level only. **Risk**: broken image refs — fixed because `/images/*` now resolves from `public/`. **Test**: `npm run dev` renders; `npm run build` includes images.

## Phase 1 — Backend scaffold
- **Objective**: runnable FastAPI service with config, logging, CORS, SQLite, seeded catalog.
- **Scope**: `backend/app/{main,core,db,schemas,api}`, movie seed extracted from `movieData.ts`, `/api/movies` endpoints, `/health`.
- **Risk**: Python 3.14 wheels — pin tested versions. **Test**: uvicorn boots; `GET /api/movies` returns 45 titles; pytest smoke.

## Phase 2 — Recommendation engines
- **Objective**: port all five algorithm modules as pure, deterministic, unit-tested services.
- **Scope**: `services/recommendations/` (matrices, personal, history, weights, group, evolution) + `/api/recommendations/*` routers.
- **Risk**: fidelity to prototype math — tests assert weights, formulas, normalization invariants. **Test**: unit tests on known inputs; endpoint returns ranked catalog.

## Phase 3 — Context analysis services
- **Objective**: mood/behavior/time/emoji services; mood behind a provider interface (heuristic default, optional ONNX/Ollama/OpenRouter).
- **Scope**: `services/analysis/` + `/api/analysis/*`.
- **Risk**: optional heavy deps — lazy import + fallback. **Test**: unit tests per service; provider fallback test.

## Phase 4 — Watch-party rooms
- **Objective**: real-time rooms with the simulator's role model.
- **Scope**: `services/rooms/` (state, permissions, manager), REST create/join, `/ws/rooms/{code}` WebSocket.
- **Risk**: concurrency — per-room asyncio locks; connection cleanup on disconnect. **Test**: pytest with two TestClient WS sessions exchanging chat/queue/poll events; permission denials asserted.

## Phase 5 — Auth, users, social
- **Objective**: JWT auth + guest mode; friends, history, my-list persisted.
- **Scope**: `core/security.py`, users/friends models + routers, seed friends.
- **Risk**: none significant. **Test**: register→login→me flow; guest flow; friends endpoints.

## Phase 6 — Frontend API layer
- **Objective**: typed client + TanStack Query hooks + WS client + env config; bundled-data fallback.
- **Scope**: `src/lib/api.ts`, `src/api/*`, `.env.example`, remove lovable-tagger.
- **Test**: `tsc`/build green with and without backend running.

## Phase 7 — Screen wiring
- **Objective**: home rows (personal picks / mood / time-block / trending) from API; friends page from API; login/guest screen; loading & error states.
- **Risk**: visual regressions — keep markup, change data sources only. **Test**: build green; manual smoke; fallback mode identical to old behavior.

## Phase 8 — Realtime watch party wiring
- **Objective**: create/join through REST; chat/reactions/queue/presence over WS; two tabs sync.
- **Test**: manual two-tab session; WS reconnect handling.

## Phase 9 — Hardening, packaging, docs
- **Objective**: Dockerfiles + compose, `.env.example`s, README rewrite, deployment guide (Render backend + Vercel frontend + Neon Postgres — all free tiers), final full test run.
- **Test**: `docker compose up` serves both; fresh-clone instructions verified.

## Commit conventions
Conventional-commit style, one logical change each, authored solely by Harshajevs, no AI attribution or co-author trailers.
