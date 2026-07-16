from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text)
    genres: Mapped[list] = mapped_column(JSON)
    duration: Mapped[str] = mapped_column(String(20))
    rating: Mapped[float] = mapped_column(Float)
    year: Mapped[int] = mapped_column(Integer, index=True)
    image: Mapped[str] = mapped_column(String(200))
    platform: Mapped[str] = mapped_column(String(50), index=True)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(200), unique=True, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(200), nullable=True)
    avatar: Mapped[str] = mapped_column(String(10), default="🧑")
    is_guest: Mapped[bool] = mapped_column(Boolean, default=False)
    # Adaptive modality weights [time, behavior, voice, facial]; learned from feedback.
    modality_weights: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    lists: Mapped[list["UserMovie"]] = relationship(back_populates="user")


class UserMovie(Base):
    """A movie in one of a user's lists: history | wishlist | watch_later."""

    __tablename__ = "user_movies"
    __table_args__ = (UniqueConstraint("user_id", "movie_id", "kind"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    kind: Mapped[str] = mapped_column(String(20), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    user: Mapped[User] = relationship(back_populates="lists")
    movie: Mapped[Movie] = relationship()


class Friendship(Base):
    """Directed friendship edge; status: accepted | pending | suggested."""

    __tablename__ = "friendships"
    __table_args__ = (UniqueConstraint("user_id", "friend_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(20), default="accepted")
    mutual_friends: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    friend: Mapped[User] = relationship(foreign_keys=[friend_id])


class WatchEvent(Base):
    """Watch activity with bounded progress (PRD FR-LIB-02)."""

    __tablename__ = "watch_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    event_type: Mapped[str] = mapped_column(String(20), default="progress")  # start | progress | complete
    progress_pct: Mapped[float] = mapped_column(Float, default=0.0)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    movie: Mapped[Movie] = relationship()


class Playlist(Base):
    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    items: Mapped[list["PlaylistItem"]] = relationship(back_populates="playlist", cascade="all, delete-orphan", order_by="PlaylistItem.position")


class PlaylistItem(Base):
    __tablename__ = "playlist_items"
    __table_args__ = (UniqueConstraint("playlist_id", "movie_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    playlist_id: Mapped[int] = mapped_column(ForeignKey("playlists.id"), index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    position: Mapped[int] = mapped_column(Integer, default=0)

    playlist: Mapped[Playlist] = relationship(back_populates="items")
    movie: Mapped[Movie] = relationship()


class MovieSuggestion(Base):
    """A movie one user suggested to another, with a message."""

    __tablename__ = "movie_suggestions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    from_user: Mapped[User] = relationship(foreign_keys=[from_user_id])
    movie: Mapped[Movie] = relationship()
