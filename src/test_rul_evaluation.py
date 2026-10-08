from src.rul_evaluation import (
    load_test_rul,
    load_test_data,
    load_test_evaluation_data,
    generate_test_predictions,
    evaluate_test_predictions,
)


def test_load_test_rul():
    data = load_test_rul()

    assert len(data) == 100

    assert list(data.columns) == [
        "engine_id",
        "actual_rul",
    ]

    assert data["engine_id"].iloc[0] == 1
    assert data["engine_id"].iloc[-1] == 100

    assert data["actual_rul"].iloc[0] == 112
    assert data["actual_rul"].iloc[1] == 98


def test_load_test_data():
    data = load_test_data()

    assert not data.empty

    assert "unit_id" in data.columns
    assert "cycle" in data.columns

    assert data["unit_id"].nunique() == 100


def test_load_test_evaluation_data():
    data = load_test_evaluation_data()

    assert len(data) == 100

    assert list(data.columns) == [
        "engine_id",
        "last_cycle",
        "actual_rul",
    ]

    assert data["engine_id"].iloc[0] == 1
    assert data["engine_id"].iloc[-1] == 100

    assert data["actual_rul"].notna().all()
    assert data["last_cycle"].notna().all()


def test_generate_test_predictions():
    predictions = generate_test_predictions()

    assert len(predictions) == 100

    assert predictions[0]["engine_id"] == 1
    assert predictions[-1]["engine_id"] == 100

    for prediction in predictions:
        assert "engine_id" in prediction
        assert "predicted_rul" in prediction
        assert prediction["predicted_rul"] >= 0


def test_evaluate_test_predictions():
    result = evaluate_test_predictions()

    assert result["engine_count"] == 100

    assert "mae" in result
    assert "rmse" in result

    assert result["mae"] >= 0
    assert result["rmse"] >= 0

    assert result["rmse"] >= result["mae"]


if __name__ == "__main__":
    test_load_test_rul()
    test_load_test_data()
    test_load_test_evaluation_data()
    test_generate_test_predictions()
    test_evaluate_test_predictions()
    print("RUL evaluation tests passed.")