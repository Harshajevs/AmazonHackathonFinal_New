"""Personal recommendation engine.

Port of research/statement-1/Personalised_AI_Recommendations/
Personalised_recommendations.py:

    result = user(4x6) @ movie(6x4)            -> 4x4
    diagonal_scores = diag(result)             -> one score per modality
    raw_consensus  = diagonal_scores . weights
    final          = 0.8 * raw_consensus + 0.2 * popularity
"""

from dataclasses import dataclass

import numpy as np

from app.services.recommendations.matrices import (
    MODALITIES,
    MODALITY_WEIGHTS,
    movie_compatibility_matrix,
)

CONSENSUS_WEIGHT = 0.8
POPULARITY_WEIGHT = 0.2


@dataclass
class ScoredMovie:
    movie_id: int
    score: float
    modality_scores: dict[str, float]
    explanation: str


def score_movie(
    user_matrix: np.ndarray,
    movie_id: int,
    title: str,
    genres: list[str],
    rating: float,
    weights: np.ndarray | None = None,
    active_modalities: list[bool] | None = None,
) -> ScoredMovie:
    w = (MODALITY_WEIGHTS if weights is None else np.asarray(weights)).copy()
    # PRD FR-REC-04: absent optional signals drop out of the consensus and
    # the remaining weights renormalize; absence is not a zero-valued mood.
    if active_modalities is not None:
        mask = np.asarray(active_modalities, dtype=float)
        if mask.sum() > 0:
            w = w * mask
    w = w / w.sum()
    movie_matrix = movie_compatibility_matrix(movie_id, title, genres, rating)
    result = user_matrix @ movie_matrix
    diagonal = np.diag(result)
    raw_consensus = float(diagonal @ w)
    popularity = min(rating / 10.0, 1.0)
    final = CONSENSUS_WEIGHT * raw_consensus + POPULARITY_WEIGHT * popularity

    modality_scores = {m: round(float(s), 4) for m, s in zip(MODALITIES, diagonal)}
    strongest = MODALITIES[int(np.argmax(diagonal * w))]
    explanation = f"Strong {strongest} match" + (f" for {', '.join(genres[:2])} content" if genres else "")
    return ScoredMovie(movie_id=movie_id, score=round(final, 4), modality_scores=modality_scores, explanation=explanation)


def rank_movies(
    user_matrix: np.ndarray,
    movies: list,
    weights: np.ndarray | None = None,
    limit: int = 10,
    active_modalities: list[bool] | None = None,
) -> list[ScoredMovie]:
    by_id = {m.id: m for m in movies}
    scored = [
        score_movie(user_matrix, m.id, m.title, list(m.genres), m.rating, weights, active_modalities)
        for m in movies
    ]
    # PRD 9.3 tie-breaking: score, then popularity, then movie id.
    scored.sort(key=lambda s: (-s.score, -by_id[s.movie_id].rating, s.movie_id))
    return scored[:limit]
