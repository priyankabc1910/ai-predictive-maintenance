from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import joblib
import pandas as pd
import tensorflow as tf

from src.predictor import predict_engine
from .schemas import PredictionResponse

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "train_FD001.txt"
MODEL_PATH = BASE_DIR / "models" / "lstm_rul_model_FD001.keras"
SCALER_PATH = BASE_DIR / "models" / "lstm_scaler_FD001.pkl"


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
# Load model and data
# --------------------------------------------------

model = tf.keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

COLUMN_NAMES = [
    "unit_id",
    "cycle",
    "op_setting_1",
    "op_setting_2",
    "op_setting_3",
] + [f"sensor_{i}" for i in range(1, 22)]

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
    }


# --------------------------------------------------
# RUL prediction
# --------------------------------------------------

@app.get(
    "/predict/{engine_id}",
    response_model=PredictionResponse
)
def predict(engine_id: int):

    engine_data = raw_df[
        raw_df["unit_id"] == engine_id
    ].copy()

    if engine_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Engine {engine_id} not found."
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
            detail=str(error)
        )
    
@app.get(
    "/fleet",
    response_model=list[PredictionResponse]
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
                    "machine_id": f"UNIT-{int(engine_id):03d}",
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

@app.get("/fleet/summary")
def fleet_summary():
    predictions = predict_fleet()

    total_machines = len(predictions)
    critical = sum(
        1 for p in predictions if p["risk_level"] == "CRITICAL"
    )
    high = sum(
        1 for p in predictions if p["risk_level"] == "HIGH"
    )
    medium = sum(
        1 for p in predictions if p["risk_level"] == "MEDIUM"
    )
    low = sum(
        1 for p in predictions if p["risk_level"] == "LOW"
    )

    average_health = (
        sum(p["health_score"] for p in predictions) / total_machines
        if total_machines
        else 0
    )

    average_rul = (
        sum(p["rul"] for p in predictions) / total_machines
        if total_machines
        else 0
    )

    return {
        "total_machines": total_machines,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "average_health_score": round(average_health, 2),
        "average_rul": round(average_rul, 2),
    }
