"""Module to define tests for adding telemetry"""
import pytest
from errors.error import ListErrors
from test_data import DEFAULT_TELEMETRY_PARAMS, TEST_TELEMETRY_RULES

from pipeline_telemetry.main import Telemetry
from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings import settings as st


def test_add_method_adds_errors_to_sub_process():
    """Test that errors are added to telemetry sub_process."""
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry.add('RETRIEVE_RAW_DATA', None, [ListErrors.KEY_NOT_FOUND])
    sub_process_telemetry = telemetry.telemetry.get('RETRIEVE_RAW_DATA')
    assert sub_process_telemetry[st.ERRORS_KEY].get(
        ListErrors.KEY_NOT_FOUND.code) == 1


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
    assert sub_process_telemetry[st.ERRORS_KEY].get(
        ListErrors.KEY_NOT_FOUND.code) == 1


def test_validate_data_method():
    """Test _validate_data_method returns list of errors."""
    telemetry = Telemetry(telemetry_rules=TEST_TELEMETRY_RULES,
                          **DEFAULT_TELEMETRY_PARAMS)
    telemetry.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    errors = telemetry._validate_data(sub_process='RETRIEVE_RAW_DATA',
                                      data={})
    assert ListErrors.KEY_NOT_FOUND.code in str(errors[0])
    assert '@KEY_<items>' in str(errors[0])


def test_validate_data_method_returns_empty_list():
    """
    Test _validate_data_method returns empty list when no errors are found.
    """
    telemetry = Telemetry(telemetry_rules=TEST_TELEMETRY_RULES,
                          **DEFAULT_TELEMETRY_PARAMS)
    telemetry.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    errors = telemetry._validate_data(sub_process='RETRIEVE_RAW_DATA',
                                      data={'items': [1, 2, 3]})
    assert errors == []
