from fleet_anomaly import (
    aggregate_fleet_anomalies,
    classify_fleet_anomaly_rate,
)


def test_anomaly_severity():
    assert classify_fleet_anomaly_rate(0.60) == "CRITICAL"
    assert classify_fleet_anomaly_rate(0.30) == "HIGH"
    assert classify_fleet_anomaly_rate(0.15) == "MEDIUM"
    assert classify_fleet_anomaly_rate(0.05) == "LOW"


def test_fleet_anomaly_aggregation():
    engines = [
        {
            "engine_id": 1,
            "machine_id": "UNIT-001",
            "anomaly_rate": 0.60,
            "severity": "CRITICAL",
        },
        {
            "engine_id": 2,
            "machine_id": "UNIT-002",
            "anomaly_rate": 0.30,
            "severity": "HIGH",
        },
        {
            "engine_id": 3,
            "machine_id": "UNIT-003",
            "anomaly_rate": 0.05,
            "severity": "LOW",
        },
    ]

    result = aggregate_fleet_anomalies(engines)

    assert result["total_engines"] == 3
    assert result["anomalous_engines"] == 3

    assert result["severity_counts"]["CRITICAL"] == 1
    assert result["severity_counts"]["HIGH"] == 1
    assert result["severity_counts"]["LOW"] == 1

    assert result["ranked_engines"][0]["machine_id"] == "UNIT-001"

    assert result["ranked_engines"][0]["anomaly_rank"] == 1
    assert result["ranked_engines"][0]["anomaly_score"] == 60.0

    assert result["ranked_engines"][1]["anomaly_rank"] == 2
    assert result["ranked_engines"][1]["anomaly_score"] == 30.0

    assert result["ranked_engines"][2]["anomaly_rank"] == 3
    assert result["ranked_engines"][2]["anomaly_score"] == 5.0


if __name__ == "__main__":
    test_anomaly_severity()
    test_fleet_anomaly_aggregation()

    print("Fleet anomaly aggregation tests passed.")