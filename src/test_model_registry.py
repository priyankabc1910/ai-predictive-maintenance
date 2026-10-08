from src.model_registry import (
    get_lstm_model_metadata,
    get_registered_models,
)


def test_get_lstm_model_metadata():
    metadata = get_lstm_model_metadata()

    assert metadata.name == "LSTM RUL Predictor"
    assert metadata.model_type == "LSTM"
    assert metadata.dataset == "NASA C-MAPSS FD001"
    assert metadata.target == "RUL"
    assert metadata.version == "1.0.0"
    assert metadata.artifact_path == (
        "models/lstm_rul_model_FD001.keras"
    )
    assert metadata.description


def test_get_registered_models():
    models = get_registered_models()

    assert len(models) == 1

    model = models[0]

    assert model.name == "LSTM RUL Predictor"
    assert model.model_type == "LSTM"
    assert model.target == "RUL"


if __name__ == "__main__":
    test_get_lstm_model_metadata()
    test_get_registered_models()

    print("Model registry tests passed.")