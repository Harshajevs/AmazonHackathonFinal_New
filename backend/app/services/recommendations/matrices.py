"""Deterministic preference/compatibility matrices.

Ports the matrix construction from the hackathon prototypes
(research/statement-1/Personalised_AI_Recommendations and
research/statement-2/Room_Recommendations), replacing per-run random
matrices with deterministic, genre-derived ones so recommendations are
stable across requests.

Conventions (from the prototype):
- Personal engine: user matrix is 4x6 (modalities x attributes),
  movie matrix is 6x4 (attributes x modalities).
- Group engine: 6x6 (emotions x modalities).
"""

import zlib

import numpy as np

MODALITIES = ["time", "behavior", "voice", "facial"]
# Prototype weights: time .30, behavior .25, voice .25, facial .20
MODALITY_WEIGHTS = np.array([0.30, 0.25, 0.25, 0.20])

TIME_BLOCKS = ["morning", "midday", "afternoon", "evening", "prime", "latenight"]
BEHAVIOR_CLUSTERS = [
    "high_engagement",
    "quick_browser",
    "binge_watcher",
    "accessibility_user",
    "content_switcher",
    "social_viewer",
]
EMOTIONS = ["angry", "disgust", "fear", "happy", "neutral", "sad"]

# PRD 9.2: modalities time, behavior, facial, voice, emoji, text with
# canonical initial weights [0.15, 0.15, 0.25, 0.20, 0.15, 0.10].
GROUP_MODALITIES = ["time", "behavior", "facial", "voice", "emoji", "text"]
GROUP_MODALITY_WEIGHTS = np.array([0.15, 0.15, 0.25, 0.20, 0.15, 0.10])

# How strongly each genre resonates with each emotion signal [angry, disgust, fear, happy, neutral, sad]
GENRE_EMOTION_AFFINITY: dict[str, list[float]] = {
    "Action": [0.85, 0.30, 0.55, 0.80, 0.50, 0.30],
    "Adventure": [0.50, 0.25, 0.45, 0.90, 0.55, 0.30],
    "Comedy": [0.25, 0.20, 0.15, 0.95, 0.60, 0.55],
    "Crime": [0.80, 0.60, 0.70, 0.40, 0.55, 0.45],
    "Drama": [0.45, 0.35, 0.40, 0.60, 0.70, 0.85],
    "Family": [0.15, 0.10, 0.10, 0.95, 0.65, 0.40],
    "Fantasy": [0.35, 0.20, 0.45, 0.85, 0.55, 0.35],
    "Horror": [0.60, 0.70, 0.95, 0.25, 0.35, 0.40],
    "Mystery": [0.55, 0.45, 0.75, 0.45, 0.60, 0.45],
    "Romance": [0.20, 0.15, 0.15, 0.90, 0.55, 0.70],
    "Sci-Fi": [0.50, 0.30, 0.60, 0.75, 0.60, 0.35],
    "Sports": [0.60, 0.15, 0.30, 0.90, 0.55, 0.25],
    "Thriller": [0.75, 0.50, 0.85, 0.40, 0.45, 0.40],
}

# How well each genre fits each time block [morning, midday, afternoon, evening, prime, latenight]
GENRE_TIME_AFFINITY: dict[str, list[float]] = {
    "Action": [0.35, 0.45, 0.55, 0.85, 0.90, 0.60],
    "Adventure": [0.50, 0.60, 0.70, 0.80, 0.75, 0.45],
    "Comedy": [0.70, 0.75, 0.70, 0.75, 0.70, 0.55],
    "Crime": [0.25, 0.35, 0.45, 0.75, 0.90, 0.80],
    "Drama": [0.45, 0.55, 0.60, 0.85, 0.80, 0.55],
    "Family": [0.80, 0.85, 0.90, 0.70, 0.50, 0.20],
    "Fantasy": [0.50, 0.60, 0.70, 0.80, 0.75, 0.50],
    "Horror": [0.10, 0.15, 0.25, 0.55, 0.80, 0.95],
    "Mystery": [0.30, 0.40, 0.50, 0.75, 0.85, 0.75],
    "Romance": [0.55, 0.60, 0.60, 0.85, 0.75, 0.50],
    "Sci-Fi": [0.40, 0.50, 0.60, 0.80, 0.85, 0.65],
    "Sports": [0.75, 0.80, 0.85, 0.85, 0.75, 0.35],
    "Thriller": [0.20, 0.30, 0.45, 0.75, 0.90, 0.85],
}

_DEFAULT_EMOTION = [0.45] * 6
_DEFAULT_TIME = [0.55] * 6


def _seed_for(movie_id: int, title: str) -> int:
    return zlib.crc32(f"{movie_id}:{title}".encode())


def _genre_mean(genres: list[str], table: dict[str, list[float]], default: list[float]) -> np.ndarray:
    rows = [table[g] for g in genres if g in table]
    if not rows:
        return np.array(default)
    return np.mean(rows, axis=0)


def movie_compatibility_matrix(movie_id: int, title: str, genres: list[str], rating: float) -> np.ndarray:
    """6x4 movie matrix (attributes x [time, behavior, voice, facial]).

    Each column is scored against that modality's own six attributes
    (time blocks, behavior clusters, emotions), derived from genre
    affinities plus small deterministic per-movie variation.
    """
    rng = np.random.default_rng(_seed_for(movie_id, title))
    emotion = _genre_mean(genres, GENRE_EMOTION_AFFINITY, _DEFAULT_EMOTION)
    time_fit = _genre_mean(genres, GENRE_TIME_AFFINITY, _DEFAULT_TIME)

    quality = min(rating / 10.0, 1.0)
    # Behavior clusters respond mostly to quality/genre breadth: bingeable,
    # engaging content scores high for high_engagement and binge_watcher.
    behavior = np.array(
        [
            0.4 + 0.5 * quality,          # high_engagement
            0.7 - 0.3 * quality,          # quick_browser
            0.35 + 0.55 * quality,        # binge_watcher
            0.5,                          # accessibility_user
            0.6 - 0.2 * quality,          # content_switcher
            0.45 + 0.2 * len(genres) / 3, # social_viewer
        ]
    )

    matrix = np.column_stack([time_fit, behavior, emotion, emotion])
    matrix = matrix + rng.uniform(-0.08, 0.08, size=matrix.shape)
    return np.clip(matrix, 0.0, 1.0)


def group_compatibility_matrix(movie_id: int, title: str, genres: list[str]) -> np.ndarray:
    """6x6 movie matrix (emotions x group modalities) for the group engine."""
    rng = np.random.default_rng(_seed_for(movie_id, title) ^ 0x6A09E667)
    emotion = _genre_mean(genres, GENRE_EMOTION_AFFINITY, _DEFAULT_EMOTION)
    matrix = np.tile(emotion.reshape(6, 1), (1, 6))
    matrix = matrix + rng.uniform(-0.10, 0.10, size=matrix.shape)
    return np.clip(matrix, 0.0, 1.0)


def build_user_matrix(
    time_block: str | None = None,
    behavior_cluster: str | None = None,
    voice_emotions: dict[str, float] | None = None,
    facial_emotions: dict[str, float] | None = None,
) -> np.ndarray:
    """4x6 user preference matrix from live context signals.

    Missing signals fall back to a uniform distribution, matching the
    prototype's neutral handling.
    """

    def one_hot(labels: list[str], value: str | None) -> np.ndarray:
        row = np.full(6, 1.0 / 6)
        if value in labels:
            row = np.full(6, 0.08)
            row[labels.index(value)] = 0.6
        return row / row.sum()

    def distribution(labels: list[str], values: dict[str, float] | None) -> np.ndarray:
        if not values:
            return np.full(6, 1.0 / 6)
        row = np.array([max(values.get(label, 0.0), 0.0) for label in labels])
        total = row.sum()
        return row / total if total > 0 else np.full(6, 1.0 / 6)

    return np.vstack(
        [
            one_hot(TIME_BLOCKS, time_block),
            one_hot(BEHAVIOR_CLUSTERS, behavior_cluster),
            distribution(EMOTIONS, voice_emotions),
            distribution(EMOTIONS, facial_emotions),
        ]
    )
