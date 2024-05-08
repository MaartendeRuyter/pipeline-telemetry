"""
Module to test telemetry main class for pipeline telemetry module.
"""

from datetime import datetime

import pytest
from test_data import DEFAULT_TELEMETRY_PARAMS, TEST_PROCESS_TYPE_3

from pipeline_telemetry import Telemetry
from pipeline_telemetry.data_classes import TelemetryData, TelemetryModel
from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings import settings as st
from pipeline_telemetry.settings.data_class import ProcessType
from pipeline_telemetry.storage.generic import AbstractTelemetryStorage
from pipeline_telemetry.storage.memory import TelemetryInMemoryStorage

# pylint: disable=protected-access


def test_telemetry_exists():
    """check that Telemetry class exists"""
    assert Telemetry


def test_telemetry_instance_creation():
    """check that Telemetry instance can be created using default_params"""
    assert Telemetry(**DEFAULT_TELEMETRY_PARAMS)


def test_telemetry_instance_has_telemetry_type_property():
    """check that Telemetry instance has a telemetry_type property"""
    assert (
        Telemetry(**DEFAULT_TELEMETRY_PARAMS).telemetry_type
        == st.DEFAULT_TELEMETRY_TYPE
    )


def test_telemetry_instance_has_source_name_property():
    """check that Telemetry instance has a source_name property"""
    assert Telemetry(**DEFAULT_TELEMETRY_PARAMS).source_name == "load_weather_data"


def test_telemetry_instance_has_category_property():
    """check that Telemetry instance has a source_name property"""
    assert Telemetry(**DEFAULT_TELEMETRY_PARAMS).category == "WEATHER"


def test_telemetry_instance_has_sub_category_property():
    """check that Telemetry instance has a sub_category property"""
    assert Telemetry(**DEFAULT_TELEMETRY_PARAMS).sub_category == "DAILY_PREDICTIONS"


def test_telemetry_instance_has_traffic_light_property():
    """
    Test that Telemetry instance has a traffic_light property that is
    set to the default value."""
    assert (
        Telemetry(**DEFAULT_TELEMETRY_PARAMS).traffic_light
        == st.DEFAULT_TRAFIC_LIGHT_COLOR
    )


def test_telemetry_instance_has_sub_process_types_property():
    """check that Telemetry instance has a sub_processes_types property"""
    assert (
        Telemetry(**DEFAULT_TELEMETRY_PARAMS).sub_process_types
        == DEFAULT_TELEMETRY_PARAMS["process_type"].sub_processes
    )


def test_telemetry_instance_has_telemetry_property():
    """
    Test that a Telemetry instance has a telemetry property that is an
    instance of class TelemetryModel"""
    assert isinstance(Telemetry(**DEFAULT_TELEMETRY_PARAMS).telemetry, TelemetryModel)


def test_telemetry_instance_has_a_start_date_time_property():
    """
    Test that a Telemetry instance has a start_date_time property that is an
    instance of class TelemetryModel"""
    assert isinstance(Telemetry(**DEFAULT_TELEMETRY_PARAMS).start_date_time, datetime)


def test_telemetry_instance_has_io_time_in_seconds_property():
    """check that Telemetry instance has a io_time_in_seconds property"""
    assert hasattr(Telemetry(**DEFAULT_TELEMETRY_PARAMS), st.IO_TIME_KEY)


def test_telemetry_instance_creation_raises_excption():
    """
    Check that Telemetry instance creation raises exception with non registered
    ProcessType.
    """
    process_type = ProcessType(process_type="not_registered", subtypes=["test"])
    telemetry_params = {
        "category": "WEATHER",
        "sub_category": "DAILY_PREDICTIONS",
        "source_name": "load_weather_data",
        "process_type": process_type,
    }
    with pytest.raises(exceptions.ProcessTypeNotRegistered):
        Telemetry(**telemetry_params)


def test_telemetry_instance_raises_exception_with_invalid_process_type():
    """
    check that Telemetry instance creation raises exception when invalid
    process_type is used
    """
    telemetry_params = DEFAULT_TELEMETRY_PARAMS | {"process_type": "invalid"}
    with pytest.raises(exceptions.ProcessTypeMustBeOfClassProcessType):
        Telemetry(**telemetry_params)


def test_telemetry_instance_sets_io_time_to_zero():
    """
    check that Telemetry instance initially has zero io_time.
    """
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    assert getattr(telemetry, st.IO_TIME_KEY) == 0


def test_telemetry_instance_increase_io_time():
    """
    check increase_io_time method increase the io_time of a Telemetry instance
    with given float value.
    """
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry.increase_io_time(1.1)
    assert getattr(telemetry, st.IO_TIME_KEY) == 1.1


def test_initialize_new_sub_process_in_telemetry_instance():
    """
    Test that a new sub_process can be initialized.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst._initialize_sub_process("RETRIEVE_RAW_DATA")
    assert "RETRIEVE_RAW_DATA" in telemetry_inst.telemetry_data


def test_initialize_a_sub_process_twice_raises_an_exception():
    """
    Test that a new sub_process can be initialized only once.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst._initialize_sub_process("RETRIEVE_RAW_DATA")
    with pytest.raises(exceptions.SubProcessAlreadyInitialized):
        telemetry_inst._initialize_sub_process("RETRIEVE_RAW_DATA")


def test_initializing_non_existing_sub_process_raises_exception():
    """
    Check that initializing a non existing sub_process raises an excpetion.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    with pytest.raises(exceptions.InvalidSubProcess):
        telemetry_inst._initialize_sub_process("Non existing")


def test_get_telemetry_data_sub_process():
    """
    Check get method returns a TelemetryData instance for an initialized.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst._initialize_sub_process("RETRIEVE_RAW_DATA")
    assert isinstance(telemetry_inst.get("RETRIEVE_RAW_DATA"), TelemetryData)


def test_increase_sub_process_base_count():
    """
    Check that a sub process base count can be increased.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    assert getattr(telemetry_inst.get("RETRIEVE_RAW_DATA"), st.BASE_COUNT_KEY) == 1


def test_increase_sub_process_fail_count():
    """
    Check that a sub process base count can be increased.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_fail_count("RETRIEVE_RAW_DATA")
    assert getattr(telemetry_inst.get("RETRIEVE_RAW_DATA"), st.FAIL_COUNT_KEY) == 1


def test_increase_non_exsiting_sub_process_raises_exception():
    """
    Check that a add a based count for a non existing sub process raises
    an excpetion
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    with pytest.raises(exceptions.InvalidSubProcess):
        telemetry_inst.increase_sub_process_base_count("Non exsiting")


def test_increase_sub_process_base_count_to_telemetry():
    """
    Check that an existing sub process base count can be inreased multiple
    times and with different values
    """
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    telemetry.increase_sub_process_base_count("RETRIEVE_RAW_DATA", increment=2)
    assert getattr(telemetry.get("RETRIEVE_RAW_DATA"), st.BASE_COUNT_KEY) == 3


def test_increase_sub_process_count_not_allowed_with_closed_telemetry():
    """
    check that a sub process base count can be added to th eTelemetry instance
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    telemetry_inst.save_and_close()
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed):
        telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")


def test_can_not_close_closed_telemetry_instance():
    """
    check that a closed telemetry instance can not be closed again
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.save_and_close()
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed):
        telemetry_inst.save_and_close()


def test_increase_sub_process_fail_not_allowed_with_closed_telemetry():
    """
    check that a sub process base count can be added to th eTelemetry instance
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    telemetry_inst.save_and_close()
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed):
        telemetry_inst.increase_sub_process_fail_count("RETRIEVE_RAW_DATA")


def test_sub_process_custom_count_not_allowed_with_closed_telemetry():
    """
    check that a sub process custom count method raises an excpetion
    when telementry object has been closed
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    telemetry_inst.save_and_close()
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed):
        telemetry_inst.increase_sub_process_custom_count(
            sub_process="RETRIEVE_RAW_DATA", custom_counter="test_counter"
        )


def test_add_sub_process_custom_counter_to_telemetry():
    """
    Check that a custom counter can be added to a subprocess.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_custom_count(
        custom_counter="network_error", sub_process="RETRIEVE_RAW_DATA"
    )
    tel_data = telemetry_inst.get("RETRIEVE_RAW_DATA")
    assert tel_data.counters["network_error"] == 1


def test_increase_existing_sub_process_custom_counter_to_telemetry():
    """
    Check that a existing custom counter can be increased
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    for _ in [1, 2]:
        telemetry_inst.increase_sub_process_custom_count(
            custom_counter="network_error", sub_process="RETRIEVE_RAW_DATA"
        )

    tel_data = telemetry_inst.get("RETRIEVE_RAW_DATA")
    assert tel_data.counters["network_error"] == 2


def test_increase_sub_process_custom_count_with_two():
    """
    check that increase_sub_process_custom_count method creates counter
    with initial value 2
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    telemetry_inst.increase_sub_process_custom_count(
        sub_process="RETRIEVE_RAW_DATA", custom_counter="test_counter", increment=2
    )

    tel_data = telemetry_inst.get("RETRIEVE_RAW_DATA")

    assert tel_data.counters["test_counter"] == 2


def test_close_telemetry_instance_sets_run_time(mocker):
    """
    check that closing the telemetry sets the run_time
    """
    mocker.patch(
        (
            "pipeline_telemetry.storage.memory."
            "TelemetryInMemoryStorage.store_telemetry"
        ),
        return_value=None,
    )
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count("RETRIEVE_RAW_DATA")
    telemetry_result = telemetry_inst.save_and_close()
    assert float(getattr(telemetry_result, st.RUN_TIME)) > 0


def test_close_telemetry_instance_calls_store_telemetry(mocker):
    """
    check that closing the telemetry sets the run_time
    """
    mocker.patch(
        (
            "pipeline_telemetry.storage.memory."
            "TelemetryInMemoryStorage.store_telemetry"
        ),
        return_value=None,
    )
    _store_telemetry_spy = mocker.spy(TelemetryInMemoryStorage, "store_telemetry")
    Telemetry(**DEFAULT_TELEMETRY_PARAMS).save_and_close()
    assert _store_telemetry_spy.called


def test_get_storage_class_returns_in_memory_storage_by_default():
    """
    check that _get_storage_class method returns TelemetryInMemoryStorage
    instance if no storage class is provided
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    assert issubclass(telemetry_inst._storage_class, TelemetryInMemoryStorage)


def test_storage_class_returns_the_correct_storage_class():
    """
    check that storage_class attribute returns the correct
    Storage class.
    """

    # pylint: disable=too-few-public-methods
    class TestStorage(AbstractTelemetryStorage):
        """test class"""

        def store_telemetry(self, telemetry):
            """test method"""
            return None

    telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy()
    telemetry_params["storage_class"] = TestStorage
    telemetry_inst = Telemetry(**telemetry_params)
    assert telemetry_inst.storage_class is TestStorage


def test_storage_class_close_method_closes_db():
    """
    check that _get_storage_class method returns an instance of
    Storage class provided
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    storage_instance = telemetry_inst.storage_class()
    storage_instance.close_db()
    assert storage_instance.db_in_memory is None
    assert storage_instance.db_cursor is None


def test_new_telemetry_has_default_traffic_light_color():
    """New telemetry instance should have default trafic light color."""
    assert (
        Telemetry(**DEFAULT_TELEMETRY_PARAMS).telemetry.traffic_light
        == st.DEFAULT_TRAFIC_LIGHT_COLOR
    )


def test_set_telemetry_traffic_light_to_orange():
    """New telemetry instance traffic light property can be set to orange."""
    tele_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    tele_inst.set_orange_traffic_light()
    assert tele_inst.telemetry.traffic_light == st.TRAFIC_LIGHT_COLOR_ORANGE


def test_set_telemetry_traffic_light_to_red():
    """New telemetry instance traffic light property can be set to red."""
    tele_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    tele_inst.set_red_traffic_light()
    assert tele_inst.telemetry.traffic_light == st.TRAFIC_LIGHT_COLOR_RED


def test_sub_process_is_initialized_returns_false():
    """
    Check that _sub_process_is_initialized returns False when sub process is not
    yet initialized
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    assert not telemetry_inst._sub_process_is_initialized("RETRIEVE_RAW_DATA")


def test_sub_process_is_initialized_returns_true():
    """
    Check that _sub_process_is_initialized returns true when sub process is
    initialized
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst._initialize_sub_process("RETRIEVE_RAW_DATA")
    assert telemetry_inst._sub_process_is_initialized("RETRIEVE_RAW_DATA")


def test_sub_process_not_yet_initialized_returns_false():
    """
    Check that _sub_process_not_yet_initialized returns False when sub process
    initialized
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst._initialize_sub_process("RETRIEVE_RAW_DATA")
    assert not telemetry_inst._sub_process_not_yet_initialized("RETRIEVE_RAW_DATA")


def test_sub_process_not_yet_initialized_returns_true():
    """
    Check that _sub_process_not_yet_initialized returns false when sub process
    is not yet initialized
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    assert telemetry_inst._sub_process_not_yet_initialized("RETRIEVE_RAW_DATA")


def test_instanciating_telemetry_with_invalid_telemetry_type():
    """
    Test that instanciating a telemetry object with invalid telemetry type
    raises an exception.
    """
    telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy()
    telemetry_params["telemetry_type"] = "invalid_type"
    with pytest.raises(exceptions.InvalidTelemetryType):
        Telemetry(**telemetry_params)


def test_validate_process_type_returns_none_with_valid_process_type():
    """
    Test that _valid_process_type validates a valid process_type by returning
    None.
    """
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    assert telemetry._validate_process_type() is None


def test_validate_process_raises_exception_process_type_of_invalid_type():
    """
    Test that _valid_process_type raises exception when process_type is not
    of type ProcessType.
    """
    telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy()
    telemetry_params["process_type"] = "process_type_of_invalid_type"
    with pytest.raises(exceptions.ProcessTypeMustBeOfClassProcessType):
        Telemetry(**telemetry_params)


def test_validate_process_raises_exception_if_process_type_not_registered():
    """
    Test that _valid_process_type raises exception when process_type is not
    registered.
    """
    telemetry_params = DEFAULT_TELEMETRY_PARAMS.copy()
    telemetry_params["process_type"] = TEST_PROCESS_TYPE_3
    with pytest.raises(exceptions.ProcessTypeNotRegistered):
        Telemetry(**telemetry_params)
