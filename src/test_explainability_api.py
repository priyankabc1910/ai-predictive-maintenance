
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


def test_maintenance_intelligence_endpoint_exists():
    response = client.get("/maintenance/intelligence/1")

    assert response.status_code != 404


def test_maintenance_intelligence_invalid_engine_returns_not_found():
    response = client.get("/maintenance/intelligence/9999")

    assert response.status_code == 404
    assert "Engine 9999 not found." in response.json()["detail"]

