"""Module to test the DailyAggregator class."""

from test_aggregator_data import TelemetryTestList

from pipeline_telemetry import PartialToSingleAggregator, TelemetrySelector
from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.settings.date_ranges import get_daily_date_range_yesterday

keys_in_telemetry_list_params = [
    "telemetry_type",
    "category",
    "sub_category",
    "source_name",
    "process_type",
    "from_date_time",
    "to_date_time",
]


def test_partial_to_daily_aggregator_exists():
    """Test that the PartialToDailyAggregator class exists."""
    assert PartialToSingleAggregator


def test_run_aggregation():
    """Method to test a single aggregation."""
    telemetry_selector = TelemetrySelector(
        category="test",
        sub_category="sub_test",
        source_name="source",
        process_type="process_type",
    )
    aggr = PartialToSingleAggregator(
        telemetry_selector=telemetry_selector, telemetry_storage=TelemetryTestList()
    )
    result_telemetry = aggr._run_aggregation(next(get_daily_date_range_yesterday()))
    assert isinstance(result_telemetry, TelemetryModel)
    assert result_telemetry.telemetry["DATA_STORAGE"].base_counter == 3
    assert result_telemetry.telemetry["DATA_STORAGE"].fail_counter == 1
