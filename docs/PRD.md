# PRD — Fire TV Enhanced Experience: Prototype → Production-Style Full Stack

## 1. Project overview

Modernize the Amazon HackOn Season 5 prototype into a single, coherent, end-to-end full-stack application: an AI-personalized Fire TV experience with mood-aware recommendations, real-time social watch parties, and cross-OTT content discovery. The original purpose, screens, and algorithms are preserved; the delivery changes from "UI showcase + disconnected simulations" to "one deployable product".

## 2. Problem statement

Content discovery on TV platforms is fragmented across OTT apps, ignores the viewer's current mood/context, and is a solitary experience. The prototype demonstrated solutions to all three (multi-modal personalization, group consensus recommendations, synchronized social viewing) but as isolated artifacts. Nothing is connected, persisted, tested, or deployable.

## 3. Current architecture & limitations

See `docs/AUDIT.md`. Summary of limitations:

- Frontend has zero network calls; all data hardcoded; production image pipeline broken.
- Nine Python algorithm modules run standalone on synthetic data; four are duplicated verbatim.
- Watch party is local-only state; the room role model exists only as a file-based CLI simulator.
- No auth, no database, no tests, no CI, no deployment story, no environment management.

## 4. Improvement opportunities

1. Unify all Python algorithms into one **FastAPI service** with a clean domain-layered structure.
2. Give the catalog a real **database** (SQLite dev / Postgres prod) seeded with the existing 45 titles.
3. Make watch parties **actually real-time** with WebSockets, porting the simulator's role/permission model.
4. Wire the frontend through a **typed API client + TanStack Query** (already installed, unused).
5. Put every AI capability behind a **provider interface** so facial/voice/LLM providers are swappable and optional — free/local first.
6. Add **JWT auth with guest mode** so the demo flow stays one-click.
7. Tests, Dockerfiles, env management, README that a new developer can follow.

## 5. Functional requirements

### FR1 — Catalog
- List/search/filter movies by genre, platform, category; hero slides; single-movie fetch.
- Catalog seeded from the existing 45-title dataset; images served correctly in dev and prod builds.

### FR2 — Personal recommendations (Statement 1)
- `POST /api/recommendations/personal`: accepts optional mood/time/behavior signals; returns ranked movies with consensus scores and per-modality explanation.
- Scoring must reproduce the prototype math: user 4×6 × movie 6×4 → diagonal → modality weights (time .30, behavior .25, voice .25, facial .20) → 0.8·consensus + 0.2·popularity.
- History-aware: watch history aggregated with exponential decay (α=1, β=0.5) and blended 80/20 with live signals.
- Adaptive weights: feedback endpoint applies `w' = 0.6·w + 0.4·feedback` per user, persisted.
- Movie compatibility matrices are **deterministic** functions of genre/year/rating (seeded), replacing per-run randomness.

### FR3 — Group recommendations (Statement 2)
- `POST /api/recommendations/group`: aggregates member 6×6 emotion×modality matrices with 70% median + 30% mean; consensus = 0.6·raw + 0.2·popularity + 0.2·suitability; returns ranked list with agreement (std-dev) and selectability metrics.

### FR4 — Context analysis (Statements 1–2)
- Mood: `POST /api/analysis/mood` behind a `MoodProvider` interface — default heuristic text/emoji provider (zero deps); optional ONNX facial provider (repo's `best.onnx` via onnxruntime); optional local LLM provider (Ollama / OpenRouter free tier). Providers degrade gracefully when unavailable.
- Behavior: `POST /api/analysis/behavior` — the 6-cluster rule classifier over MediaSession-style events.
- Time: `GET /api/analysis/time-block` — 6 time blocks with content vibes.
- Emoji: `POST /api/analysis/emoji` — 12-emoji → 6-emotion mapping with dominant mood + confidence.

### FR5 — Watch parties (Statements 2–3)
- REST: create room (returns short join code), join by code (optional password, validated this time), room info.
- WebSocket: presence, chat, emoji reactions, synchronized queue (add/remove/play-next), polls (create/vote/end), admin actions (promote/demote/kick, global chat/reaction toggles) — the simulator's permission model enforced server-side.
- Two browser tabs joined to the same room must see each other's messages/reactions/queue changes live.

### FR6 — Auth & social
- Register/login (JWT, pbkdf2), guest sessions for demo flow.
- Friends: list, requests, suggestions; friend movie suggestions feed (seeded to match existing UI).
- Watch history + my-list/watch-later persisted per user.

### FR7 — Frontend integration
- All screens keep their existing look; data now flows from the API via TanStack Query with loading/error states and graceful fallback to the bundled dataset when the backend is unreachable (static-demo mode survives).

## 6. Non-functional requirements

- **NFR1**: Zero paid services. Default install runs fully offline; optional AI providers are free/local.
- **NFR2**: Backend p50 < 100 ms for recommendation calls at this catalog size.
- **NFR3**: Typed end-to-end (Pydantic v2 schemas ↔ TS types).
- **NFR4**: Test coverage over all ported algorithm math, room lifecycle, and auth.
- **NFR5**: 12-factor config: everything via env vars with committed `.env.example`.
- **NFR6**: One-command dev up (docker compose or two obvious commands).

## 7. Proposed architecture

```
frontend/  (React 18 + Vite + TS + Tailwind + shadcn, TanStack Query, WS client)
   └─ src/lib/api.ts, src/api/hooks.ts, src/api/ws.ts  ── HTTP+WS ──┐
backend/   (FastAPI + Pydantic v2 + SQLAlchemy 2 + uvicorn)          │
   ├─ app/core        config, security, logging                      │
   ├─ app/db          engine, models, seed                           │
   ├─ app/schemas     Pydantic DTOs                                  │
   ├─ app/services    engines: personal_recs, group_recs, history,   │
   │                  weights, mood (providers/), behavior, time,    │
   │                  emoji, rooms (manager + permissions)           │
   ├─ app/api         routers: movies, recommendations, analysis,    │
   │                  rooms (REST+WS), auth, friends, users          │
   └─ tests/                                                         │
research/  (original Statement-1/2/3 preserved as provenance) ───────┘
```

- **DB**: SQLite by default (`DATABASE_URL` swappable to Postgres/Neon).
- **Realtime**: in-process room manager + WebSocket fan-out (single-node; Redis pub/sub noted as scale-out path).
- **AI providers**: `MoodProvider` protocol; registry selects by env (`MOOD_PROVIDER=heuristic|onnx|ollama|openrouter`); paid providers addable later behind the same interface.

## 8. Technology recommendations

Keep React/Vite/Tailwind/shadcn (current, good). Backend: FastAPI (async, WS-native, Pydantic typing) over Flask/Django — best fit for porting NumPy engines and WebSockets in one service. SQLAlchemy 2.0 typed ORM. No Neo4j/AppSync/Personalize — the deployed math never used them and free-tier constraints rule them out; the graph-ish "friends watching" features are served relationally.

## 9. Migration strategy

Strangler-style, additive: restructure folders first (git mv, history preserved), stand the backend up alongside the untouched UI, then wire screens one flow at a time with a fallback to bundled data — so the app is demoable at every intermediate commit. Original Python kept under `research/` as provenance; duplicated copies noted, canonical logic lives in `backend/app/services`.

## 10. Risks

| Risk | Mitigation |
|---|---|
| WS room state races | Single asyncio-guarded manager; per-room locks |
| ONNX/ultralytics deps heavy or unavailable | Optional extra; provider falls back to heuristic |
| Frontend regressions during wiring | Fallback to bundled data; screen-by-screen commits |
| 44 MB images bloat builds | Move to `public/`, drop `images.zip`, keep git history as-is (no rewrite) |
| Python 3.14 wheel availability | Pin currently-supported versions; venv per backend |

## 11. Assumptions

- Single-node deployment is acceptable for demo scale; Redis/Postgres are the documented scale-up path.
- The 45-title dataset remains the catalog (TMDB import is a documented future improvement).
- Voice-mood and VR-filter notebooks stay research artifacts (Colab-bound); their outputs enter the system as mood signals via the API contract.

## 12. Execution roadmap & success criteria

Roadmap: see `docs/EXECUTION_PLAN.md` (10 phases).

Success = all of:
1. `pytest` green; `npm run build` + `tsc` green.
2. Fresh clone → README steps → working app in <10 minutes with no credentials.
3. Home page rows served by the recommendation API with mood/time context.
4. Two tabs in one room exchange chat/reactions/queue updates in real time.
5. Auth (or guest) gates persisted lists/history.
6. No paid API required anywhere; providers swappable via env.
