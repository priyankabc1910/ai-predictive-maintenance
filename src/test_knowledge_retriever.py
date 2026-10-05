from knowledge_retriever import (
    build_maintenance_guidance_response,
)


sensor_data = [
    {
        "sensor": "sensor_4",
        "deviation_score": 7.654,
        "trend_slope": 0.42482,
        "trend_direction": "INCREASING",
        "severity": "CRITICAL",
    },
    {
        "sensor": "sensor_13",
        "deviation_score": 6.777,
        "trend_slope": 0.00320,
        "trend_direction": "INCREASING",
        "severity": "CRITICAL",
    },
    {
        "sensor": "sensor_7",
        "deviation_score": -5.979,
        "trend_slope": -0.04373,
        "trend_direction": "DECREASING",
        "severity": "CRITICAL",
    },
]


result = build_maintenance_guidance_response(
    engine_id=1,
    risk_level="CRITICAL",
    rul=2.43,
    anomaly_rate=1.0,
    critical_sensor_count=11,
    high_sensor_count=1,
    sensor_data=sensor_data,
)

print("\nMaintenance Knowledge Retrieval")
print("--------------------------------")

print(
    "Engine:",
    result["machine_id"],
)

print(
    "Risk:",
    result["risk_level"],
)

print(
    "Retrieved:",
    result["retrieval_count"],
)

for item in result["guidance"]:
    print(
        f"\n[{item['score']}] {item['title']}"
    )

    print(
        "Guidance:",
        item["guidance"],
    )

    print("Actions:")

    for action in item["recommended_actions"]:
        print(" -", action)