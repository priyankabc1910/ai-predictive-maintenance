from anomaly_trends import (
    calculate_anomaly_rate,
    classify_anomaly_trend,
    analyze_anomaly_trend,
)


def test_anomaly_rate():
    predictions = [-1, -1, 1, 1, 1]

    rate = calculate_anomaly_rate(predictions)

    assert rate == 0.4


def test_anomaly_trend_classification():
    assert (
        classify_anomaly_trend(0.10, 0.30)
        == "INCREASING"
    )

    assert (
        classify_anomaly_trend(0.30, 0.10)
        == "DECREASING"
    )

    assert (
        classify_anomaly_trend(0.20, 0.25)
        == "STABLE"
    )


def test_anomaly_trend_analysis():
    previous = [-1, 1, 1, 1, 1]
    current = [-1, -1, -1, 1, 1]

    result = analyze_anomaly_trend(
        previous_predictions=previous,
        current_predictions=current,
    )

    assert result["previous_anomaly_rate"] == 0.2
    assert result["current_anomaly_rate"] == 0.6
    assert result["rate_change"] == 0.4
    assert result["trend"] == "INCREASING"


if __name__ == "__main__":
    test_anomaly_rate()
    test_anomaly_trend_classification()
    test_anomaly_trend_analysis()

    print("Anomaly trend analysis tests passed.")