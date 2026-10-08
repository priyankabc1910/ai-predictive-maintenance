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


def test_rul_evaluation_api_consistency():
    response = client.get("/evaluation/rul")

    assert response.status_code == 200

    data = response.json()

    metrics = data["metrics"]
    error_summary = data["error_summary"]
    worst_predictions = data["worst_predictions"]

    # Dataset-level consistency
    assert metrics["engine_count"] == error_summary["engine_count"]
    assert metrics["engine_count"] == 100

    # Error distribution consistency
    assert (
        error_summary["median_absolute_error"]
        <= error_summary["p90_absolute_error"]
    )

    assert (
        error_summary["p90_absolute_error"]
        <= error_summary["p95_absolute_error"]
    )

    assert (
        error_summary["p95_absolute_error"]
        <= error_summary["maximum_absolute_error"]
    )

    # Worst predictions must be ordered by absolute error
    for index in range(len(worst_predictions) - 1):
        assert (
            worst_predictions[index]["absolute_error"]
            >= worst_predictions[index + 1]["absolute_error"]
        )

    # First result should represent the maximum error
    assert (
    round(worst_predictions[0]["absolute_error"], 4)
    == error_summary["maximum_absolute_error"]
)


if __name__ == "__main__":
    test_rul_evaluation_endpoint()
    test_rul_evaluation_api_consistency()

    print("RUL evaluation API tests passed.")