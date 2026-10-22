from fastapi.testclient import TestClient

from taskflow.api import app

HEALTH_URL = "/health"


def test_health_endpoint_returns_ok():
    with TestClient(app) as client:
        response = client.get(HEALTH_URL)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
