"""Watch-party room domain state.

Ports the role/permission model from
research/statement-2/Custom_Room_Simulator (admin / co-admin / member,
global chat+reaction toggles, playlists/queue, polls) from a file-based
CLI state machine into in-memory domain objects managed by RoomManager.
"""

import secrets
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

ROLE_ADMIN = "admin"
ROLE_CO_ADMIN = "co_admin"
ROLE_MEMBER = "member"

ROOM_OPEN = "open"
ROOM_ENDED = "ended"

MAX_CHAT_LENGTH = 500
MAX_CHAT_HISTORY = 200


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return str(uuid.uuid4())


def new_join_code() -> str:
    return secrets.token_hex(3).upper()  # 6-char code, e.g. "A3F9C1"


@dataclass
class Member:
    member_id: str
    user_id: int | None
    username: str
    avatar: str = "🧑"
    role: str = ROLE_MEMBER
    presence: str = "online"
    video_on: bool = True
    audio_on: bool = True
    hand_raised: bool = False


@dataclass
class QueueItem:
    item_id: str
    movie_id: int
    title: str
    image: str
    added_by: str


@dataclass
class Poll:
    poll_id: str
    question: str
    options: list[str]
    votes: dict[str, int] = field(default_factory=dict)  # member_id -> option index
    state: str = "open"

    def tally(self) -> list[int]:
        counts = [0] * len(self.options)
        for option_index in self.votes.values():
            if 0 <= option_index < len(self.options):
                counts[option_index] += 1
        return counts


@dataclass
class ChatMessage:
    message_id: str
    member_id: str
    username: str
    text: str
    at: str = field(default_factory=_now)


@dataclass
class Room:
    room_id: str
    join_code: str
    name: str
    host_user_id: int | None
    password_hash: str | None = None
    capacity: int = 12
    state: str = ROOM_OPEN
    version: int = 0
    sequence: int = 0
    chat_enabled: bool = True
    reactions_enabled: bool = True
    current_movie_id: int | None = None
    members: dict[str, Member] = field(default_factory=dict)
    queue: list[QueueItem] = field(default_factory=list)
    polls: dict[str, Poll] = field(default_factory=dict)
    chat_history: list[ChatMessage] = field(default_factory=list)
    created_at: str = field(default_factory=_now)

    def next_sequence(self) -> int:
        self.sequence += 1
        return self.sequence

    def bump_version(self) -> int:
        self.version += 1
        return self.version

    @property
    def admin(self) -> Member | None:
        return next((m for m in self.members.values() if m.role == ROLE_ADMIN), None)

    def snapshot(self) -> dict:
        return {
            "room_id": self.room_id,
            "join_code": self.join_code,
            "name": self.name,
            "state": self.state,
            "version": self.version,
            "sequence": self.sequence,
            "chat_enabled": self.chat_enabled,
            "reactions_enabled": self.reactions_enabled,
            "current_movie_id": self.current_movie_id,
            "capacity": self.capacity,
            "has_password": self.password_hash is not None,
            "members": [
                {
                    "member_id": m.member_id,
                    "username": m.username,
                    "avatar": m.avatar,
                    "role": m.role,
                    "presence": m.presence,
                    "video_on": m.video_on,
                    "audio_on": m.audio_on,
                    "hand_raised": m.hand_raised,
                }
                for m in self.members.values()
            ],
            "queue": [
                {"item_id": q.item_id, "movie_id": q.movie_id, "title": q.title, "image": q.image, "added_by": q.added_by}
                for q in self.queue
            ],
            "polls": [
                {"poll_id": p.poll_id, "question": p.question, "options": p.options, "tally": p.tally(), "state": p.state}
                for p in self.polls.values()
            ],
            "chat_history": [
                {"message_id": c.message_id, "member_id": c.member_id, "username": c.username, "text": c.text, "at": c.at}
                for c in self.chat_history[-50:]
            ],
        }
