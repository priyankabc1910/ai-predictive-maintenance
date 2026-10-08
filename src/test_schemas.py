from src.schemas import ModelMetadata, PredictionResult


def test_prediction_result_schema():
    result = PredictionResult(
        engine_id=1,
        rul=25.5,
        health_score=20.4,
        risk_level="HIGH",
        recommendation="Schedule maintenance at the earliest opportunity.",
    )

    assert result.engine_id == 1
    assert result.rul == 25.5
    assert result.health_score == 20.4
    assert result.risk_level == "HIGH"
    assert result.recommendation


def test_model_metadata_schema():
    metadata = ModelMetadata(
        name="LSTM RUL Predictor",
        model_type="LSTM",
        dataset="NASA C-MAPSS FD001",
        target="RUL",
        version="1.0.0",
        artifact_path="models/lstm_rul_model_FD001.keras",
        description="Temporal deep learning model for RUL prediction.",
    )

    assert metadata.name == "LSTM RUL Predictor"
    assert metadata.model_type == "LSTM"
    assert metadata.dataset == "NASA C-MAPSS FD001"
    assert metadata.target == "RUL"
    assert metadata.version == "1.0.0"
    assert metadata.artifact_path.endswith(".keras")
    assert metadata.description


if __name__ == "__main__":
    test_prediction_result_schema()
    test_model_metadata_schema()

    print("Schema tests passed.")