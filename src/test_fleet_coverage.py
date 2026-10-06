from fleet_prioritization import prioritize_fleet


def test_fleet_coverage():
    decisions = []

    for engine_id in range(1, 101):
        decisions.append(
            {
                "engine_id": engine_id,
                "machine_id": f"UNIT-{engine_id:03d}",
                "rul": float(engine_id),
                "maintenance_score": float(100 - engine_id),
                "priority": "ROUTINE",
            }
        )

    ranked = prioritize_fleet(decisions)

    assert len(ranked) == 100
    assert ranked[0]["fleet_rank"] == 1
    assert ranked[-1]["fleet_rank"] == 100

    machine_ids = {
        item["machine_id"]
        for item in ranked
    }

    assert len(machine_ids) == 100


if __name__ == "__main__":
    test_fleet_coverage()
    print("Fleet coverage test passed for 100 engines.")