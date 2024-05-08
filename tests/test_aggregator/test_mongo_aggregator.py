"""Module to test the momgo Aggregators."""

from test_aggregator_data import TEST_TELEMETRY_SELECTOR

from pipeline_telemetry import DailyAggregator, DailyMongoAggregator
from pipeline_telemetry.storage import TelemetryMongoStorage


def test_daily_mongo_aggregator_class_exists():
    """Test that DailyMongoAggregator class exists."""
    assert DailyMongoAggregator


def test_daily_mongo_aggregator_returns_daily_telemerty_class():
    """
    Test that DailyMongoAggregator class when instanciated returns
    a DailyAggregator with TelemetryMongoStorage class.
    """
    aggregator = DailyMongoAggregator(TEST_TELEMETRY_SELECTOR)
    assert isinstance(aggregator, DailyAggregator)
    assert isinstance(aggregator.storage_class, TelemetryMongoStorage)
