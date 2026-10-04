from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import numpy as np
import joblib
import pandas as pd
import tensorflow as tf

from src.predictor import predict_engine
from .schemas import PredictionResponse


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "train_FD001.txt"
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

ANOMALY_MODEL_PATH = (
    BASE_DIR
    / "models"
    / "anomaly_model_FD001.pkl"
)

ANOMALY_SCALER_PATH = (
    BASE_DIR
    / "models"
    / "anomaly_scaler_FD001.pkl"
)

ANOMALY_FEATURES_PATH = (
    BASE_DIR
    / "models"
    / "anomaly_features_FD001.pkl"
)


# --------------------------------------------------
# Model configuration
# --------------------------------------------------

WINDOW_SIZE = 30

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


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="AI Predictive Maintenance API",
    description="Backend API for RUL prediction and maintenance intelligence",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Load models and data
# --------------------------------------------------

model = tf.keras.models.load_model(MODEL_PATH)

scaler = joblib.load(
    SCALER_PATH
)

anomaly_model = joblib.load(
    ANOMALY_MODEL_PATH
)

anomaly_scaler = joblib.load(
    ANOMALY_SCALER_PATH
)

anomaly_features = joblib.load(
    ANOMALY_FEATURES_PATH
)


# --------------------------------------------------
# Load raw NASA C-MAPSS data
# --------------------------------------------------

COLUMN_NAMES = [
    "unit_id",
    "cycle",
    "op_setting_1",
    "op_setting_2",
    "op_setting_3",
] + [
    f"sensor_{i}"
    for i in range(1, 22)
]


raw_df = pd.read_csv(
    RAW_DATA_PATH,
    sep=r"\s+",
    header=None,
    names=COLUMN_NAMES,
)


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "predictive-maintenance-api",
        "model": "LSTM",
        "anomaly_detector": "Isolation Forest",
    }


# --------------------------------------------------
# Model information
# --------------------------------------------------

@app.get("/model/info")
def model_info():

    return {
        "model_type": "LSTM",
        "anomaly_model": "Isolation Forest",
        "dataset": "NASA C-MAPSS FD001",
        "window_size": WINDOW_SIZE,
        "sensor_count": len(SENSOR_COLUMNS),
        "sensors": SENSOR_COLUMNS,
        "anomaly_features": anomaly_features,
        "task": "Remaining Useful Life prediction and anomaly detection",
    }


# --------------------------------------------------
# RUL prediction
# --------------------------------------------------

@app.get(
    "/predict/{engine_id}",
    response_model=PredictionResponse,
)
def predict(engine_id: int):

    engine_data = raw_df[
        raw_df["unit_id"] == engine_id
    ].copy()

    if engine_data.empty:

        raise HTTPException(
            status_code=404,
            detail=f"Engine {engine_id} not found.",
        )

    try:

        result = predict_engine(
            engine_data=engine_data,
            engine_id=engine_id,
            model=model,
            scaler=scaler,
            sensor_columns=SENSOR_COLUMNS,
            window_size=WINDOW_SIZE,
        )

        return {
            "machine_id": f"UNIT-{engine_id:03d}",
            "engine_id": result.engine_id,
            "rul": result.rul,
            "health_score": result.health_score,
            "risk_level": result.risk_level,
            "recommendation": result.recommendation,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


# --------------------------------------------------
# Fleet predictions
# --------------------------------------------------

@app.get(
    "/fleet",
    response_model=list[PredictionResponse],
)
def predict_fleet():

    predictions = []

    engine_ids = sorted(
        raw_df["unit_id"].unique()
    )

    for engine_id in engine_ids:

        engine_data = raw_df[
            raw_df["unit_id"] == engine_id
        ].copy()

        try:

            result = predict_engine(
                engine_data=engine_data,
                engine_id=int(engine_id),
                model=model,
                scaler=scaler,
                sensor_columns=SENSOR_COLUMNS,
                window_size=WINDOW_SIZE,
            )

            predictions.append(
                {
                    "machine_id": (
                        f"UNIT-{int(engine_id):03d}"
                    ),
                    "engine_id": result.engine_id,
                    "rul": result.rul,
                    "health_score": result.health_score,
                    "risk_level": result.risk_level,
                    "recommendation": result.recommendation,
                }
            )

        except ValueError:

            continue

    return predictions


# --------------------------------------------------
# Fleet summary
# --------------------------------------------------

@app.get("/fleet/summary")
def fleet_summary():

    predictions = predict_fleet()

    total_machines = len(predictions)

    critical = sum(
        1
        for p in predictions
        if p["risk_level"] == "CRITICAL"
    )

    high = sum(
        1
        for p in predictions
        if p["risk_level"] == "HIGH"
    )

    medium = sum(
        1
        for p in predictions
        if p["risk_level"] == "MEDIUM"
    )

    low = sum(
        1
        for p in predictions
        if p["risk_level"] == "LOW"
    )

    average_health = (
        sum(
            p["health_score"]
            for p in predictions
        )
        / total_machines
        if total_machines
        else 0
    )

    average_rul = (
        sum(
            p["rul"]
            for p in predictions
        )
        / total_machines
        if total_machines
        else 0
    )

    return {
        "total_machines": total_machines,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "average_health_score": round(
            average_health,
            2,
        ),
        "average_rul": round(
            average_rul,
            2,
        ),
    }


# --------------------------------------------------
# RUL trajectory
# --------------------------------------------------

@app.get(
    "/rul/trajectory/{engine_id}"
)
def rul_trajectory(engine_id: int):

    engine_data = raw_df[
        raw_df["unit_id"] == engine_id
    ].copy()

    if engine_data.empty:

        raise HTTPException(
            status_code=404,
            detail=f"Engine {engine_id} not found.",
        )

    engine_data = engine_data.sort_values(
        "cycle"
    )

    if len(engine_data) < WINDOW_SIZE:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Engine {engine_id} has fewer "
                f"than {WINDOW_SIZE} cycles."
            ),
        )

    # ----------------------------------------------
    # Build sliding windows
    # ----------------------------------------------

    sequences = []
    cycles = []

    sensor_data = (
        engine_data[SENSOR_COLUMNS].values
    )

    scaled_data = scaler.transform(
        sensor_data
    )

    for end_idx in range(
        WINDOW_SIZE,
        len(engine_data) + 1,
    ):

        window = scaled_data[
            end_idx - WINDOW_SIZE:end_idx
        ]

        sequences.append(window)

        cycles.append(
            int(
                engine_data.iloc[
                    end_idx - 1
                ]["cycle"]
            )
        )

    sequences = np.asarray(
        sequences
    )

    predictions = model.predict(
        sequences,
        verbose=0,
    ).reshape(-1)

    # ----------------------------------------------
    # Downsample for dashboard rendering
    # ----------------------------------------------

    max_points = 25

    if len(predictions) > max_points:

        indices = np.linspace(
            0,
            len(predictions) - 1,
            max_points,
            dtype=int,
        )

    else:

        indices = np.arange(
            len(predictions)
        )

    trajectory = [
        {
            "cycle": cycles[int(index)],
            "predicted_rul": round(
                float(
                    predictions[int(index)]
                ),
                2,
            ),
        }
        for index in indices
    ]

    return {
        "engine_id": engine_id,
        "machine_id": (
            f"UNIT-{engine_id:03d}"
        ),
        "model": "LSTM",
        "window_size": WINDOW_SIZE,
        "trajectory": trajectory,
    }

# --------------------------------------------------
# Fleet anomaly detection
# --------------------------------------------------

@app.get("/anomaly/fleet")
def fleet_anomaly_detection():

    results = []

    engine_ids = sorted(
        raw_df["unit_id"].unique()
    )

    for engine_id in engine_ids:

        engine_data = raw_df[
            raw_df["unit_id"] == engine_id
        ].copy()

        engine_data = engine_data.sort_values(
            "cycle"
        )

        if len(engine_data) < WINDOW_SIZE:
            continue

        latest_window = engine_data.tail(
            WINDOW_SIZE
        )

        features = latest_window[
            anomaly_features
        ]

        scaled_features = anomaly_scaler.transform(
            features
        )

        predictions = anomaly_model.predict(
            scaled_features
        )

        decision_scores = (
            anomaly_model.decision_function(
                scaled_features
            )
        )

        anomalous_cycles = int(
            (predictions == -1).sum()
        )

        anomaly_rate = (
            anomalous_cycles
            / len(predictions)
        )

        mean_decision_score = float(
            decision_scores.mean()
        )

        minimum_decision_score = float(
            decision_scores.min()
        )

        if anomaly_rate >= 0.50:
            severity = "CRITICAL"
        elif anomaly_rate >= 0.25:
            severity = "HIGH"
        elif anomaly_rate >= 0.10:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        results.append(
            {
                "machine_id": (
                    f"UNIT-{int(engine_id):03d}"
                ),
                "engine_id": int(engine_id),
                "model": "Isolation Forest",
                "cycles_analyzed": WINDOW_SIZE,
                "latest_cycle": int(
                    latest_window[
                        "cycle"
                    ].iloc[-1]
                ),
                "anomalous_cycles": anomalous_cycles,
                "anomaly_rate": round(
                    anomaly_rate,
                    3,
                ),
                "mean_decision_score": round(
                    mean_decision_score,
                    4,
                ),
                "minimum_decision_score": round(
                    minimum_decision_score,
                    4,
                ),
                "severity": severity,
            }
        )

    return results


# --------------------------------------------------
# Anomaly detection
# --------------------------------------------------

@app.get("/anomaly/{engine_id}")
def anomaly_detection(
    engine_id: int,
):

    engine_data = raw_df[
        raw_df["unit_id"] == engine_id
    ].copy()

    if engine_data.empty:

        raise HTTPException(
            status_code=404,
            detail=f"Engine {engine_id} not found.",
        )

    engine_data = engine_data.sort_values(
        "cycle"
    )

    if len(engine_data) < WINDOW_SIZE:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Engine {engine_id} has fewer "
                f"than {WINDOW_SIZE} cycles."
            ),
        )

    

    # ----------------------------------------------
    # Analyze latest operating window
    # ----------------------------------------------

    latest_window = engine_data.tail(
        WINDOW_SIZE
    )

    features = latest_window[
        anomaly_features
    ]

    scaled_features = anomaly_scaler.transform(
        features
    )

    predictions = anomaly_model.predict(
        scaled_features
    )

    decision_scores = (
        anomaly_model.decision_function(
            scaled_features
        )
    )

    anomalous_cycles = int(
        (predictions == -1).sum()
    )

    anomaly_rate = (
        anomalous_cycles
        / len(predictions)
    )

    mean_decision_score = float(
        decision_scores.mean()
    )

    minimum_decision_score = float(
        decision_scores.min()
    )

    # ----------------------------------------------
    # Business severity
    # ----------------------------------------------

    if anomaly_rate >= 0.50:

        severity = "CRITICAL"

    elif anomaly_rate >= 0.25:

        severity = "HIGH"

    elif anomaly_rate >= 0.10:

        severity = "MEDIUM"

    else:

        severity = "LOW"

    # ----------------------------------------------
    # Recommendation
    # ----------------------------------------------

    recommendations = {
        "CRITICAL": (
            "Immediate inspection recommended. "
            "Current sensor behaviour is highly "
            "deviant from the healthy baseline."
        ),
        "HIGH": (
            "Schedule inspection soon. "
            "Multiple recent operating cycles "
            "show abnormal sensor behaviour."
        ),
        "MEDIUM": (
            "Increase monitoring frequency and "
            "review sensor trends."
        ),
        "LOW": (
            "Sensor behaviour is within the "
            "learned healthy operating range."
        ),
    }

    return {
        "machine_id": (
            f"UNIT-{engine_id:03d}"
        ),
        "engine_id": engine_id,
        "model": "Isolation Forest",
        "baseline": (
            "First 30 operating cycles"
        ),
        "cycles_analyzed": WINDOW_SIZE,
        "latest_cycle": int(
            latest_window[
                "cycle"
            ].iloc[-1]
        ),
        "anomalous_cycles": anomalous_cycles,
        "anomaly_rate": round(
            anomaly_rate,
            3,
        ),
        "mean_decision_score": round(
            mean_decision_score,
            4,
        ),
        "minimum_decision_score": round(
            minimum_decision_score,
            4,
        ),
        "severity": severity,
        "recommendation": recommendations[
            severity
        ],
    }