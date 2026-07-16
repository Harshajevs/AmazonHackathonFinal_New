"""Group (watch-party) recommendation engine.

Port of research/statement-2/Room_Recommendations/
updated_6X6_group_suggestions.py:

    group(6x6)  = 0.7 * median(member matrices) + 0.3 * mean(member matrices)
    match(6x6)  = normalize(group * movie_compat)   (element-wise)
    raw         = diag(match) . group_modality_weights
    consensus   = 0.6 * raw + 0.2 * popularity + 0.2 * suitability
"""

from dataclasses import dataclass

import numpy as np

from app.services.recommendations.matrices import (
    EMOTIONS,
    GROUP_MODALITIES,
    GROUP_MODALITY_WEIGHTS,
    group_compatibility_matrix,
)

RAW_WEIGHT = 0.6
POPULARITY_WEIGHT = 0.2
SUITABILITY_WEIGHT = 0.2
MEDIAN_SHARE = 0.7
MEAN_SHARE = 0.3

# Genres that work well (or poorly) for mixed-household group viewing.
GROUP_SUITABILITY: dict[str, float] = {
    "Family": 1.0, "Comedy": 0.95, "Adventure": 0.9, "Sports": 0.9, "Fantasy": 0.85,
    "Action": 0.8, "Sci-Fi": 0.75, "Romance": 0.65, "Drama": 0.6, "Mystery": 0.6,
    "Crime": 0.5, "Thriller": 0.45, "Horror": 0.3,
}


SELECTABILITY_THRESHOLD = 0.7


@dataclass
class GroupScoredMovie:
    movie_id: int
    score: float
    std_dev: float        # PRD 9.2: standard deviation of per-member scores
    agreement: float      # 1 - std_dev (higher = group agrees)
    selectability: float  # percentage of members scoring above threshold
    explanation: str


def member_matrix(emotions: dict[str, float] | None) -> np.ndarray:
    """6x6 member matrix (emotions x modalities) from an emotion distribution."""
    if not emotions:
        col = np.full(6, 1.0 / 6)
    else:
        col = np.array([max(emotions.get(e, 0.0), 0.0) for e in EMOTIONS])
        col = col / col.sum() if col.sum() > 0 else np.full(6, 1.0 / 6)
    return np.tile(col.reshape(6, 1), (1, len(GROUP_MODALITIES)))


def aggregate_group(matrices: list[np.ndarray]) -> np.ndarray:
    stack = np.stack(matrices)
    agg = MEDIAN_SHARE * np.median(stack, axis=0) + MEAN_SHARE * np.mean(stack, axis=0)
    return np.clip(agg, 0.0, 1.0)


def _movie_raw_score(matrix: np.ndarray, movie_id: int, title: str, genres: list[str]) -> float:
    compat = group_compatibility_matrix(movie_id, title, genres)
    match = matrix * compat
    peak = match.max()
    if peak > 0:
        match = match / peak
    return float(np.diag(match) @ GROUP_MODALITY_WEIGHTS / GROUP_MODALITY_WEIGHTS.sum())


def _suitability(genres: list[str]) -> float:
    vals = [GROUP_SUITABILITY[g] for g in genres if g in GROUP_SUITABILITY]
    return float(np.mean(vals)) if vals else 0.6


def rank_for_group(member_emotions: list[dict[str, float] | None], movies: list, limit: int = 10) -> list[GroupScoredMovie]:
    members = [member_matrix(e) for e in member_emotions] or [member_matrix(None)]
    group = aggregate_group(members)

    results = []
    for m in movies:
        genres = list(m.genres)
        raw = _movie_raw_score(group, m.id, m.title, genres)
        popularity = min(m.rating / 10.0, 1.0)
        suitability = _suitability(genres)
        score = RAW_WEIGHT * raw + POPULARITY_WEIGHT * popularity + SUITABILITY_WEIGHT * suitability

        # PRD FR-GRP-04: fairness metrics come from per-member candidate
        # scores, not the aggregate (prototype collapsed the variance).
        per_member = [_movie_raw_score(mm, m.id, m.title, genres) for mm in members]
        std_dev = float(np.std(per_member))
        selectability = float(np.mean([s > SELECTABILITY_THRESHOLD for s in per_member]) * 100)

        dominant = EMOTIONS[int(np.argmax(group.mean(axis=1)))]
        explanation = f"Fits the group's {dominant} mood; suitability {suitability:.0%}"
        results.append(
            GroupScoredMovie(
                movie_id=m.id,
                score=round(score, 4),
                std_dev=round(std_dev, 4),
                agreement=round(max(0.0, 1.0 - std_dev), 4),
                selectability=round(selectability, 2),
                explanation=explanation,
            )
        )
    # PRD 9.3 tie-breaking: score, then suitability, popularity, movie id.
    results.sort(key=lambda r: (-r.score, r.movie_id))
    return results[:limit]
