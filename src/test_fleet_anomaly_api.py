import json
from urllib.request import urlopen


API_URL = "http://127.0.0.1:8000/anomaly/fleet/summary"


def test_fleet_anomaly_api():
    with urlopen(API_URL, timeout=30) as response:
        assert response.status == 200

        data = json.loads(
            response.read().decode("utf-8")
        )

    assert data["total_engines"] == 100

    assert "anomalous_engines" in data
    assert "fleet_anomaly_rate" in data
    assert "severity_counts" in data
    assert "ranked_engines" in data

    assert len(data["ranked_engines"]) == 100

    ranks = [
        item["anomaly_rank"]
        for item in data["ranked_engines"]
    ]

    assert ranks == list(range(1, 101))

    for item in data["ranked_engines"]:
        assert "engine_id" in item
        assert "machine_id" in item
        assert "anomaly_rate" in item
        assert "anomaly_score" in item
        assert "anomaly_rank" in item
        assert "severity" in item

        assert 0 <= item["anomaly_rate"] <= 1
        assert 0 <= item["anomaly_score"] <= 100
        assert 1 <= item["anomaly_rank"] <= 100


if __name__ == "__main__":
    test_fleet_anomaly_api()
    print("Fleet anomaly API test passed for 100 engines.")