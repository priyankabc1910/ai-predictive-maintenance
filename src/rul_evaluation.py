from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

TEST_DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "test_FD001.txt"
)

RUL_DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "RUL_FD001.txt"
)


def load_test_rul() -> pd.DataFrame:
    """
    Load the official RUL values for the FD001 test set.

    Each row corresponds to one test engine.
    Engine IDs are assigned sequentially from 1.
    """

    rul_values = pd.read_csv(
        RUL_DATA_PATH,
        header=None,
        names=["actual_rul"],
    )

    rul_values["engine_id"] = (
        range(1, len(rul_values) + 1)
    )

    return rul_values[
        [
            "engine_id",
            "actual_rul",
        ]
    ]


def load_test_data() -> pd.DataFrame:
    """
    Load the NASA C-MAPSS FD001 test dataset.
    """

    column_names = [
        "unit_id",
        "cycle",
        "op_setting_1",
        "op_setting_2",
        "op_setting_3",
    ] + [
        f"sensor_{i}"
        for i in range(1, 22)
    ]

    return pd.read_csv(
        TEST_DATA_PATH,
        sep=r"\s+",
        header=None,
        names=column_names,
    )


def load_test_evaluation_data() -> pd.DataFrame:
    """
    Combine test engine metadata with the
    official ground-truth RUL values.
    """

    test_data = load_test_data()
    test_rul = load_test_rul()

    engine_summary = (
        test_data
        .groupby("unit_id")["cycle"]
        .max()
        .reset_index()
        .rename(
            columns={
                "unit_id": "engine_id",
                "cycle": "last_cycle",
            }
        )
    )

    evaluation_data = engine_summary.merge(
        test_rul,
        on="engine_id",
        how="inner",
    )

    return evaluation_data.sort_values(
        "engine_id"
    ).reset_index(drop=True)