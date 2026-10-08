from typing import Dict, List

from .rul_drivers import rank_rul_drivers


def explain_maintenance_decision(
    rul: float,
    risk_level: str,
    anomaly_rate: float,
    anomaly_severity: str,
    critical_sensor_count: int,
    high_sensor_count: int,
    sensor_data: List[Dict],
) -> Dict:

    reasons = []
    evidence = []

    # RUL evidence
    if rul <= 20:
        reasons.append(
            f"Predicted RUL is critically low at {rul:.2f} cycles."
        )

        evidence.append({
            "factor": "Remaining Useful Life",
            "value": round(rul, 2),
            "severity": "CRITICAL",
            "explanation": (
                "The engine is approaching the predicted "
                "end of its useful operating life."
            ),
        })

    elif rul <= 50:
        reasons.append(
            f"Predicted RUL is low at {rul:.2f} cycles."
        )

        evidence.append({
            "factor": "Remaining Useful Life",
            "value": round(rul, 2),
            "severity": "HIGH",
            "explanation": (
                "The engine has limited remaining useful life."
            ),
        })

    # Anomaly evidence
    if anomaly_rate >= 0.75:
        reasons.append(
            f"{anomaly_rate * 100:.1f}% of the latest telemetry "
            "window was classified as anomalous."
        )

        evidence.append({
            "factor": "Anomaly Detection",
            "value": round(anomaly_rate * 100, 1),
            "unit": "%",
            "severity": anomaly_severity,
            "explanation": (
                "Telemetry is strongly deviating from "
                "the learned healthy baseline."
            ),
        })

    elif anomaly_rate >= 0.25:
        reasons.append(
            f"{anomaly_rate * 100:.1f}% of the latest telemetry "
            "window was classified as anomalous."
        )

        evidence.append({
            "factor": "Anomaly Detection",
            "value": round(anomaly_rate * 100, 1),
            "unit": "%",
            "severity": anomaly_severity,
            "explanation": (
                "A significant portion of recent telemetry "
                "differs from the learned healthy baseline."
            ),
        })

    # Sensor degradation evidence
    if critical_sensor_count > 0:
        reasons.append(
            f"{critical_sensor_count} monitored sensors show "
            "critical deviation from their healthy baseline."
        )

    if high_sensor_count > 0:
        reasons.append(
            f"{high_sensor_count} monitored sensors show "
            "high deviation from their healthy baseline."
        )

    evidence.append({
        "factor": "Sensor Degradation",
        "value": critical_sensor_count,
        "unit": "critical sensors",
        "severity": (
            "CRITICAL"
            if critical_sensor_count > 0
            else "LOW"
        ),
        "explanation": (
            "Sensor behaviour is being compared against "
            "the engine's healthy operating baseline."
        ),
    })

    # Top sensor contributors
    sorted_sensors = sorted(
        sensor_data,
        key=lambda sensor: abs(
            sensor.get("deviation_score", 0)
        ),
        reverse=True,
    )

    top_sensors = []

    for sensor in sorted_sensors[:5]:
        top_sensors.append({
            "sensor": sensor["sensor"],
            "deviation_score": round(
                sensor["deviation_score"],
                3,
            ),
            "trend_slope": round(
                sensor["trend_slope"],
                5,
            ),
            "trend_direction": sensor["trend_direction"],
            "severity": sensor["severity"],
        })

    # Overall explanation
    if reasons:
        summary = (
            f"Engine condition is classified as {risk_level}. "
            + " ".join(reasons)
        )
    else:
        summary = (
            "No major maintenance risk factors were detected "
            "from the available model outputs."
        )

    return {
        "risk_level": risk_level,
        "summary": summary,
        "reasons": reasons,
        "evidence": evidence,
        "top_sensor_contributors": top_sensors,
    }


def summarize_rul_drivers(
    sensor_contributions: List[Dict],
) -> Dict:
    """
    Summarize the strongest sensor drivers affecting
    the RUL prediction.
    """

    ranked_drivers = rank_rul_drivers(
        sensor_contributions
    )

    positive_drivers = [
        driver
        for driver in ranked_drivers
        if driver["direction"] == "POSITIVE"
    ]

    negative_drivers = [
        driver
        for driver in ranked_drivers
        if driver["direction"] == "NEGATIVE"
    ]

    neutral_drivers = [
        driver
        for driver in ranked_drivers
        if driver["direction"] == "NEUTRAL"
    ]

    return {
        "driver_count": len(ranked_drivers),
        "positive_driver_count": len(positive_drivers),
        "negative_driver_count": len(negative_drivers),
        "neutral_driver_count": len(neutral_drivers),
        "top_driver": (
            ranked_drivers[0]
            if ranked_drivers
            else None
        ),
        "drivers": ranked_drivers,
    }