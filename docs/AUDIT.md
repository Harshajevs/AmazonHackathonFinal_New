# Repository Audit — Enhanced Fire TV Experience

Audit date: July 2026. Scope: full repository as delivered at the end of Amazon HackOn Season 5 (May–June 2025).

## 1. What the repository is

A hackathon prototype for an AI-powered Fire TV experience with three problem statements:

- **Statement 1** — Personalized AI recommendations driven by time-of-day, behavior, voice mood, and facial mood.
- **Statement 2** — Social/shared viewing: watch-party rooms, group chat analysis, group recommendations, reactions.
- **Statement 3** — Cross-OTT social watching and evolving movie preference matrices.

The deliverables are a **UI showcase website** and a set of **independent Python simulations** proving out each algorithm. Frontend and backend were never integrated — every screen runs on hardcoded data, and every Python script runs standalone with synthetic inputs.

## 2. Existing architecture

```
AmazonHackathonFinal_New/
├── FireTV(UI)_Website/        # React 18 + Vite 5 + TypeScript + shadcn/ui + Tailwind
├── Statement-1/               # Personal recommendations + mood/behavior/time analysis
├── Statement-2/               # Group analysis, room simulator, group recommendations, VR filters
├── Statement-3/               # Movie matrix preprocessing/evolution
└── Amazon_Hackon_Season_5.pdf # Problem statement document (10.6 MB)
```

### 2.1 Frontend (`FireTV(UI)_Website`)

- **Stack**: React 18.3, Vite 5.4, TypeScript 5.5, Tailwind 3.4, shadcn/ui (40+ stock Radix components), React Router 6, TanStack Query 5 (installed, never used), generated with Lovable (lovable-tagger present).
- **Routing**: a single `/` route; actual navigation is a string-based page state machine inside a 30+ member `AppContext` (17 logical screens: home, detail, search, categories, my list, playlists, history, create-room, join-room, room, friends, settings, apps, games, subscriptions, dashboard, platform).
- **Data**: 45 movies hardcoded in `src/data/movieData.ts` across 4 platforms (Netflix, Prime Video, Hotstar, Aha), 15 curated rows, 12 genres. Friends, requests, suggestions, chat messages, and room members are all hardcoded arrays.
- **Watch party**: local-only. Webcam via `getUserMedia`, chat/queue/emoji reactions mutate context state; **no WebSocket, no fetch, zero network calls anywhere in the app**.
- **Auth**: none. Implicit "You" user.
- **Assets**: 74 images (~44 MB) live in `images/` at the project root — *not* `public/` — while code references `/images/*.png`; the dev server happens to serve them, production builds do not copy them.

### 2.2 Python prototypes

| Module | What it proves | Type |
|---|---|---|
| `Personalised_recommendations.py` | 4×6 user matrix × 6×4 movie matrix → diagonal → weighted consensus (time .30, behavior .25, voice .25, facial .20); final = 0.8·consensus + 0.2·popularity | stdout simulation |
| `preprocessing_with_history.py` (×2 copies) | Exponential-decay watch-history aggregation (α=1, β=0.5), blended 80/20 with live signals | stdout simulation |
| `dynamic_ratios.py` | Momentum weight adaptation from feedback: `w' = 0.6·w + 0.4·feedback`, normalized | stdout simulation |
| `updated_6X6_group_suggestions.py` | Group recs: 6 emotions × 6 modalities, 70% median + 30% mean aggregation, consensus = 0.6·raw + 0.2·popularity + 0.2·suitability | stdout simulation |
| `updated_changing_matrix.py` | Genre-aware movie matrix that evolves as users watch (`+count/20·0.5`, clipped [0,1]) | stdout simulation |
| `Behaviour_classifier.py` (×2 copies) | Rule-based clustering of MediaSession events into 6 behavior clusters + bootstrap voting | stdout simulation |
| `FireTVTimeDisplay.py` (×2 copies) | Timezone detection → 6 time blocks → per-block content vibes | stdout simulation |
| `emoji_emotion.py` | 12 emoji → 6-emotion vectors, dominant mood + confidence | stdout simulation |
| `Mood_Detection(YOLO)/app.py` (×2 copies + `best.onnx`) | YOLO11 facial emotion detection on webcam | OpenCV GUI app |
| `Voice_Mood_Detection/*.ipynb` | Voice mood classification (Colab) | notebooks |
| `Group_Chat_Analysis/BERT.ipynb` | Chat sentiment via BERT (Colab) | notebook |
| `Custom_Room_Simulator/` | Watch-party role model: admin/co-admin/user, kick/promote, playlists, queue, polls, chat/reaction toggles — implemented as a **file-based state machine** (`room_state.json` + append-only log) driven by CLI scripts | CLI scripts |
| `VR_Filters/*.ipynb` | Background swap / jersey mask filters | notebooks |

## 3. Dependencies

- **Frontend**: current for early 2025; no critical deprecations. Notable unused installs: TanStack Query, next-themes, recharts, zod. `lovable-tagger` is IDE tooling that should not ship.
- **Python**: numpy, pandas, matplotlib, opencv, ultralytics, transformers/librosa (notebooks). No requirements.txt anywhere; no pinned versions; no virtual env definition.

## 4. Third-party services & AI integrations

The pitch references AWS AppSync, Amazon Personalize, and Neo4j — **none are present in code**. All "AI" is local: an ONNX YOLO11 model checked into the repo (~10 MB), Colab notebooks for voice/BERT, and NumPy simulations. There are no API keys, no paid services, and no network integrations of any kind.

## 5. Database schema

None. No database, no ORM, no migrations. State lives in hardcoded TS arrays, hardcoded Python dicts, and `room_state.json`.

## 6. Authentication flow

None anywhere.

## 7. Build, deployment, CI/CD

- Frontend: `npm run dev` / `vite build` only. Production build is **broken in practice** because images are outside `public/`.
- Python: no entry point, no packaging, no tests.
- No Dockerfiles, no CI/CD, no deployment configuration, no environment management (zero `.env` handling).

## 8. Known risks & technical debt

1. **No integration layer** — the core gap. The UI and the algorithms cannot talk to each other.
2. **Four exact-duplicate Python modules** across Statement folders (behavior classifier, YOLO app, time display, history preprocessing).
3. **God context**: `AppContext` mixes navigation, catalog, social, room, and playlist state with imperative setters and no persistence.
4. **Broken production asset pipeline** (images at repo root).
5. **No tests of any kind**, front or back.
6. **No error/loading states** — everything is synchronous local state.
7. **Dead code**: ProfileMenu never rendered; React Query/next-themes/zod installed but unused; 29 unused images; `images.zip` (44 MB) committed alongside the extracted images.
8. **Room simulator race conditions**: concurrent CLI writers to a shared JSON file with no locking.
9. **Security**: room passwords collected and ignored; no input validation; webcam started without permission UX.
10. **10.6 MB PDF and 44 MB zip in git history** — repository bloat.

## 9. Performance bottlenecks

- 45-movie catalog re-filtered on every render with no memoization (tolerable at this size, wrong pattern at catalog scale).
- All 15 home rows render eagerly; no code splitting; single bundle.
- Python engines are O(n) NumPy over tiny hardcoded sets — fine, but they recompute random matrices per run (non-deterministic recommendations).

## 10. What is worth preserving

- The **UI design and screen inventory** — polished, complete, and demo-proven.
- The **algorithm designs**: the 4×6 multi-modal consensus, exponential-decay history, momentum weight adaptation, 6×6 group consensus, behavior clustering rules, time blocks, emoji-emotion vectors, and the room permission model are all coherent and portable as-is.
- The **role model** of the room simulator (admin/co-admin/user with global and per-user toggles) maps directly onto a real WebSocket room service.
