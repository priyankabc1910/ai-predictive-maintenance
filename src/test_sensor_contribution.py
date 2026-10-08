from src.sensor_contribution import (
    rank_sensor_contributions,
    get_top_sensor_contributions,
)


def test_rank_sensor_contributions():
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

    ranked = rank_sensor_contributions(
        sensor_contributions
    )

    assert len(ranked) == 4

    assert ranked[0]["sensor"] == "sensor_11"
    assert ranked[1]["sensor"] == "sensor_4"
    assert ranked[2]["sensor"] == "sensor_15"
    assert ranked[3]["sensor"] == "sensor_7"

    assert ranked[0]["rank"] == 1
    assert ranked[1]["rank"] == 2
    assert ranked[2]["rank"] == 3
    assert ranked[3]["rank"] == 4

    assert ranked[0]["absolute_contribution"] == 0.82
    assert ranked[1]["absolute_contribution"] == 0.61

    for index in range(len(ranked) - 1):
        assert (
            ranked[index]["absolute_contribution"]
            >= ranked[index + 1]["absolute_contribution"]
        )


def test_get_top_sensor_contributions():
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

    top_sensors = get_top_sensor_contributions(
        sensor_contributions,
        limit=2,
    )

    assert len(top_sensors) == 2

    assert top_sensors[0]["sensor"] == "sensor_11"
    assert top_sensors[1]["sensor"] == "sensor_4"


def test_rank_sensor_contributions_empty():
    result = rank_sensor_contributions([])

    assert result == []


def test_get_top_sensor_contributions_invalid_limit():
    try:
        get_top_sensor_contributions(
            [],
            limit=0,
        )
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "limit must be greater than zero."


def test_rank_sensor_contributions_missing_sensor():
    invalid_data = [
        {
            "contribution": 0.5,
        }
    ]

    try:
        rank_sensor_contributions(invalid_data)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert (
            str(error)
            == "Each sensor contribution must contain 'sensor'."
        )


def test_rank_sensor_contributions_missing_contribution():
    invalid_data = [
        {
            "sensor": "sensor_11",
        }
    ]

    try:
        rank_sensor_contributions(invalid_data)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert (
            str(error)
            == "Each sensor contribution must contain "
            "'contribution'."
        )


if __name__ == "__main__":
    test_rank_sensor_contributions()
    test_get_top_sensor_contributions()
    test_rank_sensor_contributions_empty()
    test_get_top_sensor_contributions_invalid_limit()
    test_rank_sensor_contributions_missing_sensor()
    test_rank_sensor_contributions_missing_contribution()

    print("Sensor contribution tests passed.")