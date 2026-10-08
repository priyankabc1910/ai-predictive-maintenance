from src.model_registry import (
    get_lstm_model_metadata,
    get_random_forest_metadata,
    get_xgboost_metadata,
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


def test_get_random_forest_metadata():
    metadata = get_random_forest_metadata()

    assert metadata.name == "Random Forest RUL Predictor"
    assert metadata.model_type == "RandomForest"
    assert metadata.dataset == "NASA C-MAPSS FD001"
    assert metadata.target == "RUL"
    assert metadata.version == "1.0.0"
    assert metadata.artifact_path == (
        "models/best_rul_model_FD001.pkl"
    )
    assert metadata.description


def test_get_xgboost_metadata():
    metadata = get_xgboost_metadata()

    assert metadata.name == "XGBoost RUL Predictor"
    assert metadata.model_type == "XGBoost"
    assert metadata.dataset == "NASA C-MAPSS FD001"
    assert metadata.target == "RUL"
    assert metadata.version == "1.0.0"
    assert metadata.artifact_path == (
        "models/xgb_rul_model_FD001.pkl"
    )
    assert metadata.description


def test_get_registered_models():
    models = get_registered_models()

    assert len(models) == 3

    model_types = {
        model.model_type
        for model in models
    }

    assert model_types == {
        "LSTM",
        "RandomForest",
        "XGBoost",
    }

    for model in models:
        assert model.dataset == "NASA C-MAPSS FD001"
        assert model.target == "RUL"
        assert model.version == "1.0.0"


if __name__ == "__main__":
    test_get_lstm_model_metadata()
    test_get_random_forest_metadata()
    test_get_xgboost_metadata()
    test_get_registered_models()

    print("Model registry tests passed.")