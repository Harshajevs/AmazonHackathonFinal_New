from pydantic import BaseModel, Field


class RoomCreateIn(BaseModel):
    name: str = Field(default="Movie Night Party", max_length=100)
    password: str | None = Field(default=None, max_length=100)
    capacity: int = Field(default=12, ge=2, le=50)
    movie_id: int | None = None


class RoomJoinIn(BaseModel):
    password: str | None = None


class RoomMembershipOut(BaseModel):
    join_code: str
    room_id: str
    member_id: str
    role: str
    membership_token: str
    snapshot: dict


class RoomSummaryOut(BaseModel):
    join_code: str
    name: str
    state: str
    member_count: int
    capacity: int
    has_password: bool
    current_movie_id: int | None
