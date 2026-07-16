"""API integration tests: auth, catalog, recommendations, social, library."""


def test_health(client):
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["mood_provider"] == "heuristic"


def test_movies_seeded(client):
    movies = client.get("/api/movies", params={"limit": 100}).json()
    assert len(movies) == 45
    assert movies[0]["title"] == "Avatar: The Way of Water"


def test_movie_filters(client):
    netflix = client.get("/api/movies", params={"platform": "Netflix", "limit": 100}).json()
    assert netflix and all(m["platform"] == "Netflix" for m in netflix)
    search = client.get("/api/movies", params={"search": "stranger"}).json()
    assert any("Stranger" in m["title"] for m in search)


def test_movie_detail_and_404(client):
    assert client.get("/api/movies/1").json()["id"] == 1
    assert client.get("/api/movies/9999").status_code == 404


def test_related_excludes_self(client):
    related = client.get("/api/movies/1/related").json()
    assert related and all(m["id"] != 1 for m in related)


def test_categories_no_duplicates_in_row(client):
    rows = client.get("/api/movies/categories").json()
    assert rows
    for row in rows:
        ids = [m["id"] for m in row["movies"]]
        assert len(ids) == len(set(ids))


def test_register_login_me(client):
    r = client.post("/api/auth/register", json={"username": "newuser", "password": "supersecret1"})
    assert r.status_code == 201
    dup = client.post("/api/auth/register", json={"username": "newuser", "password": "supersecret1"})
    assert dup.status_code == 409
    login = client.post("/api/auth/login", json={"username": "newuser", "password": "supersecret1"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    me = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"}).json()
    assert me["username"] == "newuser" and me["is_guest"] is False


def test_login_generic_error(client):
    bad = client.post("/api/auth/login", json={"username": "newuser", "password": "wrong"})
    assert bad.status_code == 401
    missing = client.post("/api/auth/login", json={"username": "ghost", "password": "wrong"})
    assert missing.status_code == 401
    assert bad.json() == missing.json(), "error must not reveal which field failed"


def test_guest_flow(client, guest_headers):
    me = client.get("/api/users/me", headers=guest_headers).json()
    assert me["is_guest"] is True


def test_me_requires_auth(client):
    assert client.get("/api/users/me").status_code == 401


def test_personal_recommendations(client, guest_headers):
    body = {"behavior_cluster": "binge_watcher", "facial_emotions": {"happy": 0.8, "neutral": 0.2}, "limit": 5}
    r = client.post("/api/recommendations/personal", json=body, headers=guest_headers).json()
    assert len(r["results"]) == 5
    assert set(r["active_signals"]) >= {"time", "behavior", "facial"}
    assert r["engine_version"] and r["request_id"]
    scores = [item["score"] for item in r["results"]]
    assert scores == sorted(scores, reverse=True)
    # Determinism (same signals -> same ordering)
    again = client.post("/api/recommendations/personal", json=body, headers=guest_headers).json()
    assert [i["movie"]["id"] for i in again["results"]] == [i["movie"]["id"] for i in r["results"]]


def test_group_recommendations(client):
    body = {"members": [{"username": "a", "emotions": {"happy": 1.0}}, {"username": "b", "emotions": {"fear": 1.0}}]}
    r = client.post("/api/recommendations/group", json=body).json()
    assert r["member_count"] == 2
    assert r["results"]
    top = r["results"][0]
    assert {"score", "std_dev", "agreement", "selectability"} <= set(top)


def test_feedback_updates_weights(client, guest_headers):
    r = client.post("/api/recommendations/feedback", json={"outcome": "select"}, headers=guest_headers).json()
    assert abs(sum(r["weights"]) - 1.0) < 1e-6
    assert r["persisted"] is False  # guest


def test_friends_seeded(client, auth_headers):
    r = client.get("/api/friends", headers=auth_headers).json()
    assert len(r["friends"]) == 5
    assert len(r["requests"]) == 2
    assert len(r["suggestions"]) == 3
    assert len(r["movie_suggestions"]) == 3
    assert r["movie_suggestions"][0]["movie"]["title"]


def test_library_idempotent_add(client, auth_headers):
    for _ in range(2):
        r = client.post("/api/library/items", json={"movie_id": 3, "kind": "wishlist"}, headers=auth_headers)
        assert r.status_code == 201
    items = client.get("/api/library/items", headers=auth_headers).json()
    assert sum(1 for i in items if i["movie"]["id"] == 3 and i["kind"] == "wishlist") == 1
    client.delete("/api/library/items", params={"movie_id": 3, "kind": "wishlist"}, headers=auth_headers)
    items = client.get("/api/library/items", headers=auth_headers).json()
    assert not any(i["movie"]["id"] == 3 for i in items)


def test_history_progress_bounds(client, auth_headers):
    ok = client.post("/api/history", json={"movie_id": 5, "event_type": "progress", "progress_pct": 42.5}, headers=auth_headers)
    assert ok.status_code == 201
    bad = client.post("/api/history", json={"movie_id": 5, "progress_pct": 140}, headers=auth_headers)
    assert bad.status_code == 422
    history = client.get("/api/history", headers=auth_headers).json()
    assert history[0]["movie"]["id"] == 5


def test_playlist_crud(client, auth_headers):
    p = client.post("/api/playlists", json={"name": "Weekend"}, headers=auth_headers).json()
    client.post(f"/api/playlists/{p['id']}/items", json={"movie_id": 1}, headers=auth_headers)
    client.post(f"/api/playlists/{p['id']}/items", json={"movie_id": 2}, headers=auth_headers)
    got = client.get("/api/playlists", headers=auth_headers).json()
    mine = next(x for x in got if x["id"] == p["id"])
    assert [m["id"] for m in mine["movies"]] == [1, 2]
    client.delete(f"/api/playlists/{p['id']}/items/1", headers=auth_headers)
    client.delete(f"/api/playlists/{p['id']}", headers=auth_headers)
    got = client.get("/api/playlists", headers=auth_headers).json()
    assert not any(x["id"] == p["id"] for x in got)
