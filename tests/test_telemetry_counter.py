"""
Module to test telemetry counter login for pipeline telemetry module.
"""
import pytest
from test_data import DEFAULT_TELEMETRY_PARAMS, TEST_ERROR_TELEMETRY_COUNTER, \
    TEST_INV_TELEMETRY_COUNTER, TEST_TELEMETRY_COUNTER, \
    TEST_TELEMETRY_COUNTER_INC_2

from pipeline_telemetry.main import ERRORS_KEY, Telemetry
from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings.data_class import TelemetryCounter


@pytest.fixture
def telemetry_inst():
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    return telemetry_inst


def test_telemetry_counter_exists():
    """check that TelemetryCounter class exists"""
    assert TelemetryCounter


def test_add_telemetry_counter_to_telemetry(telemetry_inst):
    """
    Check that adding a telemetry counter to a Telemetry instance
    creates a counter
    """
    telemetry_inst.add_telemetry_counter(TEST_TELEMETRY_COUNTER)
    assert telemetry_inst.get("RETRIEVE_RAW_DATA")["test_counter"] == 1


def test_add_error_telemetry_counter_to_telemetry(telemetry_inst):
    """
    Check that adding a telemetry counter to a Telemetry instance
    creates a counter
    """
    telemetry_inst.add_telemetry_counter(TEST_ERROR_TELEMETRY_COUNTER)
    assert telemetry_inst.get("RETRIEVE_RAW_DATA")[
        ERRORS_KEY]["HAS_KEY_ERR_0001"] == 1


def test_add_error_telemetry_counter_to_telemetry_raises_exception():
    """
    Check that adding a telemetry counter to a Telemetry instance
    raises exception when basecounter has not been added
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    with pytest.raises(exceptions.BaseCountForSubProcessNotAdded):
        telemetry_inst.add_telemetry_counter(TEST_ERROR_TELEMETRY_COUNTER)


def test_add_telemetry_counter_with_icrement_2_to_telemetry(telemetry_inst):
    """
    Check that adding a telemetry counter with increment = 2 to a Telemetry
    raises the counter with value of 2
    """
    telemetry_inst.add_telemetry_counter(TEST_TELEMETRY_COUNTER)
    assert telemetry_inst.get("RETRIEVE_RAW_DATA")["test_counter"] == 1
    telemetry_inst.add_telemetry_counter(TEST_TELEMETRY_COUNTER_INC_2)
    assert telemetry_inst.get("RETRIEVE_RAW_DATA")["test_counter"] == 3


def test_add_telemetry_counter_with_increment_arg(telemetry_inst):
    """
    Check invoking add_telemetry_counter method using increment argument adds
    the value of increment to the counter
    """
    telemetry_inst.add_telemetry_counter(TEST_TELEMETRY_COUNTER, increment=10)
    assert telemetry_inst.get("RETRIEVE_RAW_DATA")["test_counter"] == 10


def test_add_telemetry_counter_raises_exception(telemetry_inst):
    """
    Check invoking add_telemetry_counter method using increment argument adds
    the value of increment to the counter
    """
    with pytest.raises(exceptions.InvalidSubProcessForProcessType):
        telemetry_inst.add_telemetry_counter(TEST_INV_TELEMETRY_COUNTER)
