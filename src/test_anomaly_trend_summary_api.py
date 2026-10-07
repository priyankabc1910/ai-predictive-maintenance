import json
from urllib.request import urlopen


API_URL = "http://127.0.0.1:8000/anomaly/fleet/trends"


def test_anomaly_trend_summary_api():
    with urlopen(API_URL, timeout=30) as response:
        assert response.status == 200
        data = json.loads(
            response.read().decode("utf-8")
        )

    assert "total_engines" in data
    assert "increasing_engines" in data
    assert "decreasing_engines" in data
    assert "stable_engines" in data
    assert "worsening_rate" in data
    assert "average_rate_change" in data
    assert "maximum_rate_change" in data
    assert "engines" in data

    assert (
        data["increasing_engines"]
        + data["decreasing_engines"]
        + data["stable_engines"]
        == data["total_engines"]
    )

    assert 0 <= data["worsening_rate"] <= 1

    assert len(data["engines"]) == data["total_engines"]

    for engine in data["engines"]:
        assert engine["trend"] in {
            "INCREASING",
            "DECREASING",
            "STABLE",
        }

        assert 0 <= engine["previous_anomaly_rate"] <= 1
        assert 0 <= engine["current_anomaly_rate"] <= 1


if __name__ == "__main__":
    test_anomaly_trend_summary_api()
    print("Anomaly trend summary API test passed.")