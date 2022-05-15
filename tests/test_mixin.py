"""
Module to test telemetry mixin class for pipeline telemetry module.
"""
import pipeline_telemetry.mixin as HP
from pipeline_telemetry.mixin import TelemetryMixin


def test_telemetry_mixin_exists():
    """check that TelemetryMixin class exists"""
    assert TelemetryMixin


def test_process_errors_from_return_values(mocker):
    """
    Test method process_errors_from_return_value calls helper method
    add_errors_from_return_value
    """
    mocker.patch(
        ("pipeline_telemetry.mixin."
         "add_errors_from_return_value"),
        return_value=None)
    add_errors_spy = mocker.spy(
        HP, "add_errors_from_return_value")

    TelemetryMixin().process_errors_from_return_values(
        sub_process='TEST',
        return_value='test')
    assert add_errors_spy.called
