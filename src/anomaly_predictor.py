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


def load_raw_data():
    return pd.read_csv(
        RAW_DATA_PATH,
        sep=r"\s+",
        header=None,
        names=COLUMN_NAMES,
    )


def load_anomaly_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_columns = joblib.load(FEATURES_PATH)

    return model, scaler, feature_columns


def score_engine(engine_id: int, window_size: int = 30):
    df = load_raw_data()

    engine_data = (
        df[df["unit_id"] == engine_id]
        .sort_values("cycle")
    )

    if engine_data.empty:
        raise ValueError(f"Engine {engine_id} not found.")

    if len(engine_data) < window_size:
        raise ValueError(
            f"Engine {engine_id} has fewer than "
            f"{window_size} cycles."
        )

    model, scaler, feature_columns = load_anomaly_artifacts()

    latest_window = engine_data.tail(window_size)

    features = latest_window[feature_columns]

    scaled_features = scaler.transform(features)

    predictions = model.predict(scaled_features)
    decision_scores = model.decision_function(scaled_features)

    anomaly_count = int((predictions == -1).sum())
    anomaly_rate = anomaly_count / len(predictions)

    mean_decision_score = float(decision_scores.mean())
    minimum_decision_score = float(decision_scores.min())

    if anomaly_rate >= 0.50:
        severity = "CRITICAL"
    elif anomaly_rate >= 0.25:
        severity = "HIGH"
    elif anomaly_rate >= 0.10:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "engine_id": int(engine_id),
        "cycles_analyzed": window_size,
        "latest_cycle": int(latest_window["cycle"].iloc[-1]),
        "anomalous_cycles": anomaly_count,
        "anomaly_rate": round(anomaly_rate, 3),
        "mean_decision_score": round(mean_decision_score, 4),
        "minimum_decision_score": round(
            minimum_decision_score, 4
        ),
        "severity": severity,
    }


if __name__ == "__main__":

    test_engines = [1, 24, 67, 83, 91]

    print("=" * 60)
    print("REAL-TIME ANOMALY DETECTION TEST")
    print("=" * 60)

    for engine_id in test_engines:

        result = score_engine(engine_id)

        print()
        print(f"Engine:             {result['engine_id']}")
        print(f"Latest cycle:       {result['latest_cycle']}")
        print(f"Cycles analyzed:    {result['cycles_analyzed']}")
        print(f"Anomalous cycles:   {result['anomalous_cycles']}")
        print(f"Anomaly rate:       {result['anomaly_rate']:.1%}")
        print(f"Mean model score:   {result['mean_decision_score']}")
        print(f"Minimum score:      {result['minimum_decision_score']}")
        print(f"Severity:           {result['severity']}")

    print()
    print("=" * 60)
    print("ANOMALY DETECTION TEST COMPLETE")
    print("=" * 60)