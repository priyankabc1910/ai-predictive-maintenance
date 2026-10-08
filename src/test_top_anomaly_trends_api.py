import json
from urllib.request import urlopen


API_URL = "http://127.0.0.1:8000/anomaly/fleet/top"


def test_top_anomaly_trends_api():
    with urlopen(API_URL, timeout=30) as response:
        assert response.status == 200
        data = json.loads(
            response.read().decode("utf-8")
        )

    assert "requested_limit" in data
    assert "returned_engines" in data
    assert "engines" in data

    assert data["requested_limit"] == 10
    assert data["returned_engines"] == 10

    engines = data["engines"]

    assert len(engines) == 10

    for engine in engines:
        assert "engine_id" in engine
        assert "machine_id" in engine
        assert "rate_change" in engine
        assert "trend" in engine
        assert "trend_rank" in engine
        assert "trend_score" in engine

        assert engine["trend_rank"] >= 1
        assert engine["trend_score"] >= 0

    for previous, current in zip(
        engines,
        engines[1:],
    ):
        assert (
            previous["rate_change"],
            previous["current_anomaly_rate"],
        ) >= (
            current["rate_change"],
            current["current_anomaly_rate"],
        )


if __name__ == "__main__":
    test_top_anomaly_trends_api()
    print("Top anomaly trends API test passed.")