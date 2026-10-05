from typing import Dict, List


PRIORITY_ORDER = {
    "IMMEDIATE": 0,
    "URGENT": 1,
    "PLANNED": 2,
    "ROUTINE": 3,
}


def prioritize_fleet(
    maintenance_decisions: List[Dict],
) -> List[Dict]:
    """
    Rank engines by maintenance urgency.

    Primary ranking:
        1. Maintenance priority
        2. Maintenance score
        3. RUL

    Lower RUL is more urgent when other signals are comparable.
    """

    ranked = sorted(
        maintenance_decisions,
        key=lambda item: (
            PRIORITY_ORDER.get(
                item["priority"].upper(),
                99,
            ),
            -item["maintenance_score"],
            item["rul"],
        ),
    )

    results = []

    for rank, item in enumerate(ranked, start=1):
        result = dict(item)
        result["fleet_rank"] = rank
        results.append(result)

    return results