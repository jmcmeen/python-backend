import uuid

from app.core.database import get_db
from app.main import app
from tests.conftest import override_get_db


async def test_health_returns_ok(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_ready_returns_ok_when_db_reachable(client):
    response = await client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


async def test_ready_returns_503_when_db_unavailable(client):
    class _FailingSession:
        async def execute(self, *args, **kwargs):
            raise RuntimeError("simulated DB outage")

    async def _failing_get_db():
        yield _FailingSession()

    app.dependency_overrides[get_db] = _failing_get_db
    try:
        response = await client.get("/ready")
    finally:
        app.dependency_overrides[get_db] = override_get_db

    assert response.status_code == 503
    assert response.json() == {"detail": "database unavailable"}


async def test_request_id_echoed_when_provided(client):
    response = await client.get("/health", headers={"X-Request-ID": "abc123"})
    assert response.headers["X-Request-ID"] == "abc123"


async def test_request_id_generated_when_absent(client):
    response = await client.get("/health")
    assert "X-Request-ID" in response.headers
    uuid.UUID(response.headers["X-Request-ID"])
