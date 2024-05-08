"""
Module to test telemetry model class for pipeline telemetry module.
"""

import pytest
from test_data import DEFAULT_TELEMETRY_MODEL_PARAMS

from pipeline_telemetry.data_classes import TelemetryModel
from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings import settings as st

# pylint: disable=protected-access


def test_telemetry_model_exists():
    """check that TelemetryModel class exists"""
    assert TelemetryModel


def test_check_telemetry_type_raises_exception_with_inv_type():
    telemetry_params = DEFAULT_TELEMETRY_MODEL_PARAMS.copy()
    telemetry_params[st.TELEMETRY_TYPE_KEY] = "invalid"
    with pytest.raises(exceptions.InvalidTelemetryType):
        TelemetryModel(**telemetry_params)._check_telemetry_type()


def test_telemetry_model_can_be_added():
    tel_model_1 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_2 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_added = tel_model_1 + tel_model_2
    assert isinstance(tel_model_added, TelemetryModel)


def test_telemetry_model_addition_adds_aggregation_counter():
    """
    Test that adding up to telemetry model instances return a Telemetry
    """
    tel_model_1 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_2 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_added = tel_model_1 + tel_model_2
    aggregation_data = tel_model_added.telemetry[st.AGGREGATION_KEY]
    assert getattr(aggregation_data, st.BASE_COUNT_KEY) == 1


def test_telemetry_model_addition_aggregates_custom_counters():
    """
    Test that adding up to telemetry model instances returns a TelemetryModel
    instance with aggregated Traffic Ligth counters in aggregation telemetry
    subprocess.
    """
    tel_model_1 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_2 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_3 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_2.get_sub_process_data("sub_process").increase_custom_count(
        increment=1, counter="counter_1"
    )
    tel_model_2.get_sub_process_data("sub_process").increase_custom_count(
        increment=2, counter="counter_2"
    )
    tel_model_3.get_sub_process_data("sub_process").increase_custom_count(
        increment=2, counter="counter_1"
    )
    tel_model_3.get_sub_process_data("sub_process").increase_custom_count(
        increment=4, counter="counter_3"
    )
    tel_model_added = tel_model_1 + tel_model_2
    tel_model_added += tel_model_3
    aggregation_data = tel_model_added.telemetry[st.AGGREGATION_KEY]
    telemetry_data = tel_model_added.telemetry["sub_process"]
    assert getattr(aggregation_data, st.COUNTERS_KEY)[st.TRAFIC_LIGHT_COLOR_GREEN] == 2
    assert getattr(telemetry_data, st.COUNTERS_KEY) == {
        "counter_1": 3,
        "counter_2": 2,
        "counter_3": 4,
    }


def test_telemetry_model_addition_aggregates_errors():
    """
    Test that adding up to telemetry model instances returns a TelemetryModel
    instance with aggregated errors.
    """
    tel_model_1 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_2 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_3 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_2.get_sub_process_data("sub_process")._increase_error_count(
        increment=1, error_code_key="error_1"
    )
    tel_model_2.get_sub_process_data("sub_process")._increase_error_count(
        increment=2, error_code_key="error_2"
    )
    tel_model_3.get_sub_process_data("sub_process")._increase_error_count(
        increment=2, error_code_key="error_1"
    )
    tel_model_3.get_sub_process_data("sub_process")._increase_error_count(
        increment=4, error_code_key="error_3"
    )
    tel_model_added = tel_model_1 + tel_model_2
    tel_model_added += tel_model_3
    telemetry_data = tel_model_added.telemetry["sub_process"]
    assert getattr(telemetry_data, st.ERRORS_KEY) == {
        "error_1": 3,
        "error_2": 2,
        "error_3": 4,
    }


def test_telemetry_model_addition_aggregates_traffic_lights():
    """
    Test that adding up to telemetry model instances returns a TelemetryModel
    instance with aggregated Traffic Ligth counters in aggregation telemetry
    subprocess.
    """
    tel_model_1 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_2 = TelemetryModel(
        **(
            DEFAULT_TELEMETRY_MODEL_PARAMS
            | {"traffic_light": st.TRAFIC_LIGHT_COLOR_ORANGE}
        )
    )
    tel_model_3 = TelemetryModel(
        **(
            DEFAULT_TELEMETRY_MODEL_PARAMS
            | {"traffic_light": st.TRAFIC_LIGHT_COLOR_RED}
        )
    )
    tel_model_added = tel_model_1 + tel_model_2
    tel_model_added += tel_model_3
    aggregation_data = tel_model_added.telemetry[st.AGGREGATION_KEY]
    aggregation_data_counters = getattr(aggregation_data, st.COUNTERS_KEY)
    assert st.TRAFIC_LIGHT_COLOR_ORANGE in aggregation_data_counters
    assert st.TRAFIC_LIGHT_COLOR_RED in aggregation_data_counters
    assert aggregation_data_counters[st.TRAFIC_LIGHT_COLOR_RED] == 1
    assert aggregation_data_counters[st.TRAFIC_LIGHT_COLOR_ORANGE] == 1


def test_telemetry_model_addition_aggregates_io_time():
    """
    Test that adding up to telemetry model instances returns a TelemetryModel
    instance with aggregated io time rounded in seconds
    """
    tel_model_1 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_2 = TelemetryModel(
        **(DEFAULT_TELEMETRY_MODEL_PARAMS | {"io_time_in_seconds": 1.2})
    )
    tel_model_3 = TelemetryModel(
        **(DEFAULT_TELEMETRY_MODEL_PARAMS | {"io_time_in_seconds": 1.7})
    )
    tel_model_added = tel_model_1 + tel_model_2
    tel_model_added += tel_model_3
    aggregation_data = tel_model_added.telemetry[st.AGGREGATION_KEY]
    aggregation_data_counters = getattr(aggregation_data, st.COUNTERS_KEY)
    assert "io_time_in_seconds" in aggregation_data_counters
    assert aggregation_data_counters["io_time_in_seconds"] == 3


def test_telemetry_model_addition_aggregates_run_time():
    """
    Test that adding up to telemetry model instances returns a TelemetryModel
    instance with aggregated run time rounded in seconds
    """
    tel_model_1 = TelemetryModel(**DEFAULT_TELEMETRY_MODEL_PARAMS)
    tel_model_2 = TelemetryModel(
        **(DEFAULT_TELEMETRY_MODEL_PARAMS | {"run_time_in_seconds": 1.2})
    )
    tel_model_3 = TelemetryModel(
        **(DEFAULT_TELEMETRY_MODEL_PARAMS | {"run_time_in_seconds": 1.7})
    )
    tel_model_added = tel_model_1 + tel_model_2
    tel_model_added += tel_model_3
    aggregation_data = tel_model_added.telemetry[st.AGGREGATION_KEY]
    aggregation_data_counters = getattr(aggregation_data, st.COUNTERS_KEY)
    assert "run_time_in_seconds" in aggregation_data_counters
    assert aggregation_data_counters["run_time_in_seconds"] == 3
