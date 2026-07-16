from pydantic import BaseModel, Field


class TimeBlockOut(BaseModel):
    key: str
    label: str
    vibe: str
    content_types: list[str]
    score: float
    hour: int


class BehaviorIn(BaseModel):
    events: list[str] = Field(min_length=1)


class BehaviorOut(BaseModel):
    cluster: str
    rates: dict[str, float]
    event_count: int


class EmojiIn(BaseModel):
    emojis: list[str] = Field(min_length=1)


class EmojiOut(BaseModel):
    dominant_emotion: str
    dominant_emoji: str
    confidence: float
    usage_probability: float
    emotion_scores: dict[str, float]


class MoodIn(BaseModel):
    text: str | None = None
    emojis: list[str] = Field(default_factory=list)
    image_base64: str | None = None
    provider: str | None = None


class MoodOut(BaseModel):
    dominant_emotion: str
    emotions: dict[str, float]
    provider: str
    confidence: float
