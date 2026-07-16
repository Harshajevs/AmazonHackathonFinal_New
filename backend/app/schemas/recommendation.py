from pydantic import BaseModel, Field

from app.schemas.movie import MovieOut

ENGINE_VERSION = "1.0.0"


class PersonalRecsIn(BaseModel):
    time_block: str | None = None
    behavior_cluster: str | None = None
    voice_emotions: dict[str, float] | None = None
    facial_emotions: dict[str, float] | None = None
    use_history: bool = True
    limit: int = Field(default=10, ge=1, le=45)


class ScoredMovieOut(BaseModel):
    movie: MovieOut
    score: float
    modality_scores: dict[str, float]
    explanation: str


class PersonalRecsOut(BaseModel):
    engine_version: str = ENGINE_VERSION
    request_id: str
    active_signals: list[str]
    used_history: bool
    used_fallback: bool
    weights: list[float]
    results: list[ScoredMovieOut]


class GroupMemberIn(BaseModel):
    username: str = "member"
    emotions: dict[str, float] | None = None


class GroupRecsIn(BaseModel):
    members: list[GroupMemberIn] = Field(default_factory=list)
    room_code: str | None = None
    limit: int = Field(default=10, ge=1, le=45)


class GroupScoredMovieOut(BaseModel):
    movie: MovieOut
    score: float
    std_dev: float
    agreement: float
    selectability: float
    explanation: str


class GroupRecsOut(BaseModel):
    engine_version: str = ENGINE_VERSION
    request_id: str
    member_count: int
    results: list[GroupScoredMovieOut]


class FeedbackIn(BaseModel):
    request_id: str | None = None
    movie_id: int | None = None
    outcome: str = "select"  # select | save | dismiss | complete | rating
    # Per-modality feedback [time, behavior, voice, facial]; optional —
    # derived from outcome when omitted.
    modality_feedback: list[float] | None = Field(default=None, min_length=4, max_length=4)


class FeedbackOut(BaseModel):
    weights: list[float]
    persisted: bool
