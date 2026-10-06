from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "train_FD001.txt"
)


COLUMN_NAMES = [
    "unit_id",
    "cycle",
    "op_setting_1",
    "op_setting_2",
    "op_setting_3",
] + [
    f"sensor_{i}"
    for i in range(1, 22)
]


SENSOR_COLUMNS = [
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_7",
    "sensor_8",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_15",
    "sensor_17",
    "sensor_20",
    "sensor_21",
]


BASELINE_WINDOW = 30
CURRENT_WINDOW = 30


def load_data():
    return pd.read_csv(
        RAW_DATA_PATH,
        sep=r"\s+",
        header=None,
        names=COLUMN_NAMES,
    )


def classify_deviation(deviation_score):
    """
    Classify how far the current sensor behaviour
    has moved from its healthy baseline.
    """

    absolute_score = abs(deviation_score)

    if absolute_score >= 3.0:
        return "CRITICAL"

    if absolute_score >= 2.0:
        return "HIGH"

    if absolute_score >= 1.0:
        return "MEDIUM"

    return "LOW"


def analyze_sensor_trends(
    engine_id: int,
    baseline_window: int = BASELINE_WINDOW,
    current_window: int = CURRENT_WINDOW,
    engine_data: pd.DataFrame = None,
):

    if engine_data is None:
        df = load_data()

        engine_data = (
            df[df["unit_id"] == engine_id]
            .sort_values("cycle")
            .copy()
        )
    else:
        engine_data = (
            engine_data[
                engine_data["unit_id"] == engine_id
            ]
            .sort_values("cycle")
            .copy()
        )

    if engine_data.empty:
        raise ValueError(
            f"Engine {engine_id} not found."
        )

    if len(engine_data) < (
        baseline_window + current_window
    ):
        raise ValueError(
            f"Engine {engine_id} does not have enough "
            f"cycles for trend analysis."
        )

    baseline = engine_data.head(
        baseline_window
    )

    current = engine_data.tail(
        current_window
    )

    results = []

    for sensor in SENSOR_COLUMNS:

        baseline_values = baseline[sensor].values
        current_values = current[sensor].values

        baseline_mean = float(
            np.mean(baseline_values)
        )

        baseline_std = float(
            np.std(baseline_values)
        )

        current_mean = float(
            np.mean(current_values)
        )

        absolute_change = (
            current_mean - baseline_mean
        )

        # Prevent division by zero for sensors
        # with extremely small baseline variance.
        safe_std = max(
            baseline_std,
            1e-6,
        )

        deviation_score = (
            absolute_change / safe_std
        )

        # Linear trend over the latest window.
        x = np.arange(
            len(current_values)
        )

        slope = float(
            np.polyfit(
                x,
                current_values,
                1,
            )[0]
        )

        if slope > 0:
            trend_direction = "INCREASING"
        elif slope < 0:
            trend_direction = "DECREASING"
        else:
            trend_direction = "STABLE"

        severity = classify_deviation(
            deviation_score
        )

        results.append(
            {
                "sensor": sensor,
                "baseline_mean": round(
                    baseline_mean,
                    4,
                ),
                "current_mean": round(
                    current_mean,
                    4,
                ),
                "absolute_change": round(
                    absolute_change,
                    4,
                ),
                "deviation_score": round(
                    deviation_score,
                    4,
                ),
                "trend_slope": round(
                    slope,
                    6,
                ),
                "trend_direction": trend_direction,
                "severity": severity,
            }
        )

    # Largest deviations first.
    results.sort(
        key=lambda item: abs(
            item["deviation_score"]
        ),
        reverse=True,
    )

    return {
        "engine_id": int(engine_id),
        "machine_id": (
            f"UNIT-{engine_id:03d}"
        ),
        "baseline_window": baseline_window,
        "current_window": current_window,
        "latest_cycle": int(
            current["cycle"].iloc[-1]
        ),
        "sensors": results,
    }


if __name__ == "__main__":

    ENGINE_ID = 1

    result = analyze_sensor_trends(
        ENGINE_ID
    )

    print("=" * 72)
    print(
        f"SENSOR TREND ANALYSIS — "
        f"{result['machine_id']}"
    )
    print("=" * 72)

    print(
        f"Baseline: first "
        f"{result['baseline_window']} cycles"
    )

    print(
        f"Current window: latest "
        f"{result['current_window']} cycles"
    )

    print(
        f"Latest cycle: "
        f"{result['latest_cycle']}"
    )

    print()
    print(
        f"{'SENSOR':<12}"
        f"{'DEV SCORE':>12}"
        f"{'SLOPE':>14}"
        f"{'TREND':>15}"
        f"{'SEVERITY':>14}"
    )

    print("-" * 72)

    for sensor in result["sensors"]:

        print(
            f"{sensor['sensor']:<12}"
            f"{sensor['deviation_score']:>12.3f}"
            f"{sensor['trend_slope']:>14.5f}"
            f"{sensor['trend_direction']:>15}"
            f"{sensor['severity']:>14}"
        )

    print()
    print("=" * 72)
    print("SENSOR TREND ANALYSIS COMPLETE")
    print("=" * 72)