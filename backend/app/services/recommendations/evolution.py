"""Movie matrix evolution.

Port of research/statement-3/Processing_Movie_Matrix/
updated_changing_matrix.py: a movie's preference matrix drifts toward the
observed audience distribution as watches accumulate.

    updated[attr, mod] = clip(initial[attr, mod] + (count / total) * 0.5, 0, 1)
"""

import numpy as np

from app.services.recommendations.matrices import (
    BEHAVIOR_CLUSTERS,
    EMOTIONS,
    MODALITIES,
    TIME_BLOCKS,
    movie_compatibility_matrix,
)

DRIFT_RATE = 0.5

_ATTRS_BY_MODALITY = {
    "time": TIME_BLOCKS,
    "behavior": BEHAVIOR_CLUSTERS,
    "voice": EMOTIONS,
    "facial": EMOTIONS,
}


def evolve_matrix(
    movie_id: int,
    title: str,
    genres: list[str],
    rating: float,
    watch_distribution: dict[str, dict[str, int]],
) -> dict:
    """Apply audience watch counts to a movie's genre-aware initial matrix.

    watch_distribution: {modality: {attribute: user_count}}
    Returns initial matrix, updated matrix, and the majority profile.
    """
    initial = movie_compatibility_matrix(movie_id, title, genres, rating)
    updated = initial.copy()
    total = sum(sum(counts.values()) for counts in watch_distribution.values()) or 1

    majority: dict[str, str] = {}
    for mod_idx, modality in enumerate(MODALITIES):
        attrs = _ATTRS_BY_MODALITY[modality]
        counts = watch_distribution.get(modality, {})
        for attr_idx, attr in enumerate(attrs):
            count = counts.get(attr, 0)
            if count:
                updated[attr_idx, mod_idx] += (count / total) * DRIFT_RATE
        if counts:
            majority[modality] = max(counts, key=counts.get)

    updated = np.clip(updated, 0.0, 1.0)
    return {
        "initial": np.round(initial, 4).tolist(),
        "updated": np.round(updated, 4).tolist(),
        "majority_profile": majority,
    }
