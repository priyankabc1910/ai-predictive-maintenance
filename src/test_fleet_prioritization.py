from fleet_prioritization import prioritize_fleet


def test_prioritize_fleet():
    decisions = [
        {
            "engine_id": 3,
            "machine_id": "UNIT-003",
            "rul": 80.0,
            "maintenance_score": 30,
            "priority": "PLANNED",
        },
        {
            "engine_id": 1,
            "machine_id": "UNIT-001",
            "rul": 2.43,
            "maintenance_score": 100,
            "priority": "IMMEDIATE",
        },
        {
            "engine_id": 2,
            "machine_id": "UNIT-002",
            "rul": 40.0,
            "maintenance_score": 70,
            "priority": "URGENT",
        },
    ]

    ranked = prioritize_fleet(decisions)

    assert ranked[0]["engine_id"] == 1
    assert ranked[0]["fleet_rank"] == 1

    assert ranked[1]["engine_id"] == 2
    assert ranked[1]["fleet_rank"] == 2

    assert ranked[2]["engine_id"] == 3
    assert ranked[2]["fleet_rank"] == 3

    print("Fleet prioritization test passed.")


if __name__ == "__main__":
    test_prioritize_fleet()