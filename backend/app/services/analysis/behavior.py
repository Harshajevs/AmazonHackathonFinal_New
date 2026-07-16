"""Behavioral clustering from playback interaction events.

Port of research/statement-1/Time_Mood_Behaviour_analysis/
Behaviour_Detection/Behaviour_classifier.py — the exact rule thresholds
are preserved.
"""

from collections import Counter
from dataclasses import dataclass

VALID_EVENTS = {"play", "pause", "skip_forward", "skip_backward", "rewind", "content_switch", "subtitle_toggle"}


@dataclass
class BehaviorResult:
    cluster: str
    rates: dict[str, float]
    event_count: int


def classify(events: list[str]) -> BehaviorResult:
    n = len(events)
    counts = Counter(e for e in events if e in VALID_EVENTS)

    def rate(*names: str) -> float:
        return sum(counts[name] for name in names) / n if n else 0.0

    subtitle_rate = rate("subtitle_toggle")
    switch_rate = rate("content_switch")
    skip_rate = rate("skip_forward", "skip_backward")
    rewind_rate = rate("rewind")

    if subtitle_rate > 0.4:
        cluster = "accessibility_user"
    elif switch_rate > 0.6:
        cluster = "content_switcher"
    elif skip_rate > 0.5 and n < 15:
        cluster = "quick_browser"
    elif rewind_rate > 0.25 and n > 20:
        cluster = "high_engagement"
    elif n > 30 and switch_rate < 0.2:
        cluster = "binge_watcher"
    else:
        cluster = "social_viewer"

    rates = {
        "subtitle_rate": round(subtitle_rate, 4),
        "switch_rate": round(switch_rate, 4),
        "skip_rate": round(skip_rate, 4),
        "rewind_rate": round(rewind_rate, 4),
    }
    return BehaviorResult(cluster=cluster, rates=rates, event_count=n)
