from src.explainability import summarize_rul_drivers


def test_summarize_rul_drivers():
    sensor_contributions = [
        {
            "sensor": "sensor_11",
            "contribution": -0.82,
        },
        {
            "sensor": "sensor_4",
            "contribution": 0.61,
        },
        {
            "sensor": "sensor_15",
            "contribution": -0.44,
        },
        {
            "sensor": "sensor_7",
            "contribution": 0.0,
        },
    ]

    result = summarize_rul_drivers(
        sensor_contributions
    )

    assert result["driver_count"] == 4
    assert result["positive_driver_count"] == 1
    assert result["negative_driver_count"] == 2
    assert result["neutral_driver_count"] == 1

    assert result["top_driver"] is not None
    assert result["top_driver"]["sensor"] == "sensor_11"
    assert result["top_driver"]["direction"] == "NEGATIVE"

    assert len(result["drivers"]) == 4


def test_summarize_rul_drivers_empty():
    result = summarize_rul_drivers([])

    assert result["driver_count"] == 0
    assert result["positive_driver_count"] == 0
    assert result["negative_driver_count"] == 0
    assert result["neutral_driver_count"] == 0
    assert result["top_driver"] is None
    assert result["drivers"] == []


def test_summarize_rul_drivers_direction_counts():
    sensor_contributions = [
        {
            "sensor": "sensor_a",
            "contribution": 0.5,
        },
        {
            "sensor": "sensor_b",
            "contribution": -0.3,
        },
        {
            "sensor": "sensor_c",
            "contribution": 0.0,
        },
        {
            "sensor": "sensor_d",
            "contribution": 0.2,
        },
    ]

    result = summarize_rul_drivers(
        sensor_contributions
    )

    assert result["positive_driver_count"] == 2
    assert result["negative_driver_count"] == 1
    assert result["neutral_driver_count"] == 1

def test_rul_driver_ranking_handles_tied_contributions():
    sensor_contributions = [
        {"sensor": "sensor_4", "contribution": 0.5},
        {"sensor": "sensor_11", "contribution": -0.5},
    ]

    result = summarize_rul_drivers(sensor_contributions)

    assert result["driver_count"] == 2
    assert result["positive_driver_count"] == 1
    assert result["negative_driver_count"] == 1
    assert result["top_driver"]["absolute_contribution"] == 0.5
    


if __name__ == "__main__":
    test_summarize_rul_drivers()
    test_summarize_rul_drivers_empty()
    test_summarize_rul_drivers_direction_counts()

    print("Explainability tests passed.")