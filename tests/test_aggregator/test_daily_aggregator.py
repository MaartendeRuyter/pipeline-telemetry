"""Module to test the DailyAggregator class."""

from test_aggregator_data import (
    DAY_BEFORE_YESTERDAY,
    TODAY,
    YESTERDAY,
    TelemetryTestList,
)

from pipeline_telemetry import DailyAggregator, TelemetrySelector
from pipeline_telemetry.aggregator.helper import TelemetryListArgs
from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.settings import settings as st
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


def test_daily_aggregator_exists():
    """Test that the DailyAggregator class exists."""
    assert DailyAggregator


def test_telemetry_selector_class_exists():
    """Test that the TelemetrySelector class exists."""
    assert TelemetrySelector


def test_telemetry_selector_class_can_be_instantiated():
    """Test that the TelemetrySelector class exists."""
    assert TelemetrySelector(
        category="test",
        sub_category="sub_test",
        source_name="source",
        process_type="process_type",
    )


def test_daily_aggregator_defines_target_telemetry_object():
    """Test that the DailyAggregator defines ."""
    telemetry_selector = TelemetrySelector(
        category="test",
        sub_category="sub_test",
        source_name="source",
        process_type="process_type",
    )

    aggr = DailyAggregator(
        telemetry_selector=telemetry_selector, telemetry_storage=TelemetryTestList
    )
    assert aggr.target_telemetry.telemetry_type == st.DAILY_AGGR_TELEMETRY_TYPE


def test_telememtry_list_params():
    """Test if telemetry list params returns TelemetryListArgs."""
    telemetry_selector = TelemetrySelector(
        category="test",
        sub_category="sub_test",
        source_name="source",
        process_type="process_type",
    )

    aggr = DailyAggregator(
        telemetry_selector=telemetry_selector, telemetry_storage=TelemetryTestList
    )
    telemetry_list_params = aggr._telememtry_list_params(
        date_time_range=next(get_daily_date_range_yesterday())
    )
    assert isinstance(telemetry_list_params, TelemetryListArgs)


def test_run_aggregation():
    """Method to test a single aggregation."""
    telemetry_selector = TelemetrySelector(
        category="test",
        sub_category="sub_test",
        source_name="source",
        process_type="process_type",
    )
    aggr = DailyAggregator(
        telemetry_selector=telemetry_selector, telemetry_storage=TelemetryTestList()
    )
    result_telemetry = aggr._run_aggregation(next(get_daily_date_range_yesterday()))
    assert isinstance(result_telemetry, TelemetryModel)
    assert result_telemetry.telemetry["DATA_STORAGE"].base_counter == 3
    assert result_telemetry.telemetry["DATA_STORAGE"].fail_counter == 1


def test_run_aggregation_for_one_day():
    """Method to test that one aggregation was stored."""
    telemetry_selector = TelemetrySelector(
        category="test",
        sub_category="sub_test",
        source_name="source",
        process_type="process_type",
    )
    storage = TelemetryTestList()
    aggr = DailyAggregator(
        telemetry_selector=telemetry_selector, telemetry_storage=storage
    )
    aggr.aggregate(YESTERDAY, TODAY)
    assert len(storage.stored_telemetry) == 1
    result_telemetry = storage.stored_telemetry[0]
    assert result_telemetry.telemetry["DATA_STORAGE"].base_counter == 3


def test_run_aggregation_for_two_days():
    """Method to test that two aggregations were stored."""
    telemetry_selector = TelemetrySelector(
        category="test",
        sub_category="sub_test",
        source_name="source",
        process_type="process_type",
    )
    storage = TelemetryTestList()
    aggr = DailyAggregator(
        telemetry_selector=telemetry_selector, telemetry_storage=storage
    )
    aggr.aggregate(DAY_BEFORE_YESTERDAY, TODAY)
    assert len(storage.stored_telemetry) == 2
    first_telemetry = storage.stored_telemetry[0]
    second_telemetry = storage.stored_telemetry[1]
    assert first_telemetry.start_date_time.date() == DAY_BEFORE_YESTERDAY
    assert second_telemetry.start_date_time.date() == YESTERDAY
