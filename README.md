# Fire TV Together — AI-Powered OTT Personalization

**Team:** OG Strikes Back · IIT Ropar · Amazon HackOn Season 5

An AI-personalized Fire TV experience: explainable, mood-aware content recommendations across OTT catalogs, and real-time social watch parties with chat, reactions, synchronized queues, polls, and server-enforced roles.

Originally a hackathon prototype (a showcase UI plus standalone Python algorithm simulations), now modernized into a single integrated full-stack application. The original prototypes are preserved under [`research/`](research/); the product documents live in [`docs/`](docs/) ([Audit](docs/AUDIT.md) · [PRD](docs/PRD.md) · [Execution Plan](docs/EXECUTION_PLAN.md)).

## Architecture

```
┌────────────────────────┐         HTTP (JSON) + WebSocket        ┌─────────────────────────────┐
│  frontend/             │  ─────────────────────────────────────▶│  backend/                   │
│  React 18 + Vite + TS  │   /api/movies, /api/recommendations,   │  FastAPI + SQLAlchemy 2     │
│  Tailwind + shadcn/ui  │   /api/rooms, /ws/rooms/{code}, ...    │  ├─ services/recommendations│
│  TanStack Query        │                                        │  │   personal 4×6 engine    │
│  RoomSocket (WS)       │◀─────  event envelopes (sequence,  ────│  │   group 6×6 engine       │
└────────────────────────┘        room version, actor, payload)   │  │   history decay, weights │
                                                                  │  ├─ services/analysis       │
        offline fallback: bundled 45-title catalog                │  │   mood providers, time,  │
        keeps the UI fully demoable without the backend           │  │   behavior, emoji        │
                                                                  │  ├─ services/rooms          │
                                                                  │  │   roles + realtime       │
                                                                  │  └─ SQLite / PostgreSQL     │
                                                                  └─────────────────────────────┘
```

**The AI engines** (ported from the hackathon prototypes, made deterministic and unit-tested):

- **Personal recommendations** — a 4×6 user context matrix (time, behavior, voice-mood, facial-mood × six attributes) is matched against per-movie 6×4 compatibility matrices derived from genre affinities. `final = 0.8 × weighted-diagonal-consensus + 0.2 × popularity`. Watch history joins via exponential decay (`e^(-0.5k)`), blended 80/20 with live context. Per-user modality weights adapt from feedback with momentum updates (`w' = 0.6w + 0.4·feedback`).
- **Group recommendations** — each room member contributes a 6×6 emotion × modality matrix; the group is aggregated cell-wise as 70% median + 30% mean; candidates rank by `0.6 × raw + 0.2 × popularity + 0.2 × group-suitability`, with agreement (per-member score deviation) and selectability metrics.
- **Context analysis** — six time-of-day blocks, a six-cluster behavior classifier over playback events, emoji→emotion vectors, and a pluggable mood provider (heuristic by default; optional ONNX facial model, Ollama, or OpenRouter free models — all swappable via one env var, no paid APIs anywhere).
- **Watch parties** — WebSocket rooms with short join codes, hashed passwords, admin/co-admin/member permissions enforced server-side, synced queues, polls with revote semantics, moderation, and ownership transfer.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite 5, Tailwind CSS, shadcn/ui, TanStack Query 5 |
| Backend | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.0, NumPy, PyJWT |
| Database | SQLite (default) or PostgreSQL via `DATABASE_URL` |
| Realtime | Native WebSockets (FastAPI) with event envelopes |
| AI providers | Heuristic (built-in) · ONNX Runtime (facial) · Ollama · OpenRouter free tier |

## Getting started

### Prerequisites

- Node.js 18+ (22 recommended) and npm
- Python 3.12+ (3.14 tested)

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                # optional; defaults work out of the box
uvicorn app.main:app --reload --port 8000
```

The first boot creates `firetv.db` and seeds the 45-title catalog plus a demo account (`demo` / `demo1234`) with a populated social graph. API docs: <http://localhost:8000/docs>.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env                # sets VITE_API_URL=http://localhost:8000
npm run dev
```

Open <http://localhost:8080>. A guest session is created automatically. If the backend is not running, the app stays fully usable on the bundled demo catalog and clearly says so.

### 3. Try the watch party

1. Open two browser tabs (or one normal + one private window).
2. Tab A: *Create Room* → pick a movie → the room header shows a 6-character join code (click to copy).
3. Tab B: *Join Room* → enter the code.
4. Chat, emoji reactions, and queue changes sync live between tabs.

### Docker (one command)

```bash
docker compose up --build
# frontend on http://localhost:3000, backend on http://localhost:8000
```

## Environment variables

### Backend (`backend/.env`)

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./firetv.db` | Any SQLAlchemy URL (Postgres/Neon supported) |
| `SECRET_KEY` | change-me | JWT signing key — set a long random value in production |
| `CORS_ORIGINS` | localhost dev ports | Comma-separated allowed origins |
| `MOOD_PROVIDER` | `heuristic` | `heuristic` · `onnx` · `ollama` · `openrouter` |
| `ONNX_MODEL_PATH` | research checkpoint | Facial-emotion ONNX model (needs `requirements-ml.txt`) |
| `OLLAMA_BASE_URL` / `OLLAMA_MODEL` | localhost / llama3.2 | Local LLM mood provider |
| `OPENROUTER_API_KEY` / `OPENROUTER_MODEL` | — / free llama | Hosted free-tier LLM mood provider |

### Frontend (`frontend/.env`)

| Variable | Default | Purpose |
|---|---|---|
| `VITE_API_URL` | `http://localhost:8000` | Backend base URL (WebSocket URL is derived) |

## AI mood providers

All providers implement one interface (`backend/app/services/analysis/mood/base.py`) and are selected by `MOOD_PROVIDER`. Anything unavailable degrades to the built-in heuristic — the app never hard-fails on a missing model:

- **heuristic** (default): keyword + emoji analysis, zero dependencies, fully offline.
- **onnx**: the hackathon's YOLO11 facial-emotion checkpoint (`research/.../best.onnx`) via ONNX Runtime — `pip install -r requirements-ml.txt`.
- **ollama**: any local Ollama model (free, private).
- **openrouter**: free-tier hosted models (needs an API key).

Adding a paid provider later means one new class and one registry entry — no caller changes.

## Testing

```bash
cd backend
.venv/bin/python -m pytest tests -v     # 45 tests: engine math, analysis, API, realtime rooms
```

```bash
cd frontend
npx tsc --noEmit -p tsconfig.app.json   # strict type check
npm run build                            # production build
```

## Project structure

```
├── backend/
│   ├── app/
│   │   ├── api/            # routers: auth, movies, recommendations, analysis, rooms (REST+WS), social, library
│   │   ├── core/           # settings, JWT + password hashing
│   │   ├── db/             # engine, models, seed data
│   │   ├── schemas/        # Pydantic DTOs
│   │   └── services/
│   │       ├── recommendations/   # personal, group, history, weights, evolution, matrices
│   │       ├── analysis/          # time blocks, behavior, emoji, mood/ providers
│   │       └── rooms/             # state, permissions, realtime manager
│   └── tests/
├── frontend/
│   └── src/
│       ├── api/            # TanStack Query hooks
│       ├── lib/            # API client, RoomSocket
│       ├── contexts/       # AppContext (navigation + room session)
│       ├── components/     # screens + shadcn/ui
│       └── data/           # bundled catalog (offline fallback)
├── research/               # original hackathon prototypes (statements 1–3)
├── docs/                   # AUDIT, PRD, EXECUTION_PLAN, hackathon PDF
└── docker-compose.yml
```

## Deployment (free tiers)

Recommended zero-cost setup:

| Piece | Platform | Notes |
|---|---|---|
| Backend | **Render** (free web service) | Deploy `backend/` with the Dockerfile; supports WebSockets. Free instances sleep after idle — first request takes ~30 s to wake. |
| Database | **Neon** (free Postgres) | Set `DATABASE_URL`; SQLite works too but resets on redeploys of ephemeral disks. |
| Frontend | **Vercel** (free) | Root `frontend/`, build `npm run build`, output `dist/`, env `VITE_API_URL=https://<render-app>.onrender.com`. |

Steps: create the Neon database → deploy the backend on Render with `DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGINS=https://<vercel-app>.vercel.app` → deploy the frontend on Vercel with `VITE_API_URL`. Alternatives that also work: Railway or Fly.io for the backend, Cloudflare Pages for the frontend, Hugging Face Spaces (Docker) for an all-in-one demo.

**Limitations on free tiers**: single backend instance only (room state is in-memory — scale-out needs the documented Redis pub/sub path), cold starts on idle, and no custom-domain TLS on some platforms.

## Troubleshooting

- **Home rows say "built-in demo catalog"** — the backend isn't reachable; check it's running and `VITE_API_URL` matches.
- **Room join fails with `room_not_found`** — codes live in backend memory; restarting the backend clears active rooms.
- **CORS errors** — add your frontend origin to `CORS_ORIGINS` in `backend/.env`.
- **`onnx` provider unavailable** — install `requirements-ml.txt` and check `ONNX_MODEL_PATH`; the API falls back to the heuristic provider meanwhile (see `/health`).
- **Webcam prompt in watch party** — browser permission for the self-view tile; denying it only disables your preview.

## Future improvements

- Redis pub/sub room fan-out + Postgres room persistence for multi-instance deployments.
- TMDB catalog import behind the same movie schema.
- Voice-mood provider from the research notebooks behind the `MoodProvider` interface.
- WebRTC audio/video bridging in watch parties (self-view exists today).
- Playlist sharing with collaborator permissions (API groundwork in place).
