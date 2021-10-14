"""Module to define tests for adding telemetry"""
import pytest
from errors.error import ListErrors
from test_data import DEFAULT_TELEMETRY_PARAMS

from pipeline_telemetry.main import Telemetry
from pipeline_telemetry.settings import exceptions


def test_add_method_adds_errors_to_sub_process():
    """Test that errors are added to telemetry sub_process."""
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry.add('RETRIEVE_RAW_DATA', None, [ListErrors.KEY_NOT_FOUND])
    sub_process_telemetry = telemetry.telemetry.get('RETRIEVE_RAW_DATA')
    assert sub_process_telemetry.get(ListErrors.KEY_NOT_FOUND.code) == 1


def test_add_method_raises_exception_when_telemetry_closed():
    """Test that errors are added to telemetry sub_process."""
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry.save_and_close()
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed):
        telemetry.add('RETRIEVE_RAW_DATA', None, [ListErrors.KEY_NOT_FOUND])


def test_add_errors_method_adds_errors_to_sub_process():
    """Test that errors are added to telemetry sub_process."""
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry._add_errors('RETRIEVE_RAW_DATA', [ListErrors.KEY_NOT_FOUND])
    sub_process_telemetry = telemetry.telemetry.get('RETRIEVE_RAW_DATA')
    assert sub_process_telemetry.get(ListErrors.KEY_NOT_FOUND.code) == 1
