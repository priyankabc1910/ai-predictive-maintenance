from src.model_comparison import (
    compare_models,
    get_best_model,
)


def test_compare_models():
    model_results = [
        {
            "model": "RandomForest",
            "mae": 24.12,
            "rmse": 33.49,
        },
        {
            "model": "XGBoost",
            "mae": 24.73,
            "rmse": 33.96,
        },
        {
            "model": "LSTM",
            "mae": 22.11,
            "rmse": 32.98,
        },
    ]

    ranked = compare_models(model_results)

    assert len(ranked) == 3

    assert ranked[0]["model"] == "LSTM"
    assert ranked[1]["model"] == "RandomForest"
    assert ranked[2]["model"] == "XGBoost"

    assert ranked[0]["rank"] == 1
    assert ranked[1]["rank"] == 2
    assert ranked[2]["rank"] == 3

    for index in range(len(ranked) - 1):
        assert (
            ranked[index]["mae"]
            <= ranked[index + 1]["mae"]
        )


def test_get_best_model():
    model_results = [
        {
            "model": "RandomForest",
            "mae": 24.12,
            "rmse": 33.49,
        },
        {
            "model": "XGBoost",
            "mae": 24.73,
            "rmse": 33.96,
        },
        {
            "model": "LSTM",
            "mae": 22.11,
            "rmse": 32.98,
        },
    ]

    best_model = get_best_model(model_results)

    assert best_model["model"] == "LSTM"
    assert best_model["rank"] == 1


def test_compare_models_empty_input():
    result = compare_models([])

    assert result == []


def test_get_best_model_empty_input():
    try:
        get_best_model([])
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "model_results cannot be empty."


if __name__ == "__main__":
    test_compare_models()
    test_get_best_model()
    test_compare_models_empty_input()
    test_get_best_model_empty_input()

    print("Model comparison tests passed.")