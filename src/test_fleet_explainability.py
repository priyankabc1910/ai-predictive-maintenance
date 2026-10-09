
from src.fleet_explainability import summarize_fleet_explainability


def test_fleet_explainability_ranks_critical_engines_first():
    engines = [
        {"engine_id": 1, "risk_level": "LOW", "maintenance_score": 20},
        {"engine_id": 2, "risk_level": "CRITICAL", "maintenance_score": 80},
        {"engine_id": 3, "risk_level": "HIGH", "maintenance_score": 60},
    ]

    result = summarize_fleet_explainability(engines)

    assert result["total_engines"] == 3
    assert result["ranked_engines"][0]["engine_id"] == 2
    assert result["ranked_engines"][1]["engine_id"] == 3
    assert result["severity_counts"]["CRITICAL"] == 1


def test_empty_fleet_explainability():
    result = summarize_fleet_explainability([])

    assert result["total_engines"] == 0
    assert result["ranked_engines"] == []
    assert result["severity_counts"]["CRITICAL"] == 0


def test_equal_severity_uses_maintenance_score():
    engines = [
        {"engine_id": 1, "risk_level": "HIGH", "maintenance_score": 50},
        {"engine_id": 2, "risk_level": "HIGH", "maintenance_score": 90},
    ]

    result = summarize_fleet_explainability(engines)

    assert result["ranked_engines"][0]["engine_id"] == 2
