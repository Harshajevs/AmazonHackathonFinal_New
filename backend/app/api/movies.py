from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db.models import Movie
from app.schemas.movie import CategoryOut, MovieOut

router = APIRouter(prefix="/api/movies", tags=["movies"])

# Curated home rows, matching the prototype's movieCategories.
_GENRE_ROWS = [
    ("action", "Action-Packed Adventures", "Action"),
    ("comedy", "Laugh Out Loud", "Comedy"),
    ("drama", "Emotional Dramas", "Drama"),
    ("crime", "Gripping Crime Thrillers", "Crime"),
    ("fantasy", "Fantasy Escapes", "Fantasy"),
    ("scifi", "Sci-Fi Journeys", "Sci-Fi"),
]
_PLATFORM_ROWS = [
    ("netflix", "Netflix Originals", "Netflix"),
    ("prime", "Prime Video Highlights", "Prime Video"),
    ("hotstar", "Hotstar Specials", "Hotstar"),
    ("aha", "Aha Originals", "Aha"),
]


@router.get("", response_model=list[MovieOut])
def list_movies(
    search: str | None = None,
    genre: str | None = None,
    platform: str | None = None,
    year: int | None = None,
    min_rating: float | None = Query(default=None, ge=0, le=10),
    featured: bool | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[MovieOut]:
    query = select(Movie).order_by(Movie.id)
    if search:
        query = query.where(Movie.title.ilike(f"%{search}%"))
    if platform:
        query = query.where(Movie.platform == platform)
    if year:
        query = query.where(Movie.year == year)
    if min_rating is not None:
        query = query.where(Movie.rating >= min_rating)
    if featured is not None:
        query = query.where(Movie.featured == featured)
    movies = db.scalars(query.offset(offset).limit(limit)).all()
    if genre:
        movies = [m for m in movies if genre in m.genres]
    return [MovieOut.model_validate(m) for m in movies]


@router.get("/categories", response_model=list[CategoryOut])
def categories(db: Session = Depends(get_db)) -> list[CategoryOut]:
    movies = db.scalars(select(Movie).order_by(Movie.id)).all()
    out: list[CategoryOut] = []

    trending = [m for m in movies if m.year >= 2022][:15]
    out.append(CategoryOut(key="trending", title="Currently Trending", movies=[MovieOut.model_validate(m) for m in trending]))

    for key, title, genre in _GENRE_ROWS:
        row = [m for m in movies if genre in m.genres][:15]
        if row:
            out.append(CategoryOut(key=key, title=title, movies=[MovieOut.model_validate(m) for m in row]))

    for key, title, platform in _PLATFORM_ROWS:
        row = [m for m in movies if m.platform == platform][:15]
        if row:
            out.append(CategoryOut(key=key, title=title, movies=[MovieOut.model_validate(m) for m in row]))
    return out


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)) -> MovieOut:
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail={"code": "movie_not_found", "message": "Movie not found"})
    return MovieOut.model_validate(movie)


@router.get("/{movie_id}/related", response_model=list[MovieOut])
def related(movie_id: int, db: Session = Depends(get_db)) -> list[MovieOut]:
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail={"code": "movie_not_found", "message": "Movie not found"})
    movies = db.scalars(select(Movie).where(Movie.id != movie_id)).all()
    genres = set(movie.genres)
    scored = sorted(movies, key=lambda m: (-len(genres & set(m.genres)), -m.rating))
    return [MovieOut.model_validate(m) for m in scored[:10]]
