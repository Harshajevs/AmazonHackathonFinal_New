"""Emoji reaction → emotion mapping.

Port of research/statement-2/Analysis/Reactions_Analysis/emoji_emotion.py.
Each emoji carries a 6-dimensional emotion weight vector over
[angry, disgust, fear, happy, neutral, sad].
"""

from collections import Counter
from dataclasses import dataclass

import numpy as np

from app.services.recommendations.matrices import EMOTIONS

EMOJI_EMOTION_VECTORS: dict[str, list[int]] = {
    "😀": [1, 1, 1, 10, 3, 1],
    "😂": [1, 1, 1, 10, 2, 1],
    "❤️": [1, 1, 1, 9, 3, 2],
    "😍": [1, 1, 1, 10, 2, 1],
    "👏": [1, 1, 1, 8, 4, 1],
    "🔥": [3, 1, 1, 8, 3, 1],
    "💯": [1, 1, 1, 8, 4, 1],
    "😮": [2, 1, 5, 4, 5, 2],
    "🤔": [2, 2, 2, 3, 9, 2],
    "😢": [2, 1, 2, 1, 3, 10],
    "😡": [10, 4, 2, 1, 2, 3],
    "😱": [2, 2, 10, 2, 2, 3],
}


@dataclass
class EmojiAnalysis:
    dominant_emotion: str
    dominant_emoji: str
    confidence: float
    usage_probability: float
    emotion_scores: dict[str, float]


def analyze(emojis: list[str]) -> EmojiAnalysis:
    known = [e for e in emojis if e in EMOJI_EMOTION_VECTORS]
    if not known:
        return EmojiAnalysis(
            dominant_emotion="neutral",
            dominant_emoji="",
            confidence=0.0,
            usage_probability=0.0,
            emotion_scores={e: 0.0 for e in EMOTIONS},
        )

    counts = Counter(known)
    dominant_emoji, dominant_count = counts.most_common(1)[0]
    vector = np.array(EMOJI_EMOTION_VECTORS[dominant_emoji], dtype=float)
    dominant_emotion = EMOTIONS[int(np.argmax(vector))]

    # Confidence: mean of the top-2 emotion weights, as in the prototype.
    confidence = float(np.mean(np.sort(vector)[-2:]) * 10)
    # Laplace-smoothed usage probability of the dominant emoji.
    usage_probability = (dominant_count + 1) / (len(known) + len(counts)) * 100

    total = np.zeros(6)
    for emoji, count in counts.items():
        total += count * np.array(EMOJI_EMOTION_VECTORS[emoji], dtype=float)
    total = total / total.sum()

    return EmojiAnalysis(
        dominant_emotion=dominant_emotion,
        dominant_emoji=dominant_emoji,
        confidence=round(min(confidence, 100.0), 2),
        usage_probability=round(usage_probability, 2),
        emotion_scores={e: round(float(s), 4) for e, s in zip(EMOTIONS, total)},
    )
