from typing import Dict, List

from .sensor_contribution import rank_sensor_contributions


def rank_rul_drivers(
    sensor_contributions: List[Dict],
) -> List[Dict]:
    """
    Rank sensor drivers contributing to an RUL prediction.

    Higher absolute contribution means a stronger driver.
    """

    ranked = rank_sensor_contributions(
        sensor_contributions
    )

    results = []

    for item in ranked:
        result = dict(item)

        if item["contribution"] > 0:
            result["direction"] = "POSITIVE"
        elif item["contribution"] < 0:
            result["direction"] = "NEGATIVE"
        else:
            result["direction"] = "NEUTRAL"

        results.append(result)

    return results


def get_top_rul_drivers(
    sensor_contributions: List[Dict],
    limit: int = 5,
) -> List[Dict]:
    """
    Return the strongest drivers of the RUL prediction.
    """

    if limit <= 0:
        raise ValueError(
            "limit must be greater than zero."
        )

    ranked = rank_rul_drivers(
        sensor_contributions
    )

    return ranked[:limit]