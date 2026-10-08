from pathlib import Path

import joblib
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