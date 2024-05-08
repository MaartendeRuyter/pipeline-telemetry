"""Module to test aggregator logic."""

from pipeline_telemetry import TelemetryAggregator


def test_aggegator_class_exists():
    """Test the TelemetryAggregator class exists."""
    assert TelemetryAggregator


def test_initializing_aggegator_instance():
    """
    Test that the TelemetryAggregator can be instantiated with an int as int support the __add__ method
    """
    assert TelemetryAggregator(1)


def test_aggegator_from_adds_all_telemetry_list_items():
    """
    Test that the aggregate_from method adds all items from a telemetry list to
    the telemetry object and returns the result.
    """
    new_telemetry = 1
    aggregator = TelemetryAggregator(new_telemetry)
    telemetry_list = [2, 3, 4]
    assert aggregator.aggregate(telemetry_list) == 10
