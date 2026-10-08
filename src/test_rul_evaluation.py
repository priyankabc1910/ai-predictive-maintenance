import joblib

from src.rul_evaluation import (
    load_test_rul,
    load_test_data,
    load_test_evaluation_data,
    generate_test_predictions,
    evaluate_test_predictions,
    build_test_error_analysis,
    summarize_test_errors,
    save_test_evaluation_results,
)

def test_save_test_evaluation_results():
    output_path = save_test_evaluation_results()

    assert output_path.exists()
    assert output_path.name == "rul_evaluation_FD001.pkl"

    saved_results = joblib.load(output_path)

    assert "metrics" in saved_results
    assert "error_summary" in saved_results
    assert "worst_predictions" in saved_results

    assert saved_results["metrics"]["engine_count"] == 100
    assert len(saved_results["worst_predictions"]) == 10

def test_summarize_test_errors():
    result = summarize_test_errors()

    assert result["engine_count"] == 100

    assert result["mean_absolute_error"] >= 0
    assert result["median_absolute_error"] >= 0
    assert result["maximum_absolute_error"] >= 0
    assert result["p90_absolute_error"] >= 0
    assert result["p95_absolute_error"] >= 0

    assert (
        result["median_absolute_error"]
        <= result["p90_absolute_error"]
    )

    assert (
        result["p90_absolute_error"]
        <= result["p95_absolute_error"]
    )

    assert (
        result["p95_absolute_error"]
        <= result["maximum_absolute_error"]
    )


def test_build_test_error_analysis():
    data = build_test_error_analysis()

    assert len(data) == 100

    assert list(data.columns) == [
        "engine_id",
        "actual_rul",
        "predicted_rul",
        "error",
        "absolute_error",
        "squared_error",
    ]

    assert data["absolute_error"].ge(0).all()
    assert data["squared_error"].ge(0).all()

    assert (
        data["absolute_error"].iloc[0]
        >= data["absolute_error"].iloc[-1]
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
    test_build_test_error_analysis()
    test_summarize_test_errors()
    test_save_test_evaluation_results()

    print("RUL evaluation tests passed.")