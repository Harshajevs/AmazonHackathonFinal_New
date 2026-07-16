import logging

import jwt as pyjwt
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, decode_access_token
from app.db.base import get_db
from app.db.models import Movie, User
from app.schemas.room import RoomCreateIn, RoomJoinIn, RoomMembershipOut, RoomSummaryOut
from app.services.rooms.manager import RoomError, manager
from app.services.rooms.permissions import PermissionDenied
from app.services.rooms.state import ROOM_ENDED

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/rooms", tags=["rooms"])
ws_router = APIRouter(tags=["rooms-ws"])

_ROOM_ERROR_STATUS = {
    "room_not_found": 404,
    "invalid_password": 403,
    "room_full": 409,
    "room_closed": 410,
}


def _membership_token(code: str, member_id: str) -> str:
    return create_access_token(member_id, extra={"kind": "room", "room": code})


def _membership_out(room, member) -> RoomMembershipOut:
    return RoomMembershipOut(
        join_code=room.join_code,
        room_id=room.room_id,
        member_id=member.member_id,
        role=member.role,
        membership_token=_membership_token(room.join_code, member.member_id),
        snapshot=room.snapshot(),
    )


@router.post("", response_model=RoomMembershipOut, status_code=201)
def create_room(
    body: RoomCreateIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> RoomMembershipOut:
    room, member = manager.create_room(
        name=body.name,
        host_user_id=user.id,
        host_username=user.username,
        host_avatar=user.avatar,
        password=body.password,
        capacity=body.capacity,
        movie_id=body.movie_id,
    )
    if body.movie_id is not None:
        movie = db.get(Movie, body.movie_id)
        if movie:
            manager._cmd_queue_add(room, member, {"movie_id": movie.id, "title": movie.title, "image": movie.image}, None)
    return _membership_out(room, member)


@router.post("/{code}/join", response_model=RoomMembershipOut)
async def join_room(code: str, body: RoomJoinIn, user: User = Depends(get_current_user)) -> RoomMembershipOut:
    try:
        room, member = manager.join_room(code.upper(), username=user.username, user_id=user.id, avatar=user.avatar, password=body.password)
    except RoomError as exc:
        raise HTTPException(status_code=_ROOM_ERROR_STATUS.get(exc.code, 400), detail={"code": exc.code, "message": exc.message})
    await manager.broadcast(
        room,
        manager.envelope(room, "member.joined", {"member_id": member.member_id, "username": member.username, "avatar": member.avatar, "role": member.role}, member),
    )
    return _membership_out(room, member)


@router.get("/{code}", response_model=RoomSummaryOut)
def room_summary(code: str, user: User = Depends(get_current_user)) -> RoomSummaryOut:
    try:
        room = manager.get_room(code.upper())
    except RoomError as exc:
        raise HTTPException(status_code=404, detail={"code": exc.code, "message": exc.message})
    return RoomSummaryOut(
        join_code=room.join_code,
        name=room.name,
        state=room.state,
        member_count=len(room.members),
        capacity=room.capacity,
        has_password=room.password_hash is not None,
        current_movie_id=room.current_movie_id,
    )


@router.post("/{code}/leave", status_code=204)
async def leave_room(code: str, member_id: str, user: User = Depends(get_current_user)) -> None:
    try:
        room = manager.get_room(code.upper())
    except RoomError:
        return
    member = room.members.get(member_id)
    if member is None:
        return
    events = manager.remove_member(room, member, reason="left")
    for event in events:
        await manager.broadcast(room, event)


@ws_router.websocket("/ws/rooms/{code}")
async def room_socket(websocket: WebSocket, code: str, token: str) -> None:
    code = code.upper()
    try:
        payload = decode_access_token(token)
        if payload.get("kind") != "room" or payload.get("room") != code:
            raise pyjwt.PyJWTError("wrong token kind")
        member_id = payload["sub"]
        room = manager.get_room(code)
        member = room.members[member_id]
    except (pyjwt.PyJWTError, RoomError, KeyError):
        await websocket.close(code=4401, reason="invalid membership token")
        return

    await websocket.accept()
    manager.attach(code, member_id, websocket)
    member.presence = "online"
    await websocket.send_json(manager.envelope(room, "room.snapshot", room.snapshot(), member))
    await manager.broadcast(room, manager.envelope(room, "member.joined", {"member_id": member.member_id, "username": member.username, "avatar": member.avatar, "role": member.role, "presence": "online"}, member))

    try:
        while True:
            message = await websocket.receive_json()
            if message.get("type") == "heartbeat.ping":
                await websocket.send_json({"type": "heartbeat.pong"})
                continue
            try:
                async with manager.lock(code):
                    events = await manager.handle_command(room, member, message)
            except (RoomError, PermissionDenied) as exc:
                await websocket.send_json(
                    {"type": "error", "payload": {"code": exc.code, "message": str(exc)}, "client_action_id": message.get("client_action_id")}
                )
                continue
            for event in events:
                await manager.broadcast(room, event)
            if room.state == ROOM_ENDED:
                break
    except WebSocketDisconnect:
        manager.detach(code, member_id)
        if member_id in room.members:
            member.presence = "offline"
            await manager.broadcast(room, manager.envelope(room, "member.updated", {"member_id": member_id, "username": member.username, "presence": "offline"}, member))
    except KeyError:
        manager.detach(code, member_id)
    finally:
        manager.detach(code, member_id)
