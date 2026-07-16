"""Adaptive modality weights.

Port of research/statement-1/Personalised_AI_Recommendations/
dynamic_ratios.py: momentum update from feedback, renormalized.

    w' = normalize(0.6 * w + 0.4 * feedback)
"""

import numpy as np

from app.services.recommendations.matrices import MODALITY_WEIGHTS

MOMENTUM = 0.6
FEEDBACK_RATE = 0.4


def default_weights() -> list[float]:
    return MODALITY_WEIGHTS.tolist()


def update_weights(current: list[float] | None, feedback: list[float]) -> list[float]:
    w = np.asarray(current if current else MODALITY_WEIGHTS, dtype=float)
    f = np.clip(np.asarray(feedback, dtype=float), 0.0, None)
    if f.shape != (4,):
        raise ValueError("feedback must contain exactly 4 values (time, behavior, voice, facial)")
    if f.sum() > 0:
        f = f / f.sum()
    updated = MOMENTUM * w + FEEDBACK_RATE * f
    updated = updated / updated.sum()
    return [round(float(x), 6) for x in updated]
