from .preprocessing import prepare_lstm_sequence
from .schemas import PredictionResult


def classify_risk(rul):
    if rul <= 20:
        return "CRITICAL"
    elif rul <= 50:
        return "HIGH"
    elif rul <= 100:
        return "MEDIUM"
    else:
        return "LOW"


def calculate_health_score(rul, max_rul=125):
    score = (rul / max_rul) * 100
    return max(0, min(100, score))


def generate_recommendation(risk_level):
    recommendations = {
        "CRITICAL": "Immediate inspection and maintenance required.",
        "HIGH": "Schedule maintenance at the earliest opportunity.",
        "MEDIUM": "Monitor machine condition and plan preventive maintenance.",
        "LOW": "Continue normal operation and routine monitoring.",
    }

    return recommendations[risk_level]


def predict_engine(
    engine_data,
    engine_id,
    model,
    scaler,
    sensor_columns,
    window_size=30
):
    sequence = prepare_lstm_sequence(
        engine_data=engine_data,
        sensor_columns=sensor_columns,
        scaler=scaler,
        window_size=window_size
    )

    prediction = model.predict(
        sequence,
        verbose=0
    )

    rul = float(prediction[0][0])

    risk_level = classify_risk(rul)
    health_score = calculate_health_score(rul)
    recommendation = generate_recommendation(risk_level)

    return PredictionResult(
        engine_id=int(engine_id),
        rul=round(rul, 2),
        health_score=round(health_score, 2),
        risk_level=risk_level,
        recommendation=recommendation
    )