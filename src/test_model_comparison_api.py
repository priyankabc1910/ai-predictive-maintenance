from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_model_comparison_endpoint():
    response = client.get("/models/comparison")

    assert response.status_code == 200

    data = response.json()

    assert "models" in data
    assert "best_model" in data

    models = data["models"]
    best_model = data["best_model"]

    assert len(models) == 3

    assert models[0]["model"] == "LSTM"
    assert models[1]["model"] == "RandomForest"
    assert models[2]["model"] == "XGBoost"

    assert models[0]["rank"] == 1
    assert models[1]["rank"] == 2
    assert models[2]["rank"] == 3

    assert best_model["model"] == "LSTM"
    assert best_model["rank"] == 1

    for model in models:
        assert "model" in model
        assert "mae" in model
        assert "rmse" in model
        assert "rank" in model

        assert model["mae"] >= 0
        assert model["rmse"] >= 0
        assert model["rmse"] >= model["mae"]


if __name__ == "__main__":
    test_model_comparison_endpoint()

    print("Model comparison API test passed.")