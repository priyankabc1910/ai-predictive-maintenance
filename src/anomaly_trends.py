from typing import Dict, List


def calculate_anomaly_rate(predictions: List[int]) -> float:
    """
    Calculate the proportion of anomalous observations.

    Isolation Forest uses:
        -1 -> anomaly
         1 -> normal
    """
    if not predictions:
        return 0.0

    anomalous_count = sum(
        1 for prediction in predictions
        if prediction == -1
    )

    return anomalous_count / len(predictions)


def classify_anomaly_trend(
    previous_rate: float,
    current_rate: float,
    threshold: float = 0.10,
) -> str:
    """
    Classify the change in anomaly rate.

    A change greater than or equal to the threshold
    is considered significant.
    """
    change = current_rate - previous_rate

    if change >= threshold:
        return "INCREASING"

    if change <= -threshold:
        return "DECREASING"

    return "STABLE"


def analyze_anomaly_trend(
    previous_predictions: List[int],
    current_predictions: List[int],
    threshold: float = 0.10,
) -> Dict:
    """
    Compare anomaly rates between two consecutive
    operating windows.
    """
    previous_rate = calculate_anomaly_rate(
        previous_predictions
    )

    current_rate = calculate_anomaly_rate(
        current_predictions
    )

    change = current_rate - previous_rate

    trend = classify_anomaly_trend(
        previous_rate=previous_rate,
        current_rate=current_rate,
        threshold=threshold,
    )

    return {
        "previous_anomaly_rate": round(
            previous_rate,
            4,
        ),
        "current_anomaly_rate": round(
            current_rate,
            4,
        ),
        "rate_change": round(
            change,
            4,
        ),
        "trend": trend,
    }
def summarize_fleet_anomaly_trends(
    engine_trends: List[Dict],
) -> Dict:
    """
    Aggregate anomaly trend results across the fleet.
    """

    total_engines = len(engine_trends)

    increasing_engines = sum(
        1
        for item in engine_trends
        if item["trend"] == "INCREASING"
    )

    decreasing_engines = sum(
        1
        for item in engine_trends
        if item["trend"] == "DECREASING"
    )

    stable_engines = sum(
        1
        for item in engine_trends
        if item["trend"] == "STABLE"
    )

    rate_changes = [
        item["rate_change"]
        for item in engine_trends
    ]

    average_rate_change = (
        sum(rate_changes) / len(rate_changes)
        if rate_changes
        else 0.0
    )

    maximum_rate_change = (
        max(rate_changes)
        if rate_changes
        else 0.0
    )

    worsening_rate = (
        increasing_engines / total_engines
        if total_engines
        else 0.0
    )

    return {
        "total_engines": total_engines,
        "increasing_engines": increasing_engines,
        "decreasing_engines": decreasing_engines,
        "stable_engines": stable_engines,
        "worsening_rate": round(
            worsening_rate,
            4,
        ),
        "average_rate_change": round(
            average_rate_change,
            4,
        ),
        "maximum_rate_change": round(
            maximum_rate_change,
            4,
        ),
    }