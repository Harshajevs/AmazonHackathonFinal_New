import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_optional_user
from app.db.base import get_db
from app.db.models import Movie, User, WatchEvent
from app.schemas.movie import MovieOut
from app.schemas.recommendation import (
    FeedbackIn,
    FeedbackOut,
    GroupRecsIn,
    GroupRecsOut,
    GroupScoredMovieOut,
    PersonalRecsIn,
    PersonalRecsOut,
    ScoredMovieOut,
)
from app.services.analysis.time_blocks import current_block
from app.services.recommendations import group as group_engine
from app.services.recommendations import personal as personal_engine
from app.services.recommendations.history import blend_with_history
from app.services.recommendations.matrices import build_user_matrix
from app.services.recommendations.weights import default_weights, update_weights

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

# Bounded outcome → per-modality feedback (PRD 9.1: cap single-event influence).
_OUTCOME_FEEDBACK = {
    "select": [0.30, 0.30, 0.20, 0.20],
    "save": [0.25, 0.35, 0.20, 0.20],
    "complete": [0.35, 0.35, 0.15, 0.15],
    "dismiss": [0.25, 0.25, 0.25, 0.25],
}


def _recent_watches(db: Session, user: User | None, limit: int = 20) -> list[Movie]:
    if user is None:
        return []
    events = db.scalars(
        select(WatchEvent).where(WatchEvent.user_id == user.id).order_by(WatchEvent.occurred_at.desc()).limit(limit)
    ).all()
    return [e.movie for e in events]


@router.post("/personal", response_model=PersonalRecsOut)
def personal(
    body: PersonalRecsIn,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> PersonalRecsOut:
    time_block = body.time_block or current_block().key
    active_signals = ["time"]
    if body.behavior_cluster:
        active_signals.append("behavior")
    if body.voice_emotions:
        active_signals.append("voice")
    if body.facial_emotions:
        active_signals.append("facial")

    user_matrix = build_user_matrix(
        time_block=time_block,
        behavior_cluster=body.behavior_cluster,
        voice_emotions=body.voice_emotions,
        facial_emotions=body.facial_emotions,
    )

    history = _recent_watches(db, user) if body.use_history else []
    if history:
        user_matrix = blend_with_history(user_matrix, history)
        active_signals.append("history")

    weights = (user.modality_weights if user and user.modality_weights else default_weights())
    active_mask = [True, bool(body.behavior_cluster), bool(body.voice_emotions), bool(body.facial_emotions)]

    movies = db.scalars(select(Movie)).all()
    ranked = personal_engine.rank_movies(user_matrix, movies, weights=weights, limit=body.limit, active_modalities=active_mask)

    by_id = {m.id: m for m in movies}
    return PersonalRecsOut(
        request_id=str(uuid.uuid4()),
        active_signals=active_signals,
        used_history=bool(history),
        used_fallback=len(active_signals) == 1,
        weights=list(weights),
        results=[
            ScoredMovieOut(
                movie=MovieOut.model_validate(by_id[s.movie_id]),
                score=s.score,
                modality_scores=s.modality_scores,
                explanation=s.explanation,
            )
            for s in ranked
        ],
    )


@router.post("/group", response_model=GroupRecsOut)
def group(body: GroupRecsIn, db: Session = Depends(get_db)) -> GroupRecsOut:
    member_emotions = [m.emotions for m in body.members] or [None]
    movies = db.scalars(select(Movie)).all()
    ranked = group_engine.rank_for_group(member_emotions, movies, limit=body.limit)
    by_id = {m.id: m for m in movies}
    return GroupRecsOut(
        request_id=str(uuid.uuid4()),
        member_count=max(len(body.members), 1),
        results=[
            GroupScoredMovieOut(
                movie=MovieOut.model_validate(by_id[s.movie_id]),
                score=s.score,
                std_dev=s.std_dev,
                agreement=s.agreement,
                selectability=s.selectability,
                explanation=s.explanation,
            )
            for s in ranked
        ],
    )


@router.post("/feedback", response_model=FeedbackOut)
def feedback(
    body: FeedbackIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> FeedbackOut:
    signal = body.modality_feedback or _OUTCOME_FEEDBACK.get(body.outcome, _OUTCOME_FEEDBACK["dismiss"])
    updated = update_weights(user.modality_weights, signal)
    user.modality_weights = updated
    db.add(user)
    db.commit()
    return FeedbackOut(weights=updated, persisted=not user.is_guest)
