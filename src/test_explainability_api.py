
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_explainability_endpoint_exists():
    response = client.get("/explain/1")

    assert response.status_code != 404


def test_explainability_invalid_engine_returns_not_found():
    response = client.get("/explain/9999")

    assert response.status_code == 404
    assert "Engine 9999 not found." in response.json()["detail"]
