"""Module to test pipeline telemetry helper methods.
"""
from errors import ReturnValueWithErrorStatus, ReturnValueWithStatus
from test_data import DEFAULT_TELEMETRY_PARAMS, TEST_ERROR_CODE

from pipeline_telemetry import Telemetry, add_errors_from_return_value, \
    increase_base_count, increase_fail_count
from pipeline_telemetry.settings.settings import BASE_COUNT_KEY, FAIL_COUNT_KEY


class HelperTest:
    pass


def test_add_result_value_with_status_without_errors():
    """
    Test adding the ResultValueWithStatus instance without an error in it, to
    the telemetry adds no errors to the telemetry object.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
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
    test_obj._telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    return_value_with_error = ReturnValueWithErrorStatus(error=TEST_ERROR_CODE)
    add_errors_from_return_value(
        object_with_telemetry=test_obj,
        sub_process="RETRIEVE_RAW_DATA",
        return_value=return_value_with_error)
    assert TEST_ERROR_CODE.code in \
        str(test_obj._telemetry.get("RETRIEVE_RAW_DATA").get('errors'))
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get('errors').get(
        TEST_ERROR_CODE.code) == 1


def test_add_result_value_with_status_with_errors():
    """
    Test adding the ResultValueWithStatus instance with 2 errors in it to the
    telemetry adds the actual errors to the telemetry object.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    return_value_with_error = ReturnValueWithErrorStatus(error=TEST_ERROR_CODE)
    return_value_with_error.add_error(TEST_ERROR_CODE)
    add_errors_from_return_value(
        object_with_telemetry=test_obj,
        sub_process="RETRIEVE_RAW_DATA",
        return_value=return_value_with_error)
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get('errors').get(
        TEST_ERROR_CODE.code) == 2


def test_increase_base_count():
    """
    Test increase base count without increment increase base counter with 1 for
    a given sub process.
    """
    test_obj = HelperTest()
    test_obj._telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
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
    test_obj._telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
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
    test_obj._telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    test_obj._telemetry._initialize_sub_process("RETRIEVE_RAW_DATA")
    increase_fail_count(
        object_with_telemetry=test_obj,
        sub_process="RETRIEVE_RAW_DATA")
    assert test_obj._telemetry.get("RETRIEVE_RAW_DATA").get(FAIL_COUNT_KEY) == 1
