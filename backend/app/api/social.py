from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.base import get_db
from app.db.models import Friendship, MovieSuggestion, User
from app.schemas.movie import MovieOut
from app.schemas.user import FriendOut, MovieSuggestionOut

router = APIRouter(prefix="/api/friends", tags=["social"])


class FriendsOut(BaseModel):
    friends: list[FriendOut]
    requests: list[FriendOut]
    suggestions: list[FriendOut]
    movie_suggestions: list[MovieSuggestionOut]


class FriendRequestIn(BaseModel):
    friend_id: int
    action: str = "accept"  # accept | decline | remove


def _friend_out(f: Friendship) -> FriendOut:
    return FriendOut(
        id=f.friend.id,
        username=f.friend.username,
        avatar=f.friend.avatar,
        status=f.status,
        mutual_friends=f.mutual_friends,
    )


@router.get("", response_model=FriendsOut)
def friends(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> FriendsOut:
    edges = db.scalars(select(Friendship).where(Friendship.user_id == user.id)).all()
    suggestions = db.scalars(
        select(MovieSuggestion).where(MovieSuggestion.to_user_id == user.id).order_by(MovieSuggestion.created_at.desc())
    ).all()
    return FriendsOut(
        friends=[_friend_out(f) for f in edges if f.status == "accepted"],
        requests=[_friend_out(f) for f in edges if f.status == "pending"],
        suggestions=[_friend_out(f) for f in edges if f.status == "suggested"],
        movie_suggestions=[
            MovieSuggestionOut(
                id=s.id,
                from_username=s.from_user.username,
                from_avatar=s.from_user.avatar,
                message=s.message,
                movie=MovieOut.model_validate(s.movie),
                created_at=s.created_at,
            )
            for s in suggestions
        ],
    )


@router.post("/requests", response_model=FriendOut)
def resolve_request(body: FriendRequestIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> FriendOut:
    edge = db.scalar(select(Friendship).where(Friendship.user_id == user.id, Friendship.friend_id == body.friend_id))
    if edge is None:
        friend = db.get(User, body.friend_id)
        if friend is None:
            raise HTTPException(status_code=404, detail={"code": "user_not_found", "message": "User not found"})
        edge = Friendship(user_id=user.id, friend_id=body.friend_id, status="pending")
        db.add(edge)
    elif body.action == "accept":
        edge.status = "accepted"
    elif body.action in ("decline", "remove"):
        db.delete(edge)
        db.commit()
        return FriendOut(id=body.friend_id, username=edge.friend.username, avatar=edge.friend.avatar, status="removed", mutual_friends=0)
    db.commit()
    return _friend_out(edge)
