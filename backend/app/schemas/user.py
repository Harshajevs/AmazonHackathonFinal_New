from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.movie import MovieOut


class RegisterIn(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    email: str | None = None
    password: str = Field(min_length=8, max_length=128)


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str | None
    avatar: str
    is_guest: bool


class FriendOut(BaseModel):
    id: int
    username: str
    avatar: str
    status: str
    mutual_friends: int


class MovieSuggestionOut(BaseModel):
    id: int
    from_username: str
    from_avatar: str
    message: str
    movie: MovieOut
    created_at: datetime


class ListItemIn(BaseModel):
    movie_id: int
