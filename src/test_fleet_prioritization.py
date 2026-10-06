from fleet_prioritization import prioritize_fleet


def test_fleet_prioritization():
    decisions = [
        {
            "engine_id": 2,
            "machine_id": "UNIT-002",
            "rul": 40,
            "maintenance_score": 70,
            "priority": "PLANNED",
        },
        {
            "engine_id": 1,
            "machine_id": "UNIT-001",
            "rul": 5,
            "maintenance_score": 100,
            "priority": "IMMEDIATE",
        },
        {
            "engine_id": 3,
            "machine_id": "UNIT-003",
            "rul": 80,
            "maintenance_score": 20,
            "priority": "ROUTINE",
        },
    ]

    ranked = prioritize_fleet(decisions)

    assert ranked[0]["machine_id"] == "UNIT-001"
    assert ranked[0]["fleet_rank"] == 1

    assert ranked[1]["machine_id"] == "UNIT-002"
    assert ranked[1]["fleet_rank"] == 2

    assert ranked[2]["machine_id"] == "UNIT-003"
    assert ranked[2]["fleet_rank"] == 3


if __name__ == "__main__":
    test_fleet_prioritization()
    print("Fleet prioritization test passed.")