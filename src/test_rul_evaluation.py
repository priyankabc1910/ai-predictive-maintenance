from rul_evaluation import (
    load_test_rul,
    load_test_data,
    load_test_evaluation_data,
)


def test_load_test_rul():
    data = load_test_rul()

    assert len(data) == 100

    assert list(data.columns) == [
        "engine_id",
        "actual_rul",
    ]

    assert data["engine_id"].iloc[0] == 1
    assert data["engine_id"].iloc[-1] == 100

    assert data["actual_rul"].iloc[0] == 112
    assert data["actual_rul"].iloc[1] == 98


def test_load_test_data():
    data = load_test_data()

    assert not data.empty

    assert "unit_id" in data.columns
    assert "cycle" in data.columns

    assert data["unit_id"].nunique() == 100


def test_load_test_evaluation_data():
    data = load_test_evaluation_data()

    assert len(data) == 100

    assert list(data.columns) == [
        "engine_id",
        "last_cycle",
        "actual_rul",
    ]

    assert data["engine_id"].iloc[0] == 1
    assert data["engine_id"].iloc[-1] == 100

    assert data["actual_rul"].notna().all()
    assert data["last_cycle"].notna().all()


if __name__ == "__main__":
    test_load_test_rul()
    test_load_test_data()
    test_load_test_evaluation_data()

    print("RUL evaluation loader tests passed.")