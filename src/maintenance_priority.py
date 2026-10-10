
from typing import Dict


def explain_maintenance_priority(
    maintenance_score: float,
    rul: float,
    anomaly_rate: float,
    critical_sensor_count: int,
    high_sensor_count: int,
) -> Dict:
    if not 0 <= maintenance_score <= 100:
        raise ValueError("Maintenance score must be between 0 and 100.")
    if rul < 0:
        raise ValueError("RUL cannot be negative.")
    if not 0 <= anomaly_rate <= 1:
        raise ValueError("Anomaly rate must be between 0 and 1.")
    if critical_sensor_count < 0 or high_sensor_count < 0:
        raise ValueError("Sensor counts cannot be negative.")

    reasons = []

    if rul <= 20:
        reasons.append("Predicted remaining useful life is critically low.")
    elif rul <= 50:
        reasons.append("Predicted remaining useful life is low.")

    if anomaly_rate >= 0.50:
        reasons.append("Recent telemetry has a critical anomaly rate.")
    elif anomaly_rate >= 0.25:
        reasons.append("Recent telemetry has a high anomaly rate.")

    if critical_sensor_count:
        reasons.append(
            f"{critical_sensor_count} sensor(s) show critical deviation."
        )
    if high_sensor_count:
        reasons.append(
            f"{high_sensor_count} sensor(s) show high deviation."
        )

    if maintenance_score >= 75:
        priority = "IMMEDIATE"
    elif maintenance_score >= 50:
        priority = "URGENT"
    elif maintenance_score >= 25:
        priority = "PLANNED"
    else:
        priority = "ROUTINE"

    if not reasons:
        reasons.append("No major risk indicators were supplied.")

    return {
        "maintenance_score": round(maintenance_score, 2),
        "priority": priority,
        "reason_count": len(reasons),
        "reasons": reasons,
    }
