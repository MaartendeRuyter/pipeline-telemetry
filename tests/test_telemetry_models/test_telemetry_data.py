"""
Module to test telemetry main class for pipeline telemetry module.
"""

from test_data import TEST_ERROR_CODE, TEST_ERROR_CODE_2

from pipeline_telemetry.data_classes import TelemetryData
from pipeline_telemetry.settings import settings as st


def test_telemetry_data_exists():
    """check that TelemetryData class exists"""
    assert TelemetryData


def test_telemetry_data_inc_base_count():
    tel_data = TelemetryData()
    assert getattr(tel_data, st.BASE_COUNT_KEY) == 0
    tel_data.increase_base_count(increment=1)
    assert getattr(tel_data, st.BASE_COUNT_KEY) == 1


def test_telemetry_data_inc_fail_count():
    tel_data = TelemetryData()
    assert getattr(tel_data, st.FAIL_COUNT_KEY) == 0
    tel_data.increase_fail_count(increment=1)
    assert getattr(tel_data, st.FAIL_COUNT_KEY) == 1


def test_telemetry_data_inc_errors_count():
    tel_data = TelemetryData()
    tel_data.increase_error_count(increment=1, error_code=TEST_ERROR_CODE)
    assert getattr(tel_data, st.ERRORS_KEY)[TEST_ERROR_CODE.code] == 1


def test_telemetry_data_inc_custom_count():
    tel_data = TelemetryData()
    tel_data.increase_custom_count(increment=1, counter="counter")
    assert getattr(tel_data, st.COUNTERS_KEY)["counter"] == 1


def test_add_telemetry_custom_count_data():
    tel_data_1 = TelemetryData()
    tel_data_2 = TelemetryData()
    tel_data_1.increase_custom_count(increment=1, counter="counter")
    tel_data_2.increase_custom_count(increment=2, counter="counter")
    tel_data_1.increase_custom_count(increment=3, counter="counter_1")
    tel_data_2.increase_custom_count(increment=4, counter="counter_2")
    tel_data_1 += tel_data_2
    assert getattr(tel_data_1, st.COUNTERS_KEY)["counter"] == 3
    assert getattr(tel_data_1, st.COUNTERS_KEY)["counter_1"] == 3
    assert getattr(tel_data_1, st.COUNTERS_KEY)["counter_2"] == 4


def test_add_telemetry_base_and_fail_count_data():
    tel_data_1 = TelemetryData()
    tel_data_2 = TelemetryData()
    tel_data_1.increase_base_count(increment=1)
    tel_data_2.increase_base_count(increment=2)
    tel_data_1.increase_fail_count(increment=3)
    tel_data_2.increase_fail_count(increment=4)
    tel_data_1 += tel_data_2
    assert getattr(tel_data_1, st.BASE_COUNT_KEY) == 3
    assert getattr(tel_data_1, st.FAIL_COUNT_KEY) == 7


def test_add_telemetry_error_count_data():
    tel_data_1 = TelemetryData()
    tel_data_2 = TelemetryData()
    tel_data_1.increase_error_count(increment=1, error_code=TEST_ERROR_CODE)
    tel_data_2.increase_error_count(increment=2, error_code=TEST_ERROR_CODE)
    tel_data_2.increase_error_count(increment=4, error_code=TEST_ERROR_CODE_2)
    tel_data_1 += tel_data_2
    assert getattr(tel_data_1, st.ERRORS_KEY)[TEST_ERROR_CODE.code] == 3
    assert getattr(tel_data_1, st.ERRORS_KEY)[TEST_ERROR_CODE_2.code] == 4
