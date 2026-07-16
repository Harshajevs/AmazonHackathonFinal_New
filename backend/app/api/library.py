from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.base import get_db
from app.db.models import Movie, Playlist, PlaylistItem, User, UserMovie, WatchEvent
from app.schemas.movie import MovieOut

router = APIRouter(tags=["library"])

LIST_KINDS = {"wishlist", "watch_later"}


class LibraryItemIn(BaseModel):
    movie_id: int
    kind: str = "wishlist"


class LibraryItemOut(BaseModel):
    kind: str
    movie: MovieOut


class HistoryIn(BaseModel):
    movie_id: int
    event_type: str = "progress"  # start | progress | complete
    progress_pct: float = Field(default=0.0, ge=0.0, le=100.0)


class HistoryOut(BaseModel):
    movie: MovieOut
    event_type: str
    progress_pct: float


class PlaylistIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class PlaylistItemIn(BaseModel):
    movie_id: int


class PlaylistOut(BaseModel):
    id: int
    name: str
    movies: list[MovieOut]


def _movie_or_404(db: Session, movie_id: int) -> Movie:
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail={"code": "movie_not_found", "message": "Movie not found"})
    return movie


# ---------- My List / Watch Later ----------

@router.get("/api/library/items", response_model=list[LibraryItemOut])
def list_items(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[LibraryItemOut]:
    items = db.scalars(select(UserMovie).where(UserMovie.user_id == user.id, UserMovie.kind.in_(LIST_KINDS))).all()
    return [LibraryItemOut(kind=i.kind, movie=MovieOut.model_validate(i.movie)) for i in items]


@router.post("/api/library/items", response_model=LibraryItemOut, status_code=201)
def add_item(body: LibraryItemIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> LibraryItemOut:
    if body.kind not in LIST_KINDS:
        raise HTTPException(status_code=422, detail={"code": "invalid_kind", "message": f"kind must be one of {sorted(LIST_KINDS)}"})
    movie = _movie_or_404(db, body.movie_id)
    existing = db.scalar(
        select(UserMovie).where(UserMovie.user_id == user.id, UserMovie.movie_id == body.movie_id, UserMovie.kind == body.kind)
    )
    if existing is None:  # idempotent add (PRD FR-LIB-01)
        db.add(UserMovie(user_id=user.id, movie_id=body.movie_id, kind=body.kind))
        db.commit()
    return LibraryItemOut(kind=body.kind, movie=MovieOut.model_validate(movie))


@router.delete("/api/library/items", status_code=204)
def remove_item(movie_id: int = Query(...), kind: str = Query(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> None:
    item = db.scalar(select(UserMovie).where(UserMovie.user_id == user.id, UserMovie.movie_id == movie_id, UserMovie.kind == kind))
    if item:
        db.delete(item)
        db.commit()


# ---------- Watch history ----------

@router.get("/api/history", response_model=list[HistoryOut])
def get_history(limit: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[HistoryOut]:
    events = db.scalars(
        select(WatchEvent).where(WatchEvent.user_id == user.id).order_by(WatchEvent.occurred_at.desc()).limit(limit)
    ).all()
    return [HistoryOut(movie=MovieOut.model_validate(e.movie), event_type=e.event_type, progress_pct=e.progress_pct) for e in events]


@router.post("/api/history", response_model=HistoryOut, status_code=201)
def record_history(body: HistoryIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> HistoryOut:
    movie = _movie_or_404(db, body.movie_id)
    event = WatchEvent(user_id=user.id, movie_id=body.movie_id, event_type=body.event_type, progress_pct=body.progress_pct)
    db.add(event)
    db.commit()
    return HistoryOut(movie=MovieOut.model_validate(movie), event_type=event.event_type, progress_pct=event.progress_pct)


# ---------- Playlists ----------

def _playlist_out(p: Playlist) -> PlaylistOut:
    return PlaylistOut(id=p.id, name=p.name, movies=[MovieOut.model_validate(i.movie) for i in p.items])


def _own_playlist(playlist_id: int, db: Session, user: User) -> Playlist:
    playlist = db.get(Playlist, playlist_id)
    if playlist is None or playlist.owner_id != user.id:
        raise HTTPException(status_code=404, detail={"code": "playlist_not_found", "message": "Playlist not found"})
    return playlist


@router.get("/api/playlists", response_model=list[PlaylistOut])
def list_playlists(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[PlaylistOut]:
    playlists = db.scalars(select(Playlist).where(Playlist.owner_id == user.id)).all()
    return [_playlist_out(p) for p in playlists]


@router.post("/api/playlists", response_model=PlaylistOut, status_code=201)
def create_playlist(body: PlaylistIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> PlaylistOut:
    playlist = Playlist(owner_id=user.id, name=body.name)
    db.add(playlist)
    db.commit()
    return _playlist_out(playlist)


@router.post("/api/playlists/{playlist_id}/items", response_model=PlaylistOut, status_code=201)
def add_playlist_item(playlist_id: int, body: PlaylistItemIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> PlaylistOut:
    playlist = _own_playlist(playlist_id, db, user)
    _movie_or_404(db, body.movie_id)
    if not any(i.movie_id == body.movie_id for i in playlist.items):
        db.add(PlaylistItem(playlist_id=playlist.id, movie_id=body.movie_id, position=len(playlist.items)))
        db.commit()
        db.refresh(playlist)
    return _playlist_out(playlist)


@router.delete("/api/playlists/{playlist_id}/items/{movie_id}", response_model=PlaylistOut)
def remove_playlist_item(playlist_id: int, movie_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> PlaylistOut:
    playlist = _own_playlist(playlist_id, db, user)
    for item in list(playlist.items):
        if item.movie_id == movie_id:
            db.delete(item)
    db.commit()
    db.refresh(playlist)
    return _playlist_out(playlist)


@router.delete("/api/playlists/{playlist_id}", status_code=204)
def delete_playlist(playlist_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> None:
    playlist = _own_playlist(playlist_id, db, user)
    db.delete(playlist)
    db.commit()
