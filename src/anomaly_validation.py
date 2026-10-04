from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "train_FD001.txt"
MODEL_PATH = BASE_DIR / "models" / "anomaly_model_FD001.pkl"
SCALER_PATH = BASE_DIR / "models" / "anomaly_scaler_FD001.pkl"
FEATURES_PATH = BASE_DIR / "models" / "anomaly_features_FD001.pkl"


COLUMN_NAMES = [
    "unit_id",
    "cycle",
    "op_setting_1",
    "op_setting_2",
    "op_setting_3",
] + [f"sensor_{i}" for i in range(1, 22)]


def load_data():
    return pd.read_csv(
        RAW_DATA_PATH,
        sep=r"\s+",
        header=None,
        names=COLUMN_NAMES,
    )


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    features = joblib.load(FEATURES_PATH)

    return model, scaler, features


def evaluate_window(
    engine_data,
    start_cycle,
    end_cycle,
    model,
    scaler,
    features,
):
    window = engine_data[
        (engine_data["cycle"] >= start_cycle)
        & (engine_data["cycle"] <= end_cycle)
    ]

    if window.empty:
        return None

    X = window[features]
    X_scaled = scaler.transform(X)

    predictions = model.predict(X_scaled)
    scores = model.decision_function(X_scaled)

    anomaly_count = int((predictions == -1).sum())
    anomaly_rate = anomaly_count / len(predictions)

    return {
        "start": int(window["cycle"].iloc[0]),
        "end": int(window["cycle"].iloc[-1]),
        "samples": len(window),
        "anomalies": anomaly_count,
        "rate": anomaly_rate,
        "mean_score": float(scores.mean()),
    }


if __name__ == "__main__":

    ENGINE_ID = 1

    df = load_data()

    engine = (
        df[df["unit_id"] == ENGINE_ID]
        .sort_values("cycle")
    )

    model, scaler, features = load_artifacts()

    max_cycle = int(engine["cycle"].max())

    windows = [
        ("EARLY", 1, 30),
        ("EARLY-MID", 31, 60),
        ("MID", 61, 90),
        ("MID-LATE", 91, 120),
        ("LATE", max(121, max_cycle - 59), max_cycle - 30),
        ("FINAL", max_cycle - 29, max_cycle),
    ]

    print("=" * 72)
    print(f"ANOMALY LIFECYCLE VALIDATION — ENGINE {ENGINE_ID}")
    print("=" * 72)

    for label, start, end in windows:

        result = evaluate_window(
            engine,
            start,
            end,
            model,
            scaler,
            features,
        )

        if result is None:
            continue

        print()
        print(f"{label}")
        print(
            f"Cycles:             "
            f"{result['start']} → {result['end']}"
        )
        print(f"Samples:             {result['samples']}")
        print(f"Anomalous samples:   {result['anomalies']}")
        print(f"Anomaly rate:        {result['rate']:.1%}")
        print(f"Mean model score:    {result['mean_score']:.4f}")

    print()
    print("=" * 72)
    print("VALIDATION COMPLETE")
    print("=" * 72)