"""
Module to test telemetry main class for pipeline telemetry module.
"""
from test_data import TEST_ERROR_CODE

from pipeline_telemetry.settings import settings as st
from pipeline_telemetry.telemetry_model import TelemetryData


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
    tel_data.increase_custom_count(increment=1, counter='counter')
    assert getattr(tel_data, st.COUNTERS_KEY)['counter'] == 1
