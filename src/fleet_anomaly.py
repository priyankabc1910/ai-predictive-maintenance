from typing import Dict, List


SEVERITY_ORDER = {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
}


def classify_fleet_anomaly_rate(anomaly_rate: float) -> str:
    if anomaly_rate >= 0.50:
        return "CRITICAL"
    if anomaly_rate >= 0.25:
        return "HIGH"
    if anomaly_rate >= 0.10:
        return "MEDIUM"
    return "LOW"

def aggregate_fleet_anomalies(
    engine_anomalies: List[Dict],
) -> Dict:
    total_engines = len(engine_anomalies)

    critical_engines = sum(
        1
        for item in engine_anomalies
        if item["severity"] == "CRITICAL"
    )

    high_engines = sum(
        1
        for item in engine_anomalies
        if item["severity"] == "HIGH"
    )

    medium_engines = sum(
        1
        for item in engine_anomalies
        if item["severity"] == "MEDIUM"
    )

    low_engines = sum(
        1
        for item in engine_anomalies
        if item["severity"] == "LOW"
    )

    anomalous_engines = sum(
        1
        for item in engine_anomalies
        if item["anomaly_rate"] > 0
    )

    fleet_anomaly_rate = (
        anomalous_engines / total_engines
        if total_engines
        else 0.0
    )

    ranked_engines = sorted(
        engine_anomalies,
        key=lambda item: (
            SEVERITY_ORDER.get(item["severity"], 99),
            -item["anomaly_rate"],
        ),
    )

    ranked_results = []

    for rank, item in enumerate(
        ranked_engines,
        start=1,
    ):
        result = dict(item)

        result["anomaly_rank"] = rank

        result["anomaly_score"] = round(
            item["anomaly_rate"] * 100,
            2,
        )

        ranked_results.append(result)

    return {
        "total_engines": total_engines,
        "anomalous_engines": anomalous_engines,
        "fleet_anomaly_rate": round(
            fleet_anomaly_rate,
            4,
        ),
        "severity_counts": {
            "CRITICAL": critical_engines,
            "HIGH": high_engines,
            "MEDIUM": medium_engines,
            "LOW": low_engines,
        },
        "ranked_engines": ranked_results,
    }