"""Module to test pipeline telemetry helper methods.
"""
import test_data as td
from errors import ReturnValueWithErrorStatus, ReturnValueWithStatus

import pipeline_telemetry.helper as HP
from pipeline_telemetry import Telemetry, add_errors_from_return_value, \
    add_telemetry_counters_from_return_value, increase_base_count, \
    increase_fail_count, is_telemetry_counter, process_return_value
from pipeline_telemetry.settings.settings import BASE_COUNT_KEY, FAIL_COUNT_KEY


class HelperTest:
    pass


def test_add_result_value_with_status_without_errors():
    """
    Test adding the ResultValueWithStatus instance without an error in it, to
    the telemetry adds no errors to the telemetry object.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**td.DEFAULT_TELEMETRY_PARAMS)
    return_value_without_error = ReturnValueWithStatus(result=[])
    add_errors_from_return_value(
        object_with_telemetry=test_obj,
        sub_process="RETRIEVE_RAW_DATA",
        return_value=return_value_without_error)
    assert not test_obj._telemetry.get("RETRIEVE_RAW_DATA").get('errors')


def test_add_result_value_with_status_with_one_error():
    """
    Test adding the ResultValueWithStatus instance with an error in it to the
    telemetry adds the actual error to the telemetry object.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**td.DEFAULT_TELEMETRY_PARAMS)
    return_value_with_error = ReturnValueWithErrorStatus(
        error=td.TEST_ERROR_CODE)
    add_errors_from_return_value(
        object_with_telemetry=test_obj,
        sub_process="RETRIEVE_RAW_DATA",
        return_value=return_value_with_error)
    assert td.TEST_ERROR_CODE.code in \
        str(test_obj._telemetry.get("RETRIEVE_RAW_DATA").get('errors'))
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get('errors').get(
        td.TEST_ERROR_CODE.code) == 1


def test_add_result_value_with_status_with_errors():
    """
    Test adding the ResultValueWithStatus instance with 2 errors in it to the
    telemetry adds the actual errors to the telemetry object.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**td.DEFAULT_TELEMETRY_PARAMS)
    return_value_with_error = ReturnValueWithErrorStatus(
        error=td.TEST_ERROR_CODE)
    return_value_with_error.add_error(td.TEST_ERROR_CODE)
    add_errors_from_return_value(
        object_with_telemetry=test_obj,
        sub_process="RETRIEVE_RAW_DATA",
        return_value=return_value_with_error)
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get('errors').get(
        td.TEST_ERROR_CODE.code) == 2


def test_process_telemetry_counters_in_return_value():
    """
    Test that when a ResultValueWithStatus instance with 2 telemetry counters
    in the result is processed by process_telemetry_counters_in_return_value
    the telemetry counters are processed.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**td.DEFAULT_TELEMETRY_PARAMS)
    add_telemetry_counters_from_return_value(
        object_with_telemetry=test_obj,
        return_value=td.TEST_RETURN_VALUE)
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get(
        'errors') is not None
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get('test_counter') == 1


def test_process_telemetry_counters_in_return_value_returns_list():
    """
    Test that when a ResultValueWithStatus instance with 2 telemetry counters
    in the result is processed by process_telemetry_counters_in_return_value
    the result list without TelemetryCounters is returned.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**td.DEFAULT_TELEMETRY_PARAMS)
    res_without_telem_counters = add_telemetry_counters_from_return_value(
        object_with_telemetry=test_obj,
        return_value=td.TEST_RETURN_VALUE)
    assert res_without_telem_counters == [
        res for res in td.TEST_RETURN_VALUE.result
        if not is_telemetry_counter(res)]


def test_increase_base_count():
    """
    Test increase base count without increment increase base counter with 1 for
    a given sub process.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**td.DEFAULT_TELEMETRY_PARAMS)
    increase_base_count(
        object_with_telemetry=test_obj,
        sub_process="RETRIEVE_RAW_DATA")
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get(BASE_COUNT_KEY) == 1


def test_increase_base_count_with_increment():
    """
    Test increase base count with increment 2 increases base counter with 2 for
    a given sub process.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**td.DEFAULT_TELEMETRY_PARAMS)
    increase_base_count(
        object_with_telemetry=test_obj,
        sub_process="RETRIEVE_RAW_DATA",
        increment=2)
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get(BASE_COUNT_KEY) == 2


def test_increase_fail_count():
    """
    Test increase fail count without increment increases teh fail counter with
    1 for a given sub process.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**td.DEFAULT_TELEMETRY_PARAMS)
    test_obj._telemetry._initialize_sub_process("RETRIEVE_RAW_DATA")
    increase_fail_count(
        object_with_telemetry=test_obj,
        sub_process="RETRIEVE_RAW_DATA")
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get(FAIL_COUNT_KEY) == 1


def test_process_return_value(mocker):
    """
    Test that process_return_value returns helper method returns the list
    retrieved add_telemetry_counters_from_return_value helper method.
    """
    mocker.patch(
        ("pipeline_telemetry.helper."
         "add_telemetry_counters_from_return_value"),
        return_value=['list with values'])
    mocker.patch(
        ("pipeline_telemetry.helper."
         "add_errors_from_return_value"),
        return_value=None)
    assert process_return_value(
        object_with_telemetry=None,
        sub_process="na for this test",
        return_value=td.TEST_RETURN_VALUE) == ['list with values']


def test_process_return_value_processes_the_errors(mocker):
    """
    Test process_return_value calls the add_errors_from_return_value method.
    """
    mocker.patch(
        ("pipeline_telemetry.helper."
         "add_telemetry_counters_from_return_value"),
        return_value=None)
    mocker.patch(
        ("pipeline_telemetry.helper."
         "add_errors_from_return_value"),
        return_value=None)
    process_telemetry_spy = mocker.spy(
        HP, "add_telemetry_counters_from_return_value")

    process_return_value(
        object_with_telemetry=None,
        sub_process="na for this test",
        return_value=td.TEST_RETURN_VALUE)
    assert process_telemetry_spy.called


def test_process_return_value_processes_the_telemetry_counters(mocker):
    """
    Test process_return_value calls the
    process_telemetry_counters_in_return_value method.
    """
    mocker.patch(
        ("pipeline_telemetry.helper."
         "add_telemetry_counters_from_return_value"),
        return_value=None)
    mocker.patch(
        ("pipeline_telemetry.helper."
         "add_errors_from_return_value"),
        return_value=None)
    process_telemetry_spy = mocker.spy(
        HP, "add_telemetry_counters_from_return_value")

    process_return_value(
        object_with_telemetry=None,
        sub_process="na for this test",
        return_value=td.TEST_RETURN_VALUE)
    assert process_telemetry_spy.called
