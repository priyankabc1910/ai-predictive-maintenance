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