from anomaly_trends import (
    calculate_anomaly_rate,
    classify_anomaly_trend,
    analyze_anomaly_trend,
    summarize_fleet_anomaly_trends,
    rank_anomaly_trends,
    get_top_anomaly_trends,
)


def test_anomaly_rate():
    predictions = [-1, -1, 1, 1, 1]

    rate = calculate_anomaly_rate(
        predictions
    )

    assert rate == 0.4


def test_anomaly_trend_classification():
    assert (
        classify_anomaly_trend(
            0.10,
            0.30,
        )
        == "INCREASING"
    )

    assert (
        classify_anomaly_trend(
            0.30,
            0.10,
        )
        == "DECREASING"
    )

    assert (
        classify_anomaly_trend(
            0.20,
            0.25,
        )
        == "STABLE"
    )


def test_anomaly_trend_analysis():
    previous = [
        -1,
        1,
        1,
        1,
        1,
    ]

    current = [
        -1,
        -1,
        -1,
        1,
        1,
    ]

    result = analyze_anomaly_trend(
        previous_predictions=previous,
        current_predictions=current,
    )

    assert result["previous_anomaly_rate"] == 0.2
    assert result["current_anomaly_rate"] == 0.6
    assert result["rate_change"] == 0.4
    assert result["trend"] == "INCREASING"


def test_fleet_anomaly_trend_summary():
    trends = [
        {
            "engine_id": 1,
            "trend": "INCREASING",
            "rate_change": 0.40,
        },
        {
            "engine_id": 2,
            "trend": "INCREASING",
            "rate_change": 0.20,
        },
        {
            "engine_id": 3,
            "trend": "DECREASING",
            "rate_change": -0.20,
        },
        {
            "engine_id": 4,
            "trend": "STABLE",
            "rate_change": 0.03,
        },
    ]

    result = summarize_fleet_anomaly_trends(
        trends
    )

    assert result["total_engines"] == 4
    assert result["increasing_engines"] == 2
    assert result["decreasing_engines"] == 1
    assert result["stable_engines"] == 1
    assert result["worsening_rate"] == 0.5
    assert result["average_rate_change"] == 0.1075
    assert result["maximum_rate_change"] == 0.40


def test_anomaly_trend_ranking():
    trends = [
        {
            "engine_id": 1,
            "machine_id": "UNIT-001",
            "current_anomaly_rate": 0.40,
            "rate_change": 0.20,
            "trend": "INCREASING",
        },
        {
            "engine_id": 2,
            "machine_id": "UNIT-002",
            "current_anomaly_rate": 0.60,
            "rate_change": 0.40,
            "trend": "INCREASING",
        },
        {
            "engine_id": 3,
            "machine_id": "UNIT-003",
            "current_anomaly_rate": 0.10,
            "rate_change": 0.00,
            "trend": "STABLE",
        },
    ]

    result = rank_anomaly_trends(
        trends
    )

    assert result[0]["engine_id"] == 2
    assert result[0]["trend_rank"] == 1
    assert result[0]["trend_score"] == 40.0

    assert result[1]["engine_id"] == 1
    assert result[1]["trend_rank"] == 2
    assert result[1]["trend_score"] == 20.0

    assert result[2]["engine_id"] == 3
    assert result[2]["trend_rank"] == 3
    assert result[2]["trend_score"] == 0.0


def test_top_anomaly_trends():
    trends = [
        {
            "engine_id": 1,
            "machine_id": "UNIT-001",
            "current_anomaly_rate": 0.30,
            "rate_change": 0.10,
            "trend": "INCREASING",
        },
        {
            "engine_id": 2,
            "machine_id": "UNIT-002",
            "current_anomaly_rate": 0.70,
            "rate_change": 0.50,
            "trend": "INCREASING",
        },
        {
            "engine_id": 3,
            "machine_id": "UNIT-003",
            "current_anomaly_rate": 0.40,
            "rate_change": 0.20,
            "trend": "INCREASING",
        },
    ]

    result = get_top_anomaly_trends(
        trends,
        limit=2,
    )

    assert len(result) == 2
    assert result[0]["engine_id"] == 2
    assert result[1]["engine_id"] == 3
    assert result[0]["trend_rank"] == 1
    assert result[1]["trend_rank"] == 2


if __name__ == "__main__":
    test_anomaly_rate()
    test_anomaly_trend_classification()
    test_anomaly_trend_analysis()
    test_fleet_anomaly_trend_summary()
    test_anomaly_trend_ranking()
    test_top_anomaly_trends()

    print("Anomaly trend analysis tests passed.")