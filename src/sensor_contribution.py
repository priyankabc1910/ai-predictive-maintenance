from typing import Dict, List


def rank_sensor_contributions(
    sensor_contributions: List[Dict],
) -> List[Dict]:
    """
    Rank sensors by their contribution magnitude.

    Each item must contain:
        sensor
        contribution
    """

    if not sensor_contributions:
        return []

    for item in sensor_contributions:
        if "sensor" not in item:
            raise ValueError(
                "Each sensor contribution must contain 'sensor'."
            )

        if "contribution" not in item:
            raise ValueError(
                "Each sensor contribution must contain "
                "'contribution'."
            )

    ranked = sorted(
        sensor_contributions,
        key=lambda item: abs(item["contribution"]),
        reverse=True,
    )

    results = []

    for rank, item in enumerate(ranked, start=1):
        result = dict(item)
        result["rank"] = rank
        result["absolute_contribution"] = round(
            abs(item["contribution"]),
            6,
        )
        results.append(result)

    return results


def get_top_sensor_contributions(
    sensor_contributions: List[Dict],
    limit: int = 5,
) -> List[Dict]:
    """
    Return the highest-contributing sensors.
    """

    if limit <= 0:
        raise ValueError(
            "limit must be greater than zero."
        )

    ranked = rank_sensor_contributions(
        sensor_contributions
    )

    return ranked[:limit]