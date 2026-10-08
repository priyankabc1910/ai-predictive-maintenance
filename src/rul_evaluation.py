from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

from .preprocessing import prepare_lstm_sequence


BASE_DIR = Path(__file__).resolve().parents[1]

TEST_DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "test_FD001.txt"
)

RUL_DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "RUL_FD001.txt"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "lstm_rul_model_FD001.keras"
)

SCALER_PATH = (
    BASE_DIR
    / "models"
    / "lstm_scaler_FD001.pkl"
)

SENSOR_COLUMNS = [
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_7",
    "sensor_8",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_15",
    "sensor_17",
    "sensor_20",
    "sensor_21",
]

WINDOW_SIZE = 30


def load_test_rul() -> pd.DataFrame:
    """
    Load the official RUL values for the FD001 test set.

    Each row corresponds to one test engine.
    Engine IDs are assigned sequentially from 1.
    """

    rul_values = pd.read_csv(
        RUL_DATA_PATH,
        header=None,
        names=["actual_rul"],
    )

    rul_values["engine_id"] = range(
        1,
        len(rul_values) + 1,
    )

    return rul_values[
        [
            "engine_id",
            "actual_rul",
        ]
    ]


def load_test_data() -> pd.DataFrame:
    """
    Load the NASA C-MAPSS FD001 test dataset.
    """

    column_names = [
        "unit_id",
        "cycle",
        "op_setting_1",
        "op_setting_2",
        "op_setting_3",
    ] + [
        f"sensor_{i}"
        for i in range(1, 22)
    ]

    return pd.read_csv(
        TEST_DATA_PATH,
        sep=r"\s+",
        header=None,
        names=column_names,
    )


def load_test_evaluation_data() -> pd.DataFrame:
    """
    Combine test engine metadata with the
    official ground-truth RUL values.
    """

    test_data = load_test_data()
    test_rul = load_test_rul()

    engine_summary = (
        test_data
        .groupby("unit_id")["cycle"]
        .max()
        .reset_index()
        .rename(
            columns={
                "unit_id": "engine_id",
                "cycle": "last_cycle",
            }
        )
    )

    evaluation_data = engine_summary.merge(
        test_rul,
        on="engine_id",
        how="inner",
    )

    return (
        evaluation_data
        .sort_values("engine_id")
        .reset_index(drop=True)
    )


def load_lstm_evaluation_artifacts():
    """
    Load the trained LSTM model and its scaler.
    """

    model = load_model(
        MODEL_PATH
    )

    scaler = joblib.load(
        SCALER_PATH
    )

    return model, scaler


def generate_test_predictions():
    """
    Generate one RUL prediction for each test engine
    using its latest 30 operating cycles.
    """

    test_data = load_test_data()

    model, scaler = (
        load_lstm_evaluation_artifacts()
    )

    predictions = []

    for engine_id in sorted(
        test_data["unit_id"].unique()
    ):
        engine_data = test_data[
            test_data["unit_id"] == engine_id
        ].copy()

        engine_data = engine_data.sort_values(
            "cycle"
        )

        if len(engine_data) < WINDOW_SIZE:
            raise ValueError(
                f"Engine {engine_id} has fewer "
                f"than {WINDOW_SIZE} cycles."
            )

        sequence = prepare_lstm_sequence(
            engine_data=engine_data,
            sensor_columns=SENSOR_COLUMNS,
            scaler=scaler,
            window_size=WINDOW_SIZE,
        )

        prediction = model.predict(
            sequence,
            verbose=0,
        )

        predicted_rul = float(
            prediction[0][0]
        )

        predictions.append(
            {
                "engine_id": int(engine_id),
                "predicted_rul": predicted_rul,
            }
        )

    return predictions


def evaluate_test_predictions():
    """
    Generate held-out test predictions and compare them
    with the official NASA RUL ground truth.
    """

    predictions = generate_test_predictions()

    prediction_df = pd.DataFrame(
        predictions
    )

    ground_truth = load_test_rul()

    evaluation = ground_truth.merge(
        prediction_df,
        on="engine_id",
        how="inner",
    )

    actual = evaluation[
        "actual_rul"
    ].to_numpy()

    predicted = evaluation[
        "predicted_rul"
    ].to_numpy()

    errors = predicted - actual

    mae = float(
        np.mean(
            np.abs(errors)
        )
    )

    rmse = float(
        np.sqrt(
            np.mean(
                errors ** 2
            )
        )
    )

    return {
        "model": "LSTM",
        "dataset": "NASA C-MAPSS FD001",
        "engine_count": len(evaluation),
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
    }

def build_test_error_analysis() -> pd.DataFrame:
    """
    Build per-engine RUL prediction errors for the
    official FD001 test set.
    """

    predictions = generate_test_predictions()

    prediction_df = pd.DataFrame(
        predictions
    )

    ground_truth = load_test_rul()

    evaluation = ground_truth.merge(
        prediction_df,
        on="engine_id",
        how="inner",
    )

    evaluation["error"] = (
        evaluation["predicted_rul"]
        - evaluation["actual_rul"]
    )

    evaluation["absolute_error"] = (
        evaluation["error"].abs()
    )

    evaluation["squared_error"] = (
        evaluation["error"] ** 2
    )

    return evaluation.sort_values(
        "absolute_error",
        ascending=False,
    ).reset_index(drop=True)

def summarize_test_errors() -> dict:
    """
    Summarize the distribution of RUL prediction errors
    across the official FD001 test set.
    """

    evaluation = build_test_error_analysis()

    absolute_errors = evaluation[
        "absolute_error"
    ]

    return {
        "engine_count": len(evaluation),
        "mean_absolute_error": round(
            float(absolute_errors.mean()),
            4,
        ),
        "median_absolute_error": round(
            float(absolute_errors.median()),
            4,
        ),
        "maximum_absolute_error": round(
            float(absolute_errors.max()),
            4,
        ),
        "p90_absolute_error": round(
            float(absolute_errors.quantile(0.90)),
            4,
        ),
        "p95_absolute_error": round(
            float(absolute_errors.quantile(0.95)),
            4,
        ),
    }

def save_test_evaluation_results(output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = BASE_DIR / "models" / "rul_evaluation_FD001.pkl"

    results = {
        "metrics": evaluate_test_predictions(),
        "error_summary": summarize_test_errors(),
        "worst_predictions": build_test_error_analysis()
        .head(10)
        .to_dict(orient="records"),
    }

    joblib.dump(results, output_path)
    return output_path

def get_worst_rul_predictions(limit: int = 10) -> list[dict]:
    if limit <= 0:
        raise ValueError("limit must be greater than zero.")

    evaluation = build_test_error_analysis()

    worst_predictions = evaluation.head(limit).copy()

    return worst_predictions[
        [
            "engine_id",
            "actual_rul",
            "predicted_rul",
            "error",
            "absolute_error",
        ]
    ].to_dict(orient="records")

get_worst_rul_predictions,
def test_get_worst_rul_predictions():
    results = get_worst_rul_predictions(limit=5)

    assert len(results) == 5

    required_fields = {
        "engine_id",
        "actual_rul",
        "predicted_rul",
        "error",
        "absolute_error",
    }

    for result in results:
        assert required_fields.issubset(result.keys())
        assert result["absolute_error"] >= 0

    # Results must be ordered from worst to best
    for i in range(len(results) - 1):
        assert (
            results[i]["absolute_error"]
            >= results[i + 1]["absolute_error"]
        )