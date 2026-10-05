from typing import Dict


def calculate_maintenance_decision(
    rul: float,
    risk_level: str,
    anomaly_rate: float,
    anomaly_severity: str,
    critical_sensor_count: int,
    high_sensor_count: int,
) -> Dict:
    """
    Combine RUL, anomaly detection, and sensor degradation signals
    into a maintenance priority and recommended action.
    """

    score = 0

    # RUL contribution
    if rul <= 20:
        score += 40
    elif rul <= 50:
        score += 30
    elif rul <= 100:
        score += 15

    # RUL risk level
    risk_points = {
        "CRITICAL": 25,
        "HIGH": 18,
        "MEDIUM": 10,
        "LOW": 0,
    }
    score += risk_points.get(risk_level.upper(), 0)

    # Anomaly contribution
    if anomaly_rate >= 0.75:
        score += 20
    elif anomaly_rate >= 0.50:
        score += 15
    elif anomaly_rate >= 0.25:
        score += 8

    # Anomaly severity
    anomaly_points = {
        "CRITICAL": 10,
        "HIGH": 7,
        "MEDIUM": 4,
        "LOW": 0,
        "NORMAL": 0,
    }
    score += anomaly_points.get(anomaly_severity.upper(), 0)

    # Sensor degradation contribution
    score += min(critical_sensor_count * 2, 10)
    score += min(high_sensor_count, 5)

    score = min(score, 100)

    # Final maintenance priority
    if score >= 75:
        priority = "IMMEDIATE"
        action = "Inspect engine immediately and schedule maintenance before continued operation."
    elif score >= 50:
        priority = "URGENT"
        action = "Schedule maintenance at the earliest available opportunity."
    elif score >= 25:
        priority = "PLANNED"
        action = "Plan preventive maintenance and continue condition monitoring."
    else:
        priority = "ROUTINE"
        action = "Continue normal operation with routine condition monitoring."

    return {
        "maintenance_score": score,
        "priority": priority,
        "action": action,
    }