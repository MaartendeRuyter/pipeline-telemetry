"""
Module to test telemetry mixin class for pipeline telemetry module.
"""
import pipeline_telemetry.mixin as MX


def test_telemetry_mixin_exists():
    """check that TelemetryMixin class exists"""
    assert MX.TelemetryMixin


def test_process_errors_from_return_value(mocker):
    """
    Test method process_errors_from_return_value calls helper method
    add_errors_from_return_value
    """
    mocker.patch(
        ("pipeline_telemetry.mixin."
         "add_errors_from_return_value"),
        return_value=None)
    add_errors_spy = mocker.spy(
        MX, "add_errors_from_return_value")

    MX.TelemetryMixin().process_errors_from_return_value(
        sub_process='TEST',
        return_value='test')
    assert add_errors_spy.called


def test_process_telemetry_counters_from_return_value(mocker):
    """
    Test method process_telemetry_counters_from_return_value calls helper
    method add_telemetry_counters_from_return_value
    """
    mocker.patch(
        ("pipeline_telemetry.mixin."
         "add_telemetry_counters_from_return_value"),
        return_value=None)
    add_telemetry_counters_spy = mocker.spy(
        MX, "add_telemetry_counters_from_return_value")

    MX.TelemetryMixin().process_telemetry_counters_from_return_value(
        return_value='test')
    assert add_telemetry_counters_spy.called
