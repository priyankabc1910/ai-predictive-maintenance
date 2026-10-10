
from src.model_comparison import (
    compare_models,
    get_best_model,
    validate_model_result,
)


def sample_models():
    return [
        {"model": "RandomForest", "mae": 24.12, "rmse": 33.49},
        {"model": "XGBoost", "mae": 24.73, "rmse": 33.96},
        {"model": "LSTM", "mae": 22.11, "rmse": 32.98},
    ]


def test_compare_models():
    ranked = compare_models(sample_models())
    assert [model["model"] for model in ranked] == [
        "LSTM", "RandomForest", "XGBoost"
    ]
    assert [model["rank"] for model in ranked] == [1, 2, 3]


def test_get_best_model():
    best = get_best_model(sample_models())
    assert best["model"] == "LSTM"
    assert best["rank"] == 1


def test_compare_models_empty_input():
    assert compare_models([]) == []


def test_get_best_model_empty_input():
    import pytest
    with pytest.raises(ValueError, match="model_results cannot be empty"):
        get_best_model([])


def test_validate_model_result():
    validate_model_result(
        {"model": "LSTM", "mae": 22.11, "rmse": 32.98}
    )


def test_validate_missing_fields():
    import pytest
    with pytest.raises(ValueError, match="Missing required model fields"):
        validate_model_result({"model": "LSTM", "mae": 22.11})


def test_validate_negative_mae():
    import pytest
    with pytest.raises(ValueError, match="MAE cannot be negative"):
        validate_model_result({"model": "LSTM", "mae": -1.0, "rmse": 32.98})


def test_validate_negative_rmse():
    import pytest
    with pytest.raises(ValueError, match="RMSE cannot be negative"):
        validate_model_result({"model": "LSTM", "mae": 22.11, "rmse": -1.0})


def test_validate_rmse_lower_than_mae():
    import pytest
    with pytest.raises(ValueError, match="RMSE cannot be lower than MAE"):
        validate_model_result({"model": "LSTM", "mae": 30.0, "rmse": 20.0})
