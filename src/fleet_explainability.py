
from typing import Dict, List


SEVERITY_ORDER = {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
}


def summarize_fleet_explainability(
    engine_explanations: List[Dict],
) -> Dict:
    total_engines = len(engine_explanations)

    severity_counts = {
        severity: sum(
            1
            for item in engine_explanations
            if item.get("risk_level") == severity
        )
        for severity in SEVERITY_ORDER
    }

    ranked_engines = sorted(
        engine_explanations,
        key=lambda item: (
            SEVERITY_ORDER.get(item.get("risk_level"), 99),
            -item.get("maintenance_score", 0),
        ),
    )

    results = []

    for rank, item in enumerate(ranked_engines, start=1):
        result = dict(item)
        result["explainability_rank"] = rank
        results.append(result)

    return {
        "total_engines": total_engines,
        "severity_counts": severity_counts,
        "ranked_engines": results,
    }
