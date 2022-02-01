"""
Module to test telemetry counter login for pipeline telemetry module.
"""
import pytest
from test_data import DEFAULT_TELEMETRY_PARAMS, TEST_ERROR_TELEMETRY_COUNTER, \
    TEST_INV_TELEMETRY_COUNTER, TEST_TELEMETRY_COUNTER, \
    TEST_TELEMETRY_COUNTER_INC_2

from pipeline_telemetry import ProcessTypes
from pipeline_telemetry.helper import is_telemetry_counter
from pipeline_telemetry.main import Telemetry
from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings import settings as st
from pipeline_telemetry.settings.data_class import TelemetryCounter


@pytest.fixture
def telemetry_inst():
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    return telemetry_inst


def test_telemetry_counter_exists():
    """check that TelemetryCounter class exists"""
    assert TelemetryCounter


def test_add_to_method():
    """
    Test that add_method on a telemetry counter adds the telemetry counter
    to given object with a _telemetry attribute
    """
    sub_process = TEST_TELEMETRY_COUNTER_INC_2.sub_process
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)

    class ClassToTestAddTo():
        _telemetry = telemetry

    obj_with_telemetry = ClassToTestAddTo()

    # ensure sub process is initialized in object's telemetry
    telemetry._initialize_sub_process(sub_process)

    # run add_to method on a Telemetry counter
    TEST_TELEMETRY_COUNTER_INC_2.add_to(obj_with_telemetry)
    assert sub_process in obj_with_telemetry._telemetry.telemetry
    assert obj_with_telemetry._telemetry.get(
        sub_process)["test_counter"] == 2


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
    assert telemetry_inst.get("RETRIEVE_RAW_DATA")[st.ERRORS_KEY]["HAS_KEY_ERR_0001"] == 1


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


def test_is_telemetry_counter_returns_false():
    """
    Test is_telemetry_counter method returns False if counter is not an instance
    off TelemetryCounter or subclass of TelemetryCounter.
    """
    assert not is_telemetry_counter("1")


def test_is_telemetry_counter_returns_true():
    """
    Test is_telemetry_counter method returns True if counter is an instance of
    TelemetryCounter.
    """
    assert is_telemetry_counter(TEST_TELEMETRY_COUNTER)


def test_is_error_returns_true_on_error_code_sub_class():
    """
    Test is_error method returns True if error is an instance of ErrorCode.
    """

    class TelemetryCounterSubClass(TelemetryCounter):
        pass

    counter = TelemetryCounterSubClass(
        process_type=TEST_TELEMETRY_COUNTER.process_type,
        sub_process=TEST_TELEMETRY_COUNTER.sub_process,
        counter_name=TEST_TELEMETRY_COUNTER.counter_name,
    )

    assert is_telemetry_counter(counter)


def test_telemetry_counter_validate_sub_process():
    """
    Test validate_sub_process method returns None if sub process is in scope of
    process_type.
    """
    assert TEST_TELEMETRY_COUNTER.validate_sub_process() is None


def test_validate_sub_process_raises_exception():
    """
    Test validate_sub_process method raises exception if sub process is not
    in scope of process_type.
    """
    counter = TelemetryCounter(
        process_type=TEST_TELEMETRY_COUNTER.process_type,
        sub_process="sub process not in scope of process_type",
        counter_name=TEST_TELEMETRY_COUNTER.counter_name,
    )

    with pytest.raises(exceptions.InvalidSubProcessForProcessType):
        counter.validate_sub_process()


def test_validate_sub_process_with_multiple_process_types():
    """
    Test validate_sub_process method returns None if sub process is in scope of
    one of the given process_types.
    """
    counter = TelemetryCounter(
        process_types=[ProcessTypes.CREATE_DATA_FROM_URL, ProcessTypes.UPLOAD_DATA],
        sub_process="DATA_UPLOAD",
        counter_name=TEST_TELEMETRY_COUNTER.counter_name,
    )
    assert counter.validate_sub_process() is None


def test_all_process_types_with_multiple_entries():
    """
    Test validate_sub_process method returns None if sub process is in scope of
    one of the given process_types.
    """
    counter = TelemetryCounter(
        process_types=[ProcessTypes.CREATE_DATA_FROM_URL, ProcessTypes.UPLOAD_DATA],
        sub_process="DATA_UPLOAD",
        counter_name=TEST_TELEMETRY_COUNTER.counter_name,
    )
    assert None not in counter.all_process_types
    assert ProcessTypes.CREATE_DATA_FROM_URL in counter.all_process_types
    assert ProcessTypes.UPLOAD_DATA in counter.all_process_types


def test_all_process_types_with_single_entry():
    """
    Test validate_sub_process method returns None if sub process is in scope of
    one of the given process_types.
    """
    counter = TelemetryCounter(
        process_type=ProcessTypes.CREATE_DATA_FROM_URL,
        sub_process="DATA_UPLOAD",
        counter_name=TEST_TELEMETRY_COUNTER.counter_name,
    )
    assert None not in counter.all_process_types
    assert ProcessTypes.CREATE_DATA_FROM_URL in counter.all_process_types
