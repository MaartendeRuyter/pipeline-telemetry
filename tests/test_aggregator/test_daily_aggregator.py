"""Module to test the DailyAggregator class.
"""
from test_aggregator_data import TelemetryTestList

from pipeline_telemetry import DailyAggregator, TelemetrySelector
from pipeline_telemetry.settings import settings as st


def test_daily_aggregator_exists():
    """Test that the DailyAggregator class exists."""
    assert DailyAggregator


def test_telemetry_selector_class_exists():
    """Test that the TelemetrySelector class exists."""
    assert TelemetrySelector


def test_telemetry_selector_class_can_be_instantiated():
    """Test that the TelemetrySelector class exists."""
    assert TelemetrySelector(
        category='test', sub_category='sub_test', source_name='source',
        process_type='process_type'
    )


def test_daily_aggregator_defines_target_telemetry_object():
    """Test that the DailyAggregator defines ."""
    telemetry_selector = TelemetrySelector(
        category='test', sub_category='sub_test', source_name='source',
        process_type='process_type')

    aggr = DailyAggregator(
        telemetry_selector=telemetry_selector,
        telemetry_storage=TelemetryTestList
    )
    assert aggr.target_telemetry_model.telemetry_type == \
        st.DAILY_AGGR_TELEMETRY_TYPE
