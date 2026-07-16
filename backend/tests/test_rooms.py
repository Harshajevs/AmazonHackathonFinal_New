"""Watch-party room lifecycle and realtime tests (PRD 8.5, section 13)."""


def _create(client, headers, **overrides):
    body = {"name": "Test Party", **overrides}
    r = client.post("/api/rooms", json=body, headers=headers)
    assert r.status_code == 201, r.text
    return r.json()


def _guest(client):
    token = client.post("/api/auth/guest").json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_join(client, guest_headers):
    room = _create(client, guest_headers)
    assert len(room["join_code"]) == 6
    assert room["role"] == "admin"

    joiner = _guest(client)
    joined = client.post(f"/api/rooms/{room['join_code']}/join", json={}, headers=joiner).json()
    assert joined["role"] == "member"
    assert len(joined["snapshot"]["members"]) == 2


def test_join_errors(client, guest_headers):
    assert client.post("/api/rooms/ZZZZZZ/join", json={}, headers=guest_headers).status_code == 404

    locked = _create(client, guest_headers, password="tv123")
    wrong = client.post(f"/api/rooms/{locked['join_code']}/join", json={"password": "nope"}, headers=_guest(client))
    assert wrong.status_code == 403
    right = client.post(f"/api/rooms/{locked['join_code']}/join", json={"password": "tv123"}, headers=_guest(client))
    assert right.status_code == 200

    tiny = _create(client, guest_headers, capacity=2)
    client.post(f"/api/rooms/{tiny['join_code']}/join", json={}, headers=_guest(client))
    full = client.post(f"/api/rooms/{tiny['join_code']}/join", json={}, headers=_guest(client))
    assert full.status_code == 409


def test_room_summary_hides_password(client, guest_headers):
    room = _create(client, guest_headers, password="secret")
    summary = client.get(f"/api/rooms/{room['join_code']}", headers=guest_headers).json()
    assert summary["has_password"] is True
    assert "password" not in str(summary).lower().replace("has_password", "")


def _recv_until(ws, event_type, limit=20):
    for _ in range(limit):
        event = ws.receive_json()
        if event["type"] == event_type:
            return event
    raise AssertionError(f"never received {event_type}")


def test_realtime_two_clients(client, guest_headers):
    """Two sockets in one room exchange chat, reactions, and queue updates."""
    room = _create(client, guest_headers)
    code, token_a = room["join_code"], room["membership_token"]
    joined = client.post(f"/api/rooms/{code}/join", json={}, headers=_guest(client)).json()
    token_b = joined["membership_token"]

    with client.websocket_connect(f"/ws/rooms/{code}?token={token_a}") as ws_a:
        snapshot = ws_a.receive_json()
        assert snapshot["type"] == "room.snapshot"
        with client.websocket_connect(f"/ws/rooms/{code}?token={token_b}") as ws_b:
            assert ws_b.receive_json()["type"] == "room.snapshot"
            _recv_until(ws_a, "member.joined")

            ws_a.send_json({"type": "chat.send", "payload": {"text": "hello room"}, "client_action_id": "c1"})
            msg = _recv_until(ws_b, "chat.message")
            assert msg["payload"]["text"] == "hello room"
            assert msg["sequence"] > 0 and msg["event_id"]

            ws_b.send_json({"type": "reaction.send", "payload": {"emoji": "🔥"}})
            assert _recv_until(ws_a, "reaction.created")["payload"]["emoji"] == "🔥"

            ws_b.send_json({"type": "queue.add", "payload": {"movie_id": 7, "title": "Top Gun", "image": "/images/image7.png"}})
            update = _recv_until(ws_a, "queue.updated")
            assert update["payload"]["queue"][0]["movie_id"] == 7
            assert update["payload"]["current_movie_id"] == 7


def test_permissions_enforced(client, guest_headers):
    """A plain member cannot run moderator/admin commands (FR-ROOM-07)."""
    room = _create(client, guest_headers)
    code = room["join_code"]
    member_token = client.post(f"/api/rooms/{code}/join", json={}, headers=_guest(client)).json()["membership_token"]

    with client.websocket_connect(f"/ws/rooms/{code}?token={member_token}") as ws:
        ws.receive_json()  # snapshot
        for command in ("queue.next", "poll.create", "room.setting.update", "member.promote", "room.end"):
            ws.send_json({"type": command, "payload": {}})
            event = _recv_until(ws, "error")
            assert event["payload"]["code"] == "forbidden", command


def test_poll_lifecycle(client, guest_headers):
    room = _create(client, guest_headers)
    code, admin_token = room["join_code"], room["membership_token"]

    with client.websocket_connect(f"/ws/rooms/{code}?token={admin_token}") as ws:
        ws.receive_json()
        ws.send_json({"type": "poll.create", "payload": {"question": "What next?", "options": ["RRR", "Wednesday"]}})
        poll = _recv_until(ws, "poll.created")
        poll_id = poll["payload"]["poll_id"]

        ws.send_json({"type": "poll.vote", "payload": {"poll_id": poll_id, "option": 0}})
        assert _recv_until(ws, "poll.updated")["payload"]["tally"] == [1, 0]
        # Revote replaces, not duplicates (FR-ROOM-06).
        ws.send_json({"type": "poll.vote", "payload": {"poll_id": poll_id, "option": 1}})
        assert _recv_until(ws, "poll.updated")["payload"]["tally"] == [0, 1]

        ws.send_json({"type": "poll.end", "payload": {"poll_id": poll_id}})
        ended = _recv_until(ws, "poll.ended")
        assert ended["payload"]["winner"] == "Wednesday"

        ws.send_json({"type": "poll.vote", "payload": {"poll_id": poll_id, "option": 0}})
        assert _recv_until(ws, "error")["payload"]["code"] == "poll_closed"


def test_ws_rejects_bad_token(client, guest_headers):
    import pytest
    from starlette.websockets import WebSocketDisconnect

    room = _create(client, guest_headers)
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect(f"/ws/rooms/{room['join_code']}?token=garbage") as ws:
            ws.receive_json()
