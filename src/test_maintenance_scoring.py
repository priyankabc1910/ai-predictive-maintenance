
import pytest

from src.maintenance_scoring import calculate_maintenance_decision


def test_critical_engine_gets_immediate_priority():
    result = calculate_maintenance_decision(
        rul=10,
        risk_level="CRITICAL",
        anomaly_rate=0.8,
        anomaly_severity="CRITICAL",
        critical_sensor_count=3,
        high_sensor_count=1,
    )

    assert result["maintenance_score"] >= 75
    assert result["maintenance_score"] <= 100
    assert result["priority"] == "IMMEDIATE"


def test_healthy_engine_gets_routine_priority():
    result = calculate_maintenance_decision(
        rul=150,
        risk_level="LOW",
        anomaly_rate=0,
        anomaly_severity="LOW",
        critical_sensor_count=0,
        high_sensor_count=0,
    )

    assert result["maintenance_score"] == 0
    assert result["priority"] == "ROUTINE"


def test_invalid_anomaly_rate_is_rejected():
    with pytest.raises(ValueError):
        calculate_maintenance_decision(
            rul=50,
            risk_level="HIGH",
            anomaly_rate=1.5,
            anomaly_severity="HIGH",
            critical_sensor_count=0,
            high_sensor_count=0,
        )
