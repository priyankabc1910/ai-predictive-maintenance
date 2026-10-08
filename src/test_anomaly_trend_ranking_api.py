import json
from urllib.request import urlopen


API_URL = "http://127.0.0.1:8000/anomaly/fleet/trends"


def test_anomaly_trend_ranking_api():
    with urlopen(API_URL, timeout=30) as response:
        assert response.status == 200
        data = json.loads(
            response.read().decode("utf-8")
        )

    engines = data["engines"]

    assert len(engines) == data["total_engines"]

    ranks = [
        engine["trend_rank"]
        for engine in engines
    ]

    assert ranks == list(
        range(1, data["total_engines"] + 1)
    )

    for engine in engines:
        assert "trend_rank" in engine
        assert "trend_score" in engine

        assert (
            1
            <= engine["trend_rank"]
            <= data["total_engines"]
        )

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
    test_anomaly_trend_ranking_api()
    print("Anomaly trend ranking API test passed.")