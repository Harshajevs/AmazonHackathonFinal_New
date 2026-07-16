import json
import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.models import Friendship, Movie, MovieSuggestion, User

logger = logging.getLogger(__name__)

SEED_FILE = Path(__file__).parent / "seed_movies.json"

# The demo social graph shipped with the prototype UI, now persisted.
DEMO_FRIENDS = [
    ("Manasa", "👩🏻", "accepted", 12),
    ("Rohith", "👨🏻", "accepted", 8),
    ("Maruthi", "👨🏽", "accepted", 15),
    ("Harsha", "🧑🏻", "accepted", 6),
    ("Suhasini", "👩🏽", "accepted", 10),
    ("Varshith", "👦🏻", "pending", 4),
    ("Akash", "👨🏿", "pending", 7),
    ("Goutham", "🧔🏻", "suggested", 3),
    ("Viswateja", "👨🏻‍🦱", "suggested", 5),
    ("Prathvik", "👦🏽", "suggested", 2),
]

DEMO_SUGGESTIONS = [
    ("Rohith", 10, "This heist series is unreal, you have to watch it!"),
    ("Manasa", 2, "Perfect for a weekend binge — the finale is wild."),
    ("Harsha", 7, "Best action movie I've seen this year."),
]


def seed(db: Session) -> None:
    if db.scalar(select(Movie).limit(1)) is not None:
        return
    movies = json.loads(SEED_FILE.read_text())
    for m in movies:
        db.add(
            Movie(
                id=int(m["id"]),
                title=m["title"],
                description=m["description"],
                genres=m["genre"],
                duration=m["duration"],
                rating=float(m["rating"]),
                year=m["year"],
                image=m["image"],
                platform=m["platform"],
                featured=bool(m.get("featured", False)),
            )
        )

    demo = User(username="demo", email="demo@firetv.local", password_hash=hash_password("demo1234"), avatar="🧑🏻‍🦰")
    db.add(demo)
    db.flush()

    name_to_user: dict[str, User] = {}
    for name, avatar, _, _ in DEMO_FRIENDS:
        u = User(username=name, avatar=avatar, is_guest=False)
        db.add(u)
        name_to_user[name] = u
    db.flush()

    for name, _, status, mutual in DEMO_FRIENDS:
        db.add(Friendship(user_id=demo.id, friend_id=name_to_user[name].id, status=status, mutual_friends=mutual))
    for name, movie_id, message in DEMO_SUGGESTIONS:
        db.add(MovieSuggestion(from_user_id=name_to_user[name].id, to_user_id=demo.id, movie_id=movie_id, message=message))

    db.commit()
    logger.info("Seeded %d movies and demo social graph", len(movies))
