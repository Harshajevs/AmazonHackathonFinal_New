"""In-memory room manager: lifecycle, command handling, WS fan-out.

Single-node by design (PRD 10.2); the scale-out path is Redis pub/sub
behind this same interface.
"""

import asyncio
import logging
from datetime import datetime, timezone

from fastapi import WebSocket

from app.core.security import hash_password, verify_password
from app.services.rooms.permissions import PermissionDenied, check_command, check_kick
from app.services.rooms.state import (
    MAX_CHAT_HISTORY,
    MAX_CHAT_LENGTH,
    ROLE_ADMIN,
    ROLE_CO_ADMIN,
    ROLE_MEMBER,
    ROOM_ENDED,
    ROOM_OPEN,
    ChatMessage,
    Member,
    Poll,
    QueueItem,
    Room,
    new_id,
    new_join_code,
)

logger = logging.getLogger(__name__)

ALLOWED_REACTIONS = ["😂", "❤️", "😮", "👏", "🔥", "💯", "😍", "🤔"]


class RoomError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class RoomManager:
    def __init__(self) -> None:
        self._rooms: dict[str, Room] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._sockets: dict[str, dict[str, WebSocket]] = {}

    # ---------- lifecycle (REST) ----------

    def create_room(
        self,
        name: str,
        host_user_id: int | None,
        host_username: str,
        host_avatar: str = "🧑",
        password: str | None = None,
        capacity: int = 12,
        movie_id: int | None = None,
    ) -> tuple[Room, Member]:
        code = new_join_code()
        while code in self._rooms:
            code = new_join_code()
        room = Room(
            room_id=new_id(),
            join_code=code,
            name=name or "Movie Night Party",
            host_user_id=host_user_id,
            password_hash=hash_password(password) if password else None,
            capacity=max(2, min(capacity, 50)),
            current_movie_id=movie_id,
        )
        member = Member(member_id=new_id(), user_id=host_user_id, username=host_username, avatar=host_avatar, role=ROLE_ADMIN)
        room.members[member.member_id] = member
        self._rooms[code] = room
        self._locks[code] = asyncio.Lock()
        self._sockets[code] = {}
        logger.info("Room %s created by %s", code, host_username)
        return room, member

    def join_room(
        self,
        code: str,
        username: str,
        user_id: int | None,
        avatar: str = "🧑",
        password: str | None = None,
    ) -> tuple[Room, Member]:
        room = self.get_room(code)
        if room.state != ROOM_OPEN:
            raise RoomError("room_closed", "This room has ended")
        if room.password_hash and not (password and verify_password(password, room.password_hash)):
            raise RoomError("invalid_password", "Incorrect room password")
        if len(room.members) >= room.capacity:
            raise RoomError("room_full", "This room is full")
        member = Member(member_id=new_id(), user_id=user_id, username=username, avatar=avatar, role=ROLE_MEMBER)
        room.members[member.member_id] = member
        return room, member

    def get_room(self, code: str) -> Room:
        room = self._rooms.get(code.upper())
        if room is None:
            raise RoomError("room_not_found", "No room with that code")
        return room

    def lock(self, code: str) -> asyncio.Lock:
        return self._locks[code.upper()]

    # ---------- websocket registry ----------

    def attach(self, code: str, member_id: str, ws: WebSocket) -> None:
        self._sockets[code.upper()][member_id] = ws

    def detach(self, code: str, member_id: str) -> None:
        self._sockets.get(code.upper(), {}).pop(member_id, None)

    async def broadcast(self, room: Room, event: dict) -> None:
        dead = []
        for member_id, ws in list(self._sockets.get(room.join_code, {}).items()):
            try:
                await ws.send_json(event)
            except Exception:
                dead.append(member_id)
        for member_id in dead:
            self.detach(room.join_code, member_id)

    # ---------- events ----------

    def envelope(self, room: Room, event_type: str, payload: dict, actor: Member | None = None, client_action_id: str | None = None) -> dict:
        return {
            "type": event_type,
            "event_id": new_id(),
            "client_action_id": client_action_id,
            "room_id": room.room_id,
            "room_version": room.version,
            "sequence": room.next_sequence(),
            "actor_member_id": actor.member_id if actor else None,
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }

    # ---------- command dispatch ----------

    async def handle_command(self, room: Room, member: Member, message: dict) -> list[dict]:
        """Validate and apply one client command; return events to broadcast."""
        command = str(message.get("type", ""))
        payload = message.get("payload") or {}
        action_id = message.get("client_action_id")

        if command == "heartbeat.ping":
            return []  # pong handled by caller, not broadcast

        check_command(member, command)
        handler = getattr(self, "_cmd_" + command.replace(".", "_"), None)
        if handler is None:
            raise PermissionDenied("unknown_command", f"Unsupported command: {command}")
        return handler(room, member, payload, action_id)

    def _cmd_chat_send(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        if not room.chat_enabled:
            raise RoomError("chat_disabled", "Chat is disabled in this room")
        text = str(payload.get("text", "")).strip()[:MAX_CHAT_LENGTH]
        if not text:
            raise RoomError("empty_message", "Message cannot be empty")
        msg = ChatMessage(message_id=new_id(), member_id=member.member_id, username=member.username, text=text)
        room.chat_history.append(msg)
        del room.chat_history[:-MAX_CHAT_HISTORY]
        return [self.envelope(room, "chat.message", {"message_id": msg.message_id, "username": member.username, "avatar": member.avatar, "text": text, "at": msg.at}, member, action_id)]

    def _cmd_reaction_send(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        if not room.reactions_enabled:
            raise RoomError("reactions_disabled", "Reactions are disabled in this room")
        emoji = str(payload.get("emoji", ""))
        if emoji not in ALLOWED_REACTIONS:
            raise RoomError("invalid_reaction", "Unsupported reaction emoji")
        return [self.envelope(room, "reaction.created", {"emoji": emoji, "username": member.username}, member, action_id)]

    def _queue_updated(self, room: Room, member: Member, action_id) -> list[dict]:
        room.bump_version()
        return [self.envelope(room, "queue.updated", {"queue": room.snapshot()["queue"], "current_movie_id": room.current_movie_id}, member, action_id)]

    def _cmd_queue_add(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        movie_id = int(payload.get("movie_id", 0))
        if any(q.movie_id == movie_id for q in room.queue):
            raise RoomError("duplicate", "Movie already in queue")
        room.queue.append(
            QueueItem(item_id=new_id(), movie_id=movie_id, title=str(payload.get("title", "")), image=str(payload.get("image", "")), added_by=member.username)
        )
        if room.current_movie_id is None:
            room.current_movie_id = movie_id
        return self._queue_updated(room, member, action_id)

    def _cmd_queue_remove(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        item_id = payload.get("item_id")
        room.queue = [q for q in room.queue if q.item_id != item_id]
        return self._queue_updated(room, member, action_id)

    def _cmd_queue_reorder(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        order = payload.get("item_ids", [])
        by_id = {q.item_id: q for q in room.queue}
        reordered = [by_id[i] for i in order if i in by_id]
        reordered += [q for q in room.queue if q.item_id not in set(order)]
        room.queue = reordered
        return self._queue_updated(room, member, action_id)

    def _cmd_queue_next(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        if room.queue:
            room.queue.pop(0)
        room.current_movie_id = room.queue[0].movie_id if room.queue else None
        return self._queue_updated(room, member, action_id)

    def _cmd_poll_create(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        question = str(payload.get("question", "")).strip()
        options = [str(o).strip() for o in payload.get("options", []) if str(o).strip()]
        if not question or len(options) < 2:
            raise RoomError("invalid_poll", "A poll needs a question and at least two options")
        poll = Poll(poll_id=new_id(), question=question, options=options)
        room.polls[poll.poll_id] = poll
        room.bump_version()
        return [self.envelope(room, "poll.created", {"poll_id": poll.poll_id, "question": question, "options": options, "tally": poll.tally(), "state": poll.state}, member, action_id)]

    def _cmd_poll_vote(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        poll = room.polls.get(str(payload.get("poll_id")))
        if poll is None:
            raise RoomError("poll_not_found", "Poll does not exist")
        if poll.state != "open":
            raise RoomError("poll_closed", "This poll has ended")
        option = int(payload.get("option", -1))
        if not (0 <= option < len(poll.options)):
            raise RoomError("invalid_option", "Invalid poll option")
        poll.votes[member.member_id] = option  # one active vote per member
        return [self.envelope(room, "poll.updated", {"poll_id": poll.poll_id, "tally": poll.tally(), "state": poll.state}, member, action_id)]

    def _cmd_poll_end(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        poll = room.polls.get(str(payload.get("poll_id")))
        if poll is None:
            raise RoomError("poll_not_found", "Poll does not exist")
        poll.state = "closed"
        tally = poll.tally()
        winner = poll.options[tally.index(max(tally))] if any(tally) else None
        return [self.envelope(room, "poll.ended", {"poll_id": poll.poll_id, "tally": tally, "winner": winner}, member, action_id)]

    def _find_member(self, room: Room, payload: dict) -> Member:
        target = room.members.get(str(payload.get("member_id")))
        if target is None:
            raise RoomError("member_not_found", "Member not in room")
        return target

    def _cmd_member_promote(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        target = self._find_member(room, payload)
        if target.role == ROLE_ADMIN:
            raise RoomError("invalid_target", "Admin role cannot be changed")
        target.role = ROLE_CO_ADMIN
        room.bump_version()
        return [self.envelope(room, "member.role_updated", {"member_id": target.member_id, "username": target.username, "role": target.role}, member, action_id)]

    def _cmd_member_demote(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        target = self._find_member(room, payload)
        if target.role == ROLE_ADMIN:
            raise RoomError("invalid_target", "Admin role cannot be changed")
        target.role = ROLE_MEMBER
        room.bump_version()
        return [self.envelope(room, "member.role_updated", {"member_id": target.member_id, "username": target.username, "role": target.role}, member, action_id)]

    def _cmd_member_kick(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        target = self._find_member(room, payload)
        check_kick(member, target)
        room.members.pop(target.member_id, None)
        room.bump_version()
        return [self.envelope(room, "member.kicked", {"member_id": target.member_id, "username": target.username}, member, action_id)]

    def _cmd_room_setting_update(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        changed = {}
        if "chat_enabled" in payload:
            room.chat_enabled = bool(payload["chat_enabled"])
            changed["chat_enabled"] = room.chat_enabled
        if "reactions_enabled" in payload:
            room.reactions_enabled = bool(payload["reactions_enabled"])
            changed["reactions_enabled"] = room.reactions_enabled
        if not changed:
            raise RoomError("invalid_setting", "No supported setting in payload")
        room.bump_version()
        return [self.envelope(room, "room.setting_updated", changed, member, action_id)]

    def _cmd_presence_update(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        for attr in ("video_on", "audio_on", "hand_raised"):
            if attr in payload:
                setattr(member, attr, bool(payload[attr]))
        return [
            self.envelope(
                room,
                "member.updated",
                {"member_id": member.member_id, "username": member.username, "video_on": member.video_on, "audio_on": member.audio_on, "hand_raised": member.hand_raised},
                member,
                action_id,
            )
        ]

    def _cmd_room_leave(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        return self.remove_member(room, member, reason="left")

    def _cmd_room_end(self, room: Room, member: Member, payload: dict, action_id) -> list[dict]:
        room.state = ROOM_ENDED
        room.bump_version()
        return [self.envelope(room, "room.ended", {"ended_by": member.username}, member, action_id)]

    # ---------- membership transitions ----------

    def remove_member(self, room: Room, member: Member, reason: str = "left") -> list[dict]:
        room.members.pop(member.member_id, None)
        events = [self.envelope(room, "member.left", {"member_id": member.member_id, "username": member.username, "reason": reason})]
        if not room.members:
            room.state = ROOM_ENDED
            events.append(self.envelope(room, "room.expired", {}))
            # Keep the record briefly for late fetches; drop the socket registry.
            self._sockets.pop(room.join_code, None)
            self._rooms.pop(room.join_code, None)
            self._locks.pop(room.join_code, None)
        elif member.role == ROLE_ADMIN:
            # Transfer ownership to the longest-standing remaining member.
            successor = next(iter(room.members.values()))
            successor.role = ROLE_ADMIN
            events.append(self.envelope(room, "member.role_updated", {"member_id": successor.member_id, "username": successor.username, "role": ROLE_ADMIN}))
        return events


manager = RoomManager()
