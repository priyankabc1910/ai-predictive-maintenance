from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "train_FD001.txt"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "anomaly_model_FD001.pkl"
)

SCALER_PATH = (
    BASE_DIR
    / "models"
    / "anomaly_scaler_FD001.pkl"
)

FEATURES_PATH = (
    BASE_DIR
    / "models"
    / "anomaly_features_FD001.pkl"
)


COLUMN_NAMES = [
    "unit_id",
    "cycle",
    "op_setting_1",
    "op_setting_2",
    "op_setting_3",
] + [f"sensor_{i}" for i in range(1, 22)]


SENSOR_COLUMNS = [
    f"sensor_{i}"
    for i in range(1, 22)
]

BASELINE_CYCLES = 30


def load_data():
    """Load NASA C-MAPSS FD001 training data."""

    df = pd.read_csv(
        RAW_DATA_PATH,
        sep=r"\s+",
        header=None,
        names=COLUMN_NAMES,
    )

    return df


def build_healthy_baseline(df):
    """
    Build a baseline dataset using the first 30 cycles
    of every engine.

    These early-life observations are used as the
    reference for normal operating behaviour.
    """

    baseline = (
        df.sort_values(["unit_id", "cycle"])
        .groupby("unit_id", group_keys=False)
        .head(BASELINE_CYCLES)
        .copy()
    )

    return baseline


def train_anomaly_model():

    print("Loading C-MAPSS FD001 data...")
    df = load_data()

    print(f"Total observations: {len(df):,}")
    print(f"Total engines: {df['unit_id'].nunique()}")

    baseline = build_healthy_baseline(df)

    print(
        f"Baseline observations: {len(baseline):,}"
    )

    features = baseline[SENSOR_COLUMNS]

    print(
        f"Training features: {len(SENSOR_COLUMNS)} sensors"
    )

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(features)

    model = IsolationForest(
        n_estimators=300,
        contamination=0.05,
        random_state=42,
        n_jobs=-1,
    )

    print("Training Isolation Forest...")

    model.fit(X_scaled)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(SENSOR_COLUMNS, FEATURES_PATH)

    print()
    print("Anomaly model training complete.")
    print(f"Model saved:  {MODEL_PATH}")
    print(f"Scaler saved: {SCALER_PATH}")
    print(f"Features saved: {FEATURES_PATH}")

    return model, scaler


if __name__ == "__main__":
    train_anomaly_model()