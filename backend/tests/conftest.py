import os
import tempfile

import pytest

# Configure a throwaway database before any app module is imported.
_tmpdir = tempfile.mkdtemp(prefix="firetv-test-")
os.environ["DATABASE_URL"] = f"sqlite:///{_tmpdir}/test.db"
os.environ["SECRET_KEY"] = "test-secret-key-with-enough-length-for-hs256"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def auth_headers(client):
    token = client.post("/api/auth/login", json={"username": "demo", "password": "demo1234"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def guest_headers(client):
    token = client.post("/api/auth/guest").json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
