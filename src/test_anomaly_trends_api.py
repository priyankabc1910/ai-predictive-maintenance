import json
from urllib.request import urlopen


API_URL = "http://127.0.0.1:8000/anomaly/fleet/trends"


def test_anomaly_trends_api():
    with urlopen(API_URL, timeout=30) as response:
        assert response.status == 200
        data = json.loads(
            response.read().decode("utf-8")
        )

    assert "total_engines" in data
    assert "engines" in data

    assert data["total_engines"] == len(
        data["engines"]
    )

    assert data["total_engines"] > 0

    for item in data["engines"]:
        assert "engine_id" in item
        assert "machine_id" in item
        assert "previous_anomaly_rate" in item
        assert "current_anomaly_rate" in item
        assert "rate_change" in item
        assert "trend" in item

        assert 0 <= item["previous_anomaly_rate"] <= 1
        assert 0 <= item["current_anomaly_rate"] <= 1

        assert item["trend"] in {
            "INCREASING",
            "DECREASING",
            "STABLE",
        }


if __name__ == "__main__":
    test_anomaly_trends_api()
    print("Anomaly trends API test passed.")