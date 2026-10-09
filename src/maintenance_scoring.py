
from typing import Dict


def calculate_maintenance_decision(
    rul: float,
    risk_level: str,
    anomaly_rate: float,
    anomaly_severity: str,
    critical_sensor_count: int,
    high_sensor_count: int,
) -> Dict:
    if rul < 0:
        raise ValueError("RUL cannot be negative.")
    if not 0 <= anomaly_rate <= 1:
        raise ValueError("Anomaly rate must be between 0 and 1.")
    if critical_sensor_count < 0 or high_sensor_count < 0:
        raise ValueError("Sensor counts cannot be negative.")

    score = 0.0

    if rul <= 20:
        score += 40
    elif rul <= 50:
        score += 30
    elif rul <= 100:
        score += 15

    score += anomaly_rate * 30
    score += min(critical_sensor_count, 5) * 4
    score += min(high_sensor_count, 5) * 2

    if risk_level.upper() == "CRITICAL":
        score += 10
    elif risk_level.upper() == "HIGH":
        score += 7
    elif risk_level.upper() == "MEDIUM":
        score += 3

    if anomaly_severity.upper() == "CRITICAL":
        score += 10
    elif anomaly_severity.upper() == "HIGH":
        score += 6
    elif anomaly_severity.upper() == "MEDIUM":
        score += 3

    score = round(min(score, 100.0), 2)

    if score >= 75:
        priority = "IMMEDIATE"
        action = "Inspect the engine immediately and assess maintenance requirements."
    elif score >= 50:
        priority = "URGENT"
        action = "Schedule maintenance as soon as possible."
    elif score >= 25:
        priority = "PLANNED"
        action = "Plan preventive maintenance and monitor sensor trends."
    else:
        priority = "ROUTINE"
        action = "Continue routine monitoring and scheduled maintenance."

    return {
        "maintenance_score": score,
        "priority": priority,
        "action": action,
    }
