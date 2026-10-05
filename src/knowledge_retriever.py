import json
from pathlib import Path
from typing import Dict, List


BASE_DIR = Path(__file__).resolve().parents[1]

KNOWLEDGE_PATH = (
    BASE_DIR
    / "knowledge"
    / "maintenance_guidance.json"
)


def load_maintenance_knowledge() -> List[Dict]:
    if not KNOWLEDGE_PATH.exists():
        raise FileNotFoundError(
            f"Maintenance knowledge base not found: {KNOWLEDGE_PATH}"
        )

    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_maintenance_guidance(
    risk_level: str,
    rul: float,
    anomaly_rate: float,
    critical_sensor_count: int,
    high_sensor_count: int,
    sensor_data: List[Dict],
    top_k: int = 5,
) -> List[Dict]:

    knowledge = load_maintenance_knowledge()

    matches = []

    # ------------------------------------------
    # Build signals from actual model output
    # ------------------------------------------

    signals = set()

    if rul <= 20:
        signals.add("RUL-CRITICAL")

    if anomaly_rate >= 0.75:
        signals.add("ANOMALY-HIGH")

    if critical_sensor_count > 0:
        signals.add("SENSOR-CRITICAL")

    if critical_sensor_count >= 3:
        signals.add("MULTI-SENSOR-DEGRADATION")

    trend_directions = {
        sensor.get("trend_direction")
        for sensor in sensor_data
    }

    if "INCREASING" in trend_directions:
        signals.add("TREND-INCREASING")

    if "DECREASING" in trend_directions:
        signals.add("TREND-DECREASING")

    # ------------------------------------------
    # Match knowledge records
    # ------------------------------------------

    for item in knowledge:

        item_id = item.get("id")

        if item_id not in signals:
            continue

        risk_levels = {
            level.upper()
            for level in item.get("risk_levels", [])
        }

        if risk_level.upper() not in risk_levels:
            continue

        # --------------------------------------
        # Calculate retrieval priority
        # --------------------------------------

        score = 0

        if item_id == "RUL-CRITICAL":
            score += 100

        elif item_id == "ANOMALY-HIGH":
            score += 90

        elif item_id == "SENSOR-CRITICAL":
            score += 80

        elif item_id == "MULTI-SENSOR-DEGRADATION":
            score += 85

        elif item_id in {
            "TREND-INCREASING",
            "TREND-DECREASING",
        }:
            score += 50

        matches.append({
            "id": item["id"],
            "title": item["title"],
            "category": item["category"],
            "score": score,
            "guidance": item["guidance"],
            "recommended_actions": item[
                "recommended_actions"
            ],
        })

    # ------------------------------------------
    # Sort by relevance
    # ------------------------------------------

    matches.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return matches[:top_k]


def build_maintenance_guidance_response(
    engine_id: int,
    risk_level: str,
    rul: float,
    anomaly_rate: float,
    critical_sensor_count: int,
    high_sensor_count: int,
    sensor_data: List[Dict],
    top_k: int = 5,
) -> Dict:

    results = retrieve_maintenance_guidance(
        risk_level=risk_level,
        rul=rul,
        anomaly_rate=anomaly_rate,
        critical_sensor_count=critical_sensor_count,
        high_sensor_count=high_sensor_count,
        sensor_data=sensor_data,
        top_k=top_k,
    )

    return {
        "engine_id": int(engine_id),
        "machine_id": f"UNIT-{engine_id:03d}",
        "risk_level": risk_level,
        "retrieval_count": len(results),
        "guidance": results,
    }