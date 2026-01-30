import pytest

from fakeredis.aioredis import FakeRedis
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_redis


@pytest.fixture(autouse=True)
def fake_redis(monkeypatch) -> FakeRedis:
    """Изолируем Redis"""

    redis_instance = FakeRedis(decode_responses=True)
    app.dependency_overrides[get_redis] = lambda: redis_instance
    return redis_instance


@pytest.fixture
def client():
    return TestClient(app)


def test_get_credit_with_open_history_returns_cached(client):
    payload = {
        "income": 45000,
        "history": [
            {"sum": "1000", "credit_date": "2023-01-10", "is_closed": False}
        ],
    }

    response = client.post("/score", json=payload)
    assert response.status_code == 201
    assert response.json()["result"] == 30000.0

def test_income_branches(client):
    response = client.post("/score", json={"income": 52000, "history": []})
    assert response.status_code == 201
    assert response.json()["result"] == 20000.0

    response = client.post("/score", json={"income": 40000, "history": []})
    assert response.status_code == 201
    assert response.json()["result"] == 10000.0

    response = client.post("/score", json={"income": 20000, "history": []})
    assert response.status_code == 201
    assert response.json()["result"] == 0.0


def test_metrics_endpoint_exports_metrics(client):
    client.post("/score", json={"income": 20000, "history": []})
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "http_requests_total" in r.text
    assert "http_request_duration_seconds" in r.text