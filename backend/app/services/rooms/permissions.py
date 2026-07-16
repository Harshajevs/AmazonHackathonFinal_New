"""Server-authoritative permission checks (PRD section 13).

The permission table from the prototype's room simulator, enforced on
every command — crafted client events cannot bypass role checks.
"""

from app.services.rooms.state import ROLE_ADMIN, ROLE_CO_ADMIN, Member

# Commands any member may issue (subject to room/global toggles).
_MEMBER_COMMANDS = {
    "chat.send",
    "reaction.send",
    "queue.add",
    "poll.vote",
    "presence.update",
    "room.leave",
    "heartbeat.ping",
    "connection.resume",
}

# Commands requiring co-admin or admin.
_MODERATOR_COMMANDS = {
    "queue.remove",
    "queue.reorder",
    "queue.next",
    "poll.create",
    "poll.end",
    "member.kick",
    "room.setting.update",
}

# Admin-only commands.
_ADMIN_COMMANDS = {"member.promote", "member.demote", "room.end"}


class PermissionDenied(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


def check_command(member: Member, command: str) -> None:
    if command in _MEMBER_COMMANDS:
        return
    if command in _MODERATOR_COMMANDS:
        if member.role in (ROLE_ADMIN, ROLE_CO_ADMIN):
            return
        raise PermissionDenied("forbidden", "This action requires co-admin or admin role")
    if command in _ADMIN_COMMANDS:
        if member.role == ROLE_ADMIN:
            return
        raise PermissionDenied("forbidden", "This action requires the admin role")
    raise PermissionDenied("unknown_command", f"Unsupported command: {command}")


def check_kick(actor: Member, target: Member) -> None:
    """Admin can kick anyone; co-admin only plain members."""
    if actor.role == ROLE_ADMIN and target.member_id != actor.member_id:
        return
    if actor.role == ROLE_CO_ADMIN and target.role not in (ROLE_ADMIN, ROLE_CO_ADMIN):
        return
    raise PermissionDenied("forbidden", "You cannot remove this member")
