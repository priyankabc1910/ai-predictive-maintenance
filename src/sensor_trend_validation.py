from pathlib import Path

from sensor_trends import analyze_sensor_trends


REPRESENTATIVE_ENGINES = [
    1,
    24,
    67,
    83,
    91,
]


if __name__ == "__main__":

    print("=" * 72)
    print("SENSOR DEGRADATION FLEET VALIDATION")
    print("=" * 72)

    for engine_id in REPRESENTATIVE_ENGINES:

        result = analyze_sensor_trends(engine_id)

        critical = sum(
            1
            for sensor in result["sensors"]
            if sensor["severity"] == "CRITICAL"
        )

        high = sum(
            1
            for sensor in result["sensors"]
            if sensor["severity"] == "HIGH"
        )

        medium = sum(
            1
            for sensor in result["sensors"]
            if sensor["severity"] == "MEDIUM"
        )

        low = sum(
            1
            for sensor in result["sensors"]
            if sensor["severity"] == "LOW"
        )

        print()
        print(
            f"{result['machine_id']} "
            f"(latest cycle: {result['latest_cycle']})"
        )

        print(
            f"  Critical sensors : {critical}"
        )

        print(
            f"  High sensors     : {high}"
        )

        print(
            f"  Medium sensors   : {medium}"
        )

        print(
            f"  Low sensors      : {low}"
        )

        print("  Top 3 deviations:")

        for sensor in result["sensors"][:3]:

            print(
                f"    {sensor['sensor']}: "
                f"{sensor['deviation_score']:+.3f}σ "
                f"| {sensor['trend_direction']} "
                f"| {sensor['severity']}"
            )

    print()
    print("=" * 72)
    print("FLEET SENSOR VALIDATION COMPLETE")
    print("=" * 72)