from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_rul_evaluation_endpoint():
    response = client.get("/evaluation/rul")

    assert response.status_code == 200

    data = response.json()

    assert "metrics" in data
    assert "error_summary" in data
    assert "worst_predictions" in data

    metrics = data["metrics"]

    assert metrics["model"] == "LSTM"
    assert metrics["dataset"] == "NASA C-MAPSS FD001"
    assert metrics["engine_count"] == 100

    assert metrics["mae"] >= 0
    assert metrics["rmse"] >= 0
    assert metrics["rmse"] >= metrics["mae"]

    error_summary = data["error_summary"]

    assert error_summary["engine_count"] == 100
    assert error_summary["mean_absolute_error"] >= 0
    assert error_summary["median_absolute_error"] >= 0
    assert error_summary["maximum_absolute_error"] >= 0
    assert error_summary["p90_absolute_error"] >= 0
    assert error_summary["p95_absolute_error"] >= 0

    worst_predictions = data["worst_predictions"]

    assert len(worst_predictions) == 10

    for prediction in worst_predictions:
        assert "engine_id" in prediction
        assert "actual_rul" in prediction
        assert "predicted_rul" in prediction
        assert "error" in prediction
        assert "absolute_error" in prediction

        assert prediction["absolute_error"] >= 0

if __name__ == "__main__":
    test_rul_evaluation_endpoint()

    print("RUL evaluation API test passed.")