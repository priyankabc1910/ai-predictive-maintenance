
import pytest

from src.maintenance_cost import estimate_maintenance_cost


def test_immediate_maintenance_estimate():
    result = estimate_maintenance_cost("IMMEDIATE")

    assert result["estimated_cost"] == 50000.0
    assert result["currency"] == "INR"
    assert result["estimate_type"] == "illustrative"


def test_custom_cost_estimate():
    result = estimate_maintenance_cost(
        "PLANNED",
        {"PLANNED": 7500},
    )

    assert result["estimated_cost"] == 7500.0


def test_unsupported_priority_is_rejected():
    with pytest.raises(ValueError):
        estimate_maintenance_cost("UNKNOWN")


def test_negative_cost_is_rejected():
    with pytest.raises(ValueError):
        estimate_maintenance_cost("ROUTINE", {"ROUTINE": -10})
