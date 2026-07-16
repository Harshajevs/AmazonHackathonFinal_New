"""History-aware preprocessing.

Port of research/statement-1/Personalised_AI_Recommendations/
preprocessing_with_history.py:

    w_i            = alpha * exp(-beta * i)   (i = 0 is most recent), normalized
    history(6x4)   = sum(w_i * movie_matrix_i)
    processed(4x6) = 0.8 * live_user_matrix + 0.2 * history.T
"""

import numpy as np

from app.services.recommendations.matrices import movie_compatibility_matrix

ALPHA = 1.0
BETA = 0.5
LIVE_WEIGHT = 0.8
HISTORY_WEIGHT = 0.2


def decay_weights(n: int, alpha: float = ALPHA, beta: float = BETA) -> np.ndarray:
    if n == 0:
        return np.array([])
    w = alpha * np.exp(-beta * np.arange(n))
    return w / w.sum()


def history_matrix(movies: list) -> np.ndarray | None:
    """Aggregate watch history (most recent first) into a 6x4 matrix."""
    if not movies:
        return None
    weights = decay_weights(len(movies))
    agg = np.zeros((6, 4))
    for w, m in zip(weights, movies):
        agg += w * movie_compatibility_matrix(m.id, m.title, list(m.genres), m.rating)
    return agg


def blend_with_history(user_matrix: np.ndarray, movies: list) -> np.ndarray:
    hist = history_matrix(movies)
    if hist is None:
        return user_matrix
    return LIVE_WEIGHT * user_matrix + HISTORY_WEIGHT * hist.T
