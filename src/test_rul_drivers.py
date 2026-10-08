from src.rul_drivers import (
    rank_rul_drivers,
    get_top_rul_drivers,
)


def test_rank_rul_drivers():
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

    ranked = rank_rul_drivers(
        sensor_contributions
    )

    assert len(ranked) == 4

    assert ranked[0]["sensor"] == "sensor_11"
    assert ranked[0]["direction"] == "NEGATIVE"

    assert ranked[1]["sensor"] == "sensor_4"
    assert ranked[1]["direction"] == "POSITIVE"

    assert ranked[2]["sensor"] == "sensor_15"
    assert ranked[2]["direction"] == "NEGATIVE"

    assert ranked[3]["sensor"] == "sensor_7"
    assert ranked[3]["direction"] == "NEUTRAL"

    assert ranked[0]["rank"] == 1
    assert ranked[1]["rank"] == 2
    assert ranked[2]["rank"] == 3
    assert ranked[3]["rank"] == 4


def test_get_top_rul_drivers():
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
            "contribution": 0.21,
        },
    ]

    top_drivers = get_top_rul_drivers(
        sensor_contributions,
        limit=2,
    )

    assert len(top_drivers) == 2

    assert top_drivers[0]["sensor"] == "sensor_11"
    assert top_drivers[1]["sensor"] == "sensor_4"


def test_rank_rul_drivers_empty():
    result = rank_rul_drivers([])

    assert result == []


def test_get_top_rul_drivers_invalid_limit():
    try:
        get_top_rul_drivers(
            [],
            limit=0,
        )
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "limit must be greater than zero."


def test_rul_driver_direction():
    sensor_contributions = [
        {
            "sensor": "positive_sensor",
            "contribution": 0.5,
        },
        {
            "sensor": "negative_sensor",
            "contribution": -0.5,
        },
        {
            "sensor": "neutral_sensor",
            "contribution": 0.0,
        },
    ]

    ranked = rank_rul_drivers(
        sensor_contributions
    )

    directions = {
        item["sensor"]: item["direction"]
        for item in ranked
    }

    assert directions["positive_sensor"] == "POSITIVE"
    assert directions["negative_sensor"] == "NEGATIVE"
    assert directions["neutral_sensor"] == "NEUTRAL"


if __name__ == "__main__":
    test_rank_rul_drivers()
    test_get_top_rul_drivers()
    test_rank_rul_drivers_empty()
    test_get_top_rul_drivers_invalid_limit()
    test_rul_driver_direction()

    print("RUL driver tests passed.")