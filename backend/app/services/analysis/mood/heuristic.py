"""Zero-dependency mood provider: keyword and emoji heuristics.

Default provider — keeps the whole system runnable offline with no
model downloads, mirroring the sentiment heuristics used across the
prototype's chat/reaction analysis.
"""

import numpy as np

from app.services.analysis.emoji import analyze as analyze_emojis
from app.services.analysis.mood.base import MoodInput, MoodProvider, MoodResult
from app.services.recommendations.matrices import EMOTIONS

_KEYWORDS: dict[str, list[str]] = {
    "angry": ["angry", "furious", "annoyed", "hate", "rage", "mad", "irritated", "frustrated"],
    "disgust": ["disgusting", "gross", "awful", "terrible", "worst", "cringe", "yuck"],
    "fear": ["scared", "afraid", "terrified", "anxious", "nervous", "creepy", "horror", "worried"],
    "happy": ["happy", "great", "awesome", "love", "amazing", "excited", "fun", "laugh", "best", "enjoy", "chill"],
    "neutral": ["okay", "fine", "alright", "whatever", "normal", "meh"],
    "sad": ["sad", "depressed", "lonely", "cry", "miss", "tired", "down", "upset", "heartbroken"],
}


class HeuristicMoodProvider(MoodProvider):
    name = "heuristic"

    def analyze(self, payload: MoodInput) -> MoodResult:
        scores = np.full(6, 0.5)

        if payload.text:
            text = payload.text.lower()
            hits = np.array(
                [sum(word in text for word in _KEYWORDS[emotion]) for emotion in EMOTIONS],
                dtype=float,
            )
            if hits.sum() > 0:
                scores = scores + 2.0 * hits

        if payload.emojis:
            emoji_result = analyze_emojis(payload.emojis)
            emoji_scores = np.array([emoji_result.emotion_scores[e] for e in EMOTIONS])
            if emoji_scores.sum() > 0:
                scores = scores + 4.0 * emoji_scores

        distribution = scores / scores.sum()
        dominant_idx = int(np.argmax(distribution))
        spread = float(distribution.max() - np.sort(distribution)[-2])
        return MoodResult(
            dominant_emotion=EMOTIONS[dominant_idx],
            emotions={e: round(float(s), 4) for e, s in zip(EMOTIONS, distribution)},
            provider=self.name,
            confidence=round(min(0.5 + spread * 2, 1.0), 4),
        )
