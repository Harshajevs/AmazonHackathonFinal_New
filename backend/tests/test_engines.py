"""Unit tests for the ported recommendation math (PRD section 9)."""

import numpy as np
import pytest

from app.services.recommendations.group import aggregate_group, member_matrix, rank_for_group
from app.services.recommendations.history import blend_with_history, decay_weights
from app.services.recommendations.matrices import (
    GROUP_MODALITY_WEIGHTS,
    MODALITY_WEIGHTS,
    build_user_matrix,
    movie_compatibility_matrix,
)
from app.services.recommendations.personal import rank_movies, score_movie
from app.services.recommendations.weights import update_weights


class FakeMovie:
    def __init__(self, id, title, genres, rating):
        self.id, self.title, self.genres, self.rating = id, title, genres, rating


MOVIES = [
    FakeMovie(1, "Explosions", ["Action", "Thriller"], 8.0),
    FakeMovie(2, "Giggles", ["Comedy", "Family"], 7.5),
    FakeMovie(3, "Shadows", ["Horror", "Mystery"], 6.5),
]


def test_canonical_weights():
    assert MODALITY_WEIGHTS.tolist() == [0.30, 0.25, 0.25, 0.20]
    assert GROUP_MODALITY_WEIGHTS.tolist() == [0.15, 0.15, 0.25, 0.20, 0.15, 0.10]
    assert MODALITY_WEIGHTS.sum() == pytest.approx(1.0)
    assert GROUP_MODALITY_WEIGHTS.sum() == pytest.approx(1.0)


def test_movie_matrix_deterministic_and_bounded():
    a = movie_compatibility_matrix(1, "Explosions", ["Action"], 8.0)
    b = movie_compatibility_matrix(1, "Explosions", ["Action"], 8.0)
    assert np.array_equal(a, b)
    assert a.shape == (6, 4)
    assert a.min() >= 0.0 and a.max() <= 1.0


def test_user_matrix_rows_are_distributions():
    matrix = build_user_matrix(time_block="evening", behavior_cluster="binge_watcher", facial_emotions={"happy": 0.9, "neutral": 0.1})
    assert matrix.shape == (4, 6)
    np.testing.assert_allclose(matrix.sum(axis=1), np.ones(4))


def test_personal_scoring_formula():
    """final = 0.8 * (diag(U @ M) . w) + 0.2 * rating/10, reproduced by hand."""
    user = build_user_matrix(time_block="evening")
    movie = MOVIES[0]
    matrix = movie_compatibility_matrix(movie.id, movie.title, movie.genres, movie.rating)
    diag = np.diag(user @ matrix)
    expected = 0.8 * float(diag @ MODALITY_WEIGHTS) + 0.2 * movie.rating / 10
    result = score_movie(user, movie.id, movie.title, movie.genres, movie.rating)
    assert result.score == pytest.approx(expected, abs=1e-3)


def test_rank_is_stable():
    user = build_user_matrix(time_block="evening")
    first = rank_movies(user, MOVIES)
    second = rank_movies(user, MOVIES)
    assert [s.movie_id for s in first] == [s.movie_id for s in second]


def test_active_modality_renormalization():
    """FR-REC-04: dropping voice/facial must not tank scores via absence."""
    user = build_user_matrix(time_block="evening", facial_emotions={"happy": 1.0})
    full = score_movie(user, 2, "Giggles", ["Comedy"], 7.5, active_modalities=[True, True, True, True])
    time_only = score_movie(user, 2, "Giggles", ["Comedy"], 7.5, active_modalities=[True, False, False, False])
    assert 0 < time_only.score <= 1.2
    assert abs(full.score - time_only.score) < 0.5


def test_decay_weights_sum_to_one():
    w = decay_weights(20)
    assert w.sum() == pytest.approx(1.0)
    assert all(w[i] > w[i + 1] for i in range(19)), "most recent watch must weigh most"


def test_history_blend_shape_and_no_history_passthrough():
    user = build_user_matrix(time_block="morning")
    assert np.array_equal(blend_with_history(user, []), user)
    blended = blend_with_history(user, MOVIES)
    assert blended.shape == (4, 6)
    assert not np.array_equal(blended, user)


def test_weight_update_momentum():
    updated = update_weights(None, [1.0, 0.0, 0.0, 0.0])
    expected = 0.6 * np.array([0.30, 0.25, 0.25, 0.20]) + 0.4 * np.array([1.0, 0, 0, 0])
    np.testing.assert_allclose(updated, expected / expected.sum(), atol=1e-6)
    assert sum(updated) == pytest.approx(1.0)


def test_weight_update_rejects_bad_shape():
    with pytest.raises(ValueError):
        update_weights(None, [1.0, 0.0])


def test_group_aggregation_median_mean():
    happy = member_matrix({"happy": 1.0})
    sad = member_matrix({"sad": 1.0})
    agg = aggregate_group([happy, happy, sad])
    manual = 0.7 * np.median(np.stack([happy, happy, sad]), axis=0) + 0.3 * np.mean(np.stack([happy, happy, sad]), axis=0)
    np.testing.assert_allclose(agg, np.clip(manual, 0, 1))


def test_group_ranking_metrics():
    members = [{"happy": 1.0}, {"happy": 0.8, "neutral": 0.2}, {"sad": 1.0}]
    results = rank_for_group(members, MOVIES)
    assert len(results) == 3
    for r in results:
        assert 0.0 <= r.score <= 1.0
        assert 0.0 <= r.agreement <= 1.0
        assert 0.0 <= r.selectability <= 100.0
        assert r.std_dev >= 0.0


def test_group_prefers_comedy_for_happy_group():
    members = [{"happy": 1.0}] * 4
    results = rank_for_group(members, MOVIES)
    assert results[0].movie_id == 2, "an all-happy group should get the comedy first"
