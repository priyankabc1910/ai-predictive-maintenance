
from typing import Dict


DEFAULT_COST_ESTIMATES = {
    "IMMEDIATE": 50000.0,
    "URGENT": 25000.0,
    "PLANNED": 10000.0,
    "ROUTINE": 2000.0,
}


def estimate_maintenance_cost(
    priority: str,
    cost_estimates: Dict[str, float] = None,
) -> Dict:
    estimates = (
        DEFAULT_COST_ESTIMATES.copy()
        if cost_estimates is None
        else cost_estimates.copy()
    )

    normalized_priority = priority.upper()

    if normalized_priority not in estimates:
        raise ValueError(f"Unsupported maintenance priority: {priority}")

    cost = estimates[normalized_priority]

    if cost < 0:
        raise ValueError("Maintenance cost estimate cannot be negative.")

    return {
        "priority": normalized_priority,
        "estimated_cost": round(float(cost), 2),
        "currency": "INR",
        "estimate_type": "illustrative",
        "disclaimer": (
            "Illustrative planning estimate only; "
            "not a vendor quote or actual repair cost."
        ),
    }
