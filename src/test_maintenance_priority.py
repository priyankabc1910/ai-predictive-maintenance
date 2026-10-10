
import pytest

from src.maintenance_priority import explain_maintenance_priority


def test_critical_priority_has_evidence():
    result = explain_maintenance_priority(
        maintenance_score=90,
        rul=10,
        anomaly_rate=0.7,
        critical_sensor_count=2,
        high_sensor_count=1,
    )

    assert result["priority"] == "IMMEDIATE"
    assert result["reason_count"] == 4


def test_healthy_engine_gets_routine_priority():
    result = explain_maintenance_priority(
        maintenance_score=0,
        rul=150,
        anomaly_rate=0,
        critical_sensor_count=0,
        high_sensor_count=0,
    )

    assert result["priority"] == "ROUTINE"
    assert result["reason_count"] == 1


def test_invalid_score_is_rejected():
    with pytest.raises(ValueError):
        explain_maintenance_priority(
            maintenance_score=120,
            rul=10,
            anomaly_rate=0.5,
            critical_sensor_count=0,
            high_sensor_count=0,
        )
