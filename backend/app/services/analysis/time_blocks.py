"""Time-of-day content blocks.

Port of research/statement-1/Time_Mood_Behaviour_analysis/Time_Detection/
FireTVTimeDisplay.py: six daily blocks, each with a content vibe and score.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TimeBlock:
    key: str
    label: str
    start_hour: int
    end_hour: int
    vibe: str
    content_types: list[str]
    score: float


TIME_BLOCKS = [
    TimeBlock("morning", "Morning Fresh", 6, 10, "Light and energizing starts", ["News", "Comedy", "Family", "Sports"], 0.62),
    TimeBlock("midday", "Midday Break", 10, 14, "Easy comfort viewing", ["Comedy", "Family", "Romance"], 0.55),
    TimeBlock("afternoon", "Afternoon Wind", 14, 18, "Family-friendly picks", ["Family", "Adventure", "Fantasy"], 0.58),
    TimeBlock("evening", "Evening Prime", 18, 22, "Peak drama and action hours", ["Action", "Drama", "Thriller"], 0.93),
    TimeBlock("prime", "Late Prime", 22, 24, "Gripping late-night thrillers", ["Thriller", "Crime", "Mystery"], 0.78),
    TimeBlock("latenight", "Night Owl", 0, 6, "Niche and intense picks", ["Horror", "Mystery", "Sci-Fi"], 0.30),
]


def current_block(now: datetime | None = None) -> TimeBlock:
    hour = (now or datetime.now()).hour
    for block in TIME_BLOCKS:
        if block.start_hour <= hour < block.end_hour:
            return block
    return TIME_BLOCKS[-1]
