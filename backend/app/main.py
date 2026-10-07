from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import numpy as np
import joblib
import pandas as pd
import tensorflow as tf

from src.fleet_anomaly import (
    aggregate_fleet_anomalies,
    classify_fleet_anomaly_rate,
)
from src.fleet_prioritization import prioritize_fleet
from src.anomaly_trends import (
    analyze_anomaly_trend,
    summarize_fleet_anomaly_trends,
)
from src.maintenance_engine import calculate_maintenance_decision
from src.explainability import explain_maintenance_decision
from src.sensor_trends import analyze_sensor_trends
from src.knowledge_retriever import (
    build_maintenance_guidance_response,
)
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

TEST_DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "test_FD001.txt"
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

test_df = pd.read_csv(
    TEST_DATA_PATH,
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

@app.get("/anomaly/fleet/summary")
def fleet_anomaly_summary():
    engine_results = []

    for engine_id in sorted(test_df["unit_id"].unique()):
        engine_data = test_df[
            test_df["unit_id"] == engine_id
        ].copy()

        engine_data = engine_data.sort_values("cycle")

        if len(engine_data) < WINDOW_SIZE:
            continue

        latest_window = engine_data.tail(WINDOW_SIZE)

        features = latest_window[anomaly_features]

        scaled_features = anomaly_scaler.transform(
            features
        )

        predictions = anomaly_model.predict(
            scaled_features
        )

        anomalous_cycles = int(
            (predictions == -1).sum()
        )

        anomaly_rate = (
            anomalous_cycles / len(predictions)
        )

        severity = classify_fleet_anomaly_rate(
            anomaly_rate
        )

        engine_results.append(
            {
                "engine_id": int(engine_id),
                "machine_id": f"UNIT-{int(engine_id):03d}",
                "anomaly_rate": round(
                    anomaly_rate,
                    3,
                ),
                "anomalous_cycles": anomalous_cycles,
                "severity": severity,
            }
        )

    result = aggregate_fleet_anomalies(
        engine_results
    )

    return result

@app.get("/anomaly/fleet/trends")
def fleet_anomaly_trends():
    engine_results = []

    for engine_id in sorted(test_df["unit_id"].unique()):
        engine_data = test_df[
            test_df["unit_id"] == engine_id
        ].copy()

        engine_data = engine_data.sort_values("cycle")

        if len(engine_data) < WINDOW_SIZE * 2:
            continue

        previous_window = engine_data.iloc[
            -WINDOW_SIZE * 2:-WINDOW_SIZE
        ]

        current_window = engine_data.iloc[
            -WINDOW_SIZE:
        ]

        previous_features = previous_window[
            anomaly_features
        ]

        current_features = current_window[
            anomaly_features
        ]

        previous_scaled = anomaly_scaler.transform(
            previous_features
        )

        current_scaled = anomaly_scaler.transform(
            current_features
        )

        previous_predictions = anomaly_model.predict(
            previous_scaled
        )

        current_predictions = anomaly_model.predict(
            current_scaled
        )

        trend_result = analyze_anomaly_trend(
            previous_predictions=previous_predictions.tolist(),
            current_predictions=current_predictions.tolist(),
        )

        engine_results.append(
            {
                "engine_id": int(engine_id),
                "machine_id": f"UNIT-{int(engine_id):03d}",
                **trend_result,
            }
        )

    fleet_summary = summarize_fleet_anomaly_trends(
        engine_results
    )

    return {
        **fleet_summary,
        "engines": engine_results,
    }

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

# --------------------------------------------------
# Sensor degradation trends
# --------------------------------------------------

@app.get("/sensors/{engine_id}/trends")
def sensor_trends(engine_id: int):

    try:
        result = analyze_sensor_trends(
            engine_id=engine_id
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    # --------------------------------------------------
# Maintenance decision
# --------------------------------------------------
@app.get("/maintenance/fleet")
def get_fleet_maintenance():
    maintenance_decisions = []

    for engine_id in sorted(test_df["unit_id"].unique()):
        try:
            engine_data = test_df[
                test_df["unit_id"] == engine_id
            ].copy()

            prediction = predict_engine(
                engine_data=engine_data,
                engine_id=engine_id,
                model=model,
                scaler=scaler,
                sensor_columns=SENSOR_COLUMNS,
                window_size=WINDOW_SIZE,
            )

            engine_data = engine_data.sort_values("cycle")

            if len(engine_data) < WINDOW_SIZE:
                continue

            latest_window = engine_data.tail(WINDOW_SIZE)

            features = latest_window[anomaly_features]
            scaled_features = anomaly_scaler.transform(features)

            anomaly_predictions = anomaly_model.predict(
                scaled_features
            )

            anomaly_rate = float(
                (anomaly_predictions == -1).sum()
                / len(anomaly_predictions)
            )

            if anomaly_rate >= 0.50:
                anomaly_severity = "CRITICAL"
            elif anomaly_rate >= 0.25:
                anomaly_severity = "HIGH"
            elif anomaly_rate >= 0.10:
                anomaly_severity = "MEDIUM"
            else:
                anomaly_severity = "LOW"

            try:
                sensor_result = analyze_sensor_trends(
                    engine_id,
                    engine_data=engine_data,
                )

                critical_sensor_count = sum(
                    1
                    for sensor in sensor_result["sensors"]
                    if sensor["severity"] == "CRITICAL"
                )

                high_sensor_count = sum(
                    1
                    for sensor in sensor_result["sensors"]
                    if sensor["severity"] == "HIGH"
                )

            except ValueError:
                critical_sensor_count = 0
                high_sensor_count = 0

            maintenance_decision = calculate_maintenance_decision(
                rul=prediction.rul,
                risk_level=prediction.risk_level,
                anomaly_rate=anomaly_rate,
                anomaly_severity=anomaly_severity,
                critical_sensor_count=critical_sensor_count,
                high_sensor_count=high_sensor_count,
            )

            maintenance_decisions.append(
                {
                    "engine_id": prediction.engine_id,
                    "machine_id": f"UNIT-{engine_id:03d}",
                    "rul": prediction.rul,
                    "maintenance_score": maintenance_decision[
                        "maintenance_score"
                    ],
                    "priority": maintenance_decision["priority"],
                }
            )

        except Exception:
            continue

    return prioritize_fleet(maintenance_decisions)


@app.get("/maintenance/{engine_id}")
def get_maintenance_decision(engine_id: int):

    engine_data = raw_df[
        raw_df["unit_id"] == engine_id
    ].copy()

    if engine_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Engine {engine_id} not found.",
        )

    try:
        # ------------------------------------------
        # RUL prediction
        # ------------------------------------------

        prediction = predict_engine(
            engine_data=engine_data,
            engine_id=engine_id,
            model=model,
            scaler=scaler,
            sensor_columns=SENSOR_COLUMNS,
            window_size=WINDOW_SIZE,
        )

        # ------------------------------------------
        # Anomaly detection
        # ------------------------------------------

        engine_data = engine_data.sort_values("cycle")

        if len(engine_data) < WINDOW_SIZE:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Engine {engine_id} has fewer "
                    f"than {WINDOW_SIZE} cycles."
                ),
            )

        latest_window = engine_data.tail(WINDOW_SIZE)

        features = latest_window[
            anomaly_features
        ]

        scaled_features = anomaly_scaler.transform(
            features
        )

        anomaly_predictions = anomaly_model.predict(
            scaled_features
        )

        anomaly_rate = float(
            (anomaly_predictions == -1).sum()
            / len(anomaly_predictions)
        )

        if anomaly_rate >= 0.50:
            anomaly_severity = "CRITICAL"
        elif anomaly_rate >= 0.25:
            anomaly_severity = "HIGH"
        elif anomaly_rate >= 0.10:
            anomaly_severity = "MEDIUM"
        else:
            anomaly_severity = "LOW"

        # ------------------------------------------
        # Sensor degradation
        # ------------------------------------------

        sensor_result = analyze_sensor_trends(
            engine_id
        )

        critical_sensor_count = sum(
            1
            for sensor in sensor_result["sensors"]
            if sensor["severity"] == "CRITICAL"
        )

        high_sensor_count = sum(
            1
            for sensor in sensor_result["sensors"]
            if sensor["severity"] == "HIGH"
        )

        # ------------------------------------------
        # Maintenance decision
        # ------------------------------------------

        decision = calculate_maintenance_decision(
            rul=prediction.rul,
            risk_level=prediction.risk_level,
            anomaly_rate=anomaly_rate,
            anomaly_severity=anomaly_severity,
            critical_sensor_count=critical_sensor_count,
            high_sensor_count=high_sensor_count,
        )

        return {
            "engine_id": prediction.engine_id,
            "machine_id": f"UNIT-{prediction.engine_id:03d}",
            "rul": prediction.rul,
            "risk_level": prediction.risk_level,
            "anomaly_rate": round(
                anomaly_rate,
                3,
            ),
            "anomaly_severity": anomaly_severity,
            "critical_sensor_count": critical_sensor_count,
            "high_sensor_count": high_sensor_count,
            **decision,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

# --------------------------------------------------
# Maintenance explainability
# --------------------------------------------------

@app.get("/explain/{engine_id}")
def get_maintenance_explanation(engine_id: int):

    engine_data = raw_df[
        raw_df["unit_id"] == engine_id
    ].copy()

    if engine_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Engine {engine_id} not found.",
        )

    try:

        # ------------------------------------------
        # RUL prediction
        # ------------------------------------------

        prediction = predict_engine(
            engine_data=engine_data,
            engine_id=engine_id,
            model=model,
            scaler=scaler,
            sensor_columns=SENSOR_COLUMNS,
            window_size=WINDOW_SIZE,
        )

        # ------------------------------------------
        # Anomaly detection
        # ------------------------------------------

        engine_data = engine_data.sort_values("cycle")

        if len(engine_data) < WINDOW_SIZE:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Engine {engine_id} has fewer "
                    f"than {WINDOW_SIZE} cycles."
                ),
            )

        latest_window = engine_data.tail(WINDOW_SIZE)

        features = latest_window[
            anomaly_features
        ]

        scaled_features = anomaly_scaler.transform(
            features
        )

        anomaly_predictions = anomaly_model.predict(
            scaled_features
        )

        anomaly_rate = float(
            (anomaly_predictions == -1).sum()
            / len(anomaly_predictions)
        )

        if anomaly_rate >= 0.50:
            anomaly_severity = "CRITICAL"
        elif anomaly_rate >= 0.25:
            anomaly_severity = "HIGH"
        elif anomaly_rate >= 0.10:
            anomaly_severity = "MEDIUM"
        else:
            anomaly_severity = "LOW"

        # ------------------------------------------
        # Sensor degradation
        # ------------------------------------------

        sensor_result = analyze_sensor_trends(
            engine_id
        )

        critical_sensor_count = sum(
            1
            for sensor in sensor_result["sensors"]
            if sensor["severity"] == "CRITICAL"
        )

        high_sensor_count = sum(
            1
            for sensor in sensor_result["sensors"]
            if sensor["severity"] == "HIGH"
        )

        # ------------------------------------------
        # Explain decision
        # ------------------------------------------

        explanation = explain_maintenance_decision(
            rul=prediction.rul,
            risk_level=prediction.risk_level,
            anomaly_rate=anomaly_rate,
            anomaly_severity=anomaly_severity,
            critical_sensor_count=critical_sensor_count,
            high_sensor_count=high_sensor_count,
            sensor_data=sensor_result["sensors"],
        )

        return {
            "engine_id": prediction.engine_id,
            "machine_id": f"UNIT-{prediction.engine_id:03d}",
            **explanation,
        }

    except Exception as error:
     raise HTTPException(
        status_code=500,
        detail=f"{type(error).__name__}: {error}",
    )

# --------------------------------------------------
# Maintenance knowledge retrieval
# --------------------------------------------------

@app.get("/knowledge/{engine_id}")
def get_maintenance_knowledge(engine_id: int):

    engine_data = raw_df[
        raw_df["unit_id"] == engine_id
    ].copy()

    if engine_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Engine {engine_id} not found.",
        )

    try:

        # ------------------------------------------
        # RUL prediction
        # ------------------------------------------

        prediction = predict_engine(
            engine_data=engine_data,
            engine_id=engine_id,
            model=model,
            scaler=scaler,
            sensor_columns=SENSOR_COLUMNS,
            window_size=WINDOW_SIZE,
        )

        # ------------------------------------------
        # Anomaly detection
        # ------------------------------------------

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

        latest_window = engine_data.tail(
            WINDOW_SIZE
        )

        features = latest_window[
            anomaly_features
        ]

        scaled_features = anomaly_scaler.transform(
            features
        )

        anomaly_predictions = anomaly_model.predict(
            scaled_features
        )

        anomaly_rate = float(
            (anomaly_predictions == -1).sum()
            / len(anomaly_predictions)
        )

        # ------------------------------------------
        # Anomaly severity
        # ------------------------------------------

        if anomaly_rate >= 0.50:
            anomaly_severity = "CRITICAL"

        elif anomaly_rate >= 0.25:
            anomaly_severity = "HIGH"

        elif anomaly_rate >= 0.10:
            anomaly_severity = "MEDIUM"

        else:
            anomaly_severity = "LOW"

        # ------------------------------------------
        # Sensor degradation
        # ------------------------------------------

        sensor_result = analyze_sensor_trends(
            engine_id
        )

        critical_sensor_count = sum(
            1
            for sensor in sensor_result["sensors"]
            if sensor["severity"] == "CRITICAL"
        )

        high_sensor_count = sum(
            1
            for sensor in sensor_result["sensors"]
            if sensor["severity"] == "HIGH"
        )

        # ------------------------------------------
        # Knowledge retrieval
        # ------------------------------------------

        result = build_maintenance_guidance_response(
            engine_id=engine_id,
            risk_level=prediction.risk_level,
            rul=prediction.rul,
            anomaly_rate=anomaly_rate,
            critical_sensor_count=critical_sensor_count,
            high_sensor_count=high_sensor_count,
            sensor_data=sensor_result["sensors"],
            top_k=5,
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

@app.get("/maintenance/intelligence/{engine_id}")
def get_maintenance_intelligence(engine_id: int):

    engine_data = raw_df[
        raw_df["unit_id"] == engine_id
    ].copy()

    if engine_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Engine {engine_id} not found.",
        )

    try:

        # ==========================================
        # 1. RUL PREDICTION
        # ==========================================

        prediction = predict_engine(
            engine_data=engine_data,
            engine_id=engine_id,
            model=model,
            scaler=scaler,
            sensor_columns=SENSOR_COLUMNS,
            window_size=WINDOW_SIZE,
        )

        # ==========================================
        # 2. ANOMALY DETECTION
        # ==========================================

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

        latest_window = engine_data.tail(
            WINDOW_SIZE
        )

        features = latest_window[
            anomaly_features
        ]

        scaled_features = anomaly_scaler.transform(
            features
        )

        anomaly_predictions = anomaly_model.predict(
            scaled_features
        )

        anomaly_rate = float(
            (anomaly_predictions == -1).sum()
            / len(anomaly_predictions)
        )

        # ==========================================
        # 3. ANOMALY SEVERITY
        # ==========================================

        if anomaly_rate >= 0.50:
            anomaly_severity = "CRITICAL"

        elif anomaly_rate >= 0.25:
            anomaly_severity = "HIGH"

        elif anomaly_rate >= 0.10:
            anomaly_severity = "MEDIUM"

        else:
            anomaly_severity = "LOW"

        # ==========================================
        # 4. SENSOR DEGRADATION
        # ==========================================

        sensor_result = analyze_sensor_trends(
            engine_id
        )

        critical_sensor_count = sum(
            1
            for sensor in sensor_result["sensors"]
            if sensor["severity"] == "CRITICAL"
        )

        high_sensor_count = sum(
            1
            for sensor in sensor_result["sensors"]
            if sensor["severity"] == "HIGH"
        )

        # ==========================================
        # 5. MAINTENANCE DECISION
        # ==========================================

        maintenance_decision = (
            calculate_maintenance_decision(
                rul=prediction.rul,
                risk_level=prediction.risk_level,
                anomaly_rate=anomaly_rate,
                anomaly_severity=anomaly_severity,
                critical_sensor_count=critical_sensor_count,
                high_sensor_count=high_sensor_count,
            )
        )

        # ==========================================
        # 6. EXPLAINABILITY
        # ==========================================

        explanation = (
            explain_maintenance_decision(
                rul=prediction.rul,
                risk_level=prediction.risk_level,
                anomaly_rate=anomaly_rate,
                anomaly_severity=anomaly_severity,
                critical_sensor_count=critical_sensor_count,
                high_sensor_count=high_sensor_count,
                sensor_data=sensor_result["sensors"],
            )
        )

        # ==========================================
        # 7. KNOWLEDGE RETRIEVAL
        # ==========================================

        knowledge = (
            build_maintenance_guidance_response(
                engine_id=engine_id,
                risk_level=prediction.risk_level,
                rul=prediction.rul,
                anomaly_rate=anomaly_rate,
                critical_sensor_count=critical_sensor_count,
                high_sensor_count=high_sensor_count,
                sensor_data=sensor_result["sensors"],
                top_k=5,
            )
        )

        # ==========================================
        # 8. UNIFIED RESPONSE
        # ==========================================

        return {
            "engine_id": prediction.engine_id,
            "machine_id": f"UNIT-{engine_id:03d}",

            "prediction": {
                "rul": prediction.rul,
                "health_score": prediction.health_score,
                "risk_level": prediction.risk_level,
                "recommendation": prediction.recommendation,
            },

            "anomaly": {
                "anomaly_rate": anomaly_rate,
                "severity": anomaly_severity,
            },

            "sensor_health": {
                "critical_sensor_count": critical_sensor_count,
                "high_sensor_count": high_sensor_count,
                "sensors": sensor_result["sensors"],
            },

            "maintenance_decision": {
                "maintenance_score": maintenance_decision[
                    "maintenance_score"
                ],
                "priority": maintenance_decision[
                    "priority"
                ],
                "action": maintenance_decision[
                    "action"
                ],
            },

            "explainability": explanation,

            "knowledge": knowledge,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{type(error).__name__}: {error}",
        )

