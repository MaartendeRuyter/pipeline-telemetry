"""
Module to test telemetry main class for pipeline telemetry module.
"""
from datetime import datetime

import pytest
from test_data import DEFAULT_TELEMETRY_PARAMS

from pipeline_telemetry.main import FAIL_COUNT_KEY, Telemetry, mongo_telemetry
from pipeline_telemetry.settings import exceptions, settings
from pipeline_telemetry.settings.data_class import ProcessType
from pipeline_telemetry.storage.generic import AbstractTelemetryStorage
from pipeline_telemetry.storage.memory import TelemetryInMemoryStorage
from pipeline_telemetry.storage.mongo import TelemetryMongoStorage

# pylint: disable=protected-access


def test_telemetry_exists():
    """ check that Telemetry class exists """
    assert Telemetry


def test_telemetry_instance_creation():
    """ check that Telemetry instance can be created using default_params """
    assert Telemetry(**DEFAULT_TELEMETRY_PARAMS).process_name == \
        'load_weather_data'


def test_telemetry_instance_creation_raises_excption():
    """
    Check that Telemetry instance creation raises exception with non registered
    ProcessType.
    """
    process_type = ProcessType(
        process_type='not_registered',
        subtypes=['test'])
    telemetry_params = {
        'process_name': 'load_weather_data',
        'process_type': process_type
    }
    with pytest.raises(exceptions.ProcessTypeNotRegistered):
        Telemetry(**telemetry_params)


def test_telemetry_instance_has_telemetry_property():
    """ check that Telemetry instance has a telemetry property """
    assert Telemetry(**DEFAULT_TELEMETRY_PARAMS).telemetry


def test_telemetry_instance_has_sub_process_types_property():
    """
    check that Telemetry instance has a sub_process_types property that return
    a dict with all sub_process_types
    """
    assert isinstance(
        Telemetry(**DEFAULT_TELEMETRY_PARAMS).sub_process_types, list)
    assert Telemetry(**DEFAULT_TELEMETRY_PARAMS).sub_process_types == \
        settings.DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES


def test_telemetry_instance_raises_exception_with_invalid_process_type():
    """
    check that Telemetry instance creation raises exception when invalid
    process_type is used
    """
    telemetry_params = DEFAULT_TELEMETRY_PARAMS | {'process_type': 'invalid'}
    with pytest.raises(exceptions.ProcessTypeMustBeOfClassProcessType):
        Telemetry(**telemetry_params)


def test_telemetry_instance_sets_start_time():
    """
    check that Telemetry instance has a start_date_time
    """
    telemetry = Telemetry(**DEFAULT_TELEMETRY_PARAMS).telemetry
    assert isinstance(telemetry.get('start_date_time'), datetime)


def test_increase_new_sub_process_base_count_to_telemetry():
    """
    Check that a new sub process base count can be added to a Telemetry
    instance.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    assert 'RETRIEVE_RAW_DATA' in telemetry_inst.telemetry
    assert telemetry_inst.get('RETRIEVE_RAW_DATA')['base_counter'] == 1


def test_increase_non_exsiting_sub_process_raises_exception():
    """
    Check that a add a based count for a non existing sub process raises
    an excpetion
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    with pytest.raises(exceptions.InvalidSubProcess):
        telemetry_inst.increase_sub_process_base_count('Non exsiting')


def test_increase_sub_process_base_count_to_telemetry():
    """
    Check that an existing sub process base count can be inreased.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    assert telemetry_inst.get('RETRIEVE_RAW_DATA')['base_counter'] == 1
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    assert telemetry_inst.get('RETRIEVE_RAW_DATA')['base_counter'] == 2


def test_increase_sub_process_count_not_allowed_with_closed_telemetry():
    """
    check that a sub process base count can be added to th eTelemetry instance
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry_inst.save_and_close()
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed):
        telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')


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
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry_inst.save_and_close()
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed):
        telemetry_inst.increase_sub_process_fail_count('RETRIEVE_RAW_DATA')


def test_sub_process_custom_count_not_allowed_with_closed_telemetry():
    """
    check that a sub process custom count method raises an excpetion
    when telementry object has been closed
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry_inst.save_and_close()
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed):
        telemetry_inst.increase_sub_process_custom_count(
            sub_process='RETRIEVE_RAW_DATA',
            custom_counter='test_counter')


def test_custom_count_not_allowed_with_closed_telemetry():
    """
    check that a custom count method raises an excpetion
    when telementry object has been closed
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.save_and_close()
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed):
        telemetry_inst.increase_custom_count(
            custom_counter='test_counter')


def test_add_sub_process_fail_count_to_telemetry():
    """
    check that a sub process fail count can be increased
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry_inst.increase_sub_process_fail_count('RETRIEVE_RAW_DATA')
    assert telemetry_inst.telemetry['RETRIEVE_RAW_DATA'][FAIL_COUNT_KEY] == 1


def test_add_sub_process_fail_count_raises_excpetion():
    """
    check that a sub process fail count raises an excpetion when sub_process
    has not yet been initialized by increase_sub_process_base_count(sub_process)
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    with pytest.raises(exceptions.BaseCountForSubProcessNotAdded):
        telemetry_inst.increase_sub_process_fail_count('RETRIEVE_RAW_DATA')


def test_add_custom_counter_to_telemetry():
    """
    check that a custom counter can be added to the telemetry instance
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_custom_count('network_error')
    assert telemetry_inst.telemetry['network_error'] == 1


def test_add_sub_process_custom_counter_to_telemetry():
    """
    Check that a custom counter can be added to a subprocess.
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry_inst.increase_sub_process_custom_count(
        custom_counter='network_error',
        sub_process='RETRIEVE_RAW_DATA')
    assert telemetry_inst.get('RETRIEVE_RAW_DATA')['network_error'] == 1


def test_increase_existing_sub_process_custom_counter_to_telemetry():
    """
    Check that a existing custom counter can be icnrease
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    for _ in [1, 2]:
        telemetry_inst.increase_sub_process_custom_count(
            custom_counter='network_error',
            sub_process='RETRIEVE_RAW_DATA')

    assert telemetry_inst.get('RETRIEVE_RAW_DATA')['network_error'] == 2


def test_increase_custom_counter_to_telemetry():
    """
    check that a custom counter once created can be increased with any value
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_custom_count('network_error')
    telemetry_inst.increase_custom_count('network_error', 2)
    assert telemetry_inst.telemetry['network_error'] == 3


def test_increase_sub_process_custom_count_raises_excpetion():
    """
    check that increase_sub_process_custom_count method raises an excpetion
    when sub_process has not yet been initialized
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    with pytest.raises(exceptions.BaseCountForSubProcessNotAdded):
        telemetry_inst.increase_sub_process_custom_count(
            sub_process='RETRIEVE_RAW_DATA',
            custom_counter='test_counter')


def test_increase_sub_process_custom_count_with_two():
    """
    check that increase_sub_process_custom_count method creates counter
    with initial value 2
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry_inst.increase_sub_process_custom_count(
        sub_process='RETRIEVE_RAW_DATA',
        custom_counter='test_counter',
        increment=2)
    assert telemetry_inst.telemetry[
        'RETRIEVE_RAW_DATA']['test_counter'] == 2


def test_close_telemetry_instance_sets_run_time(mocker):
    """
    check that closing the telemetry sets the run_time
    """
    mocker.patch(
        ("pipeline_telemetry.storage.memory."
         "TelemetryInMemoryStorage.store_telemetry"),
        return_value=None)
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    telemetry_inst.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry_result = telemetry_inst.save_and_close()
    assert float(telemetry_result.get('run_time_in_seconds')) > 0


def test_close_telemetry_instance_calls_store_telemetry(mocker):
    """
    check that closing the telemetry sets the run_time
    """
    mocker.patch(
        ("pipeline_telemetry.storage.memory."
         "TelemetryInMemoryStorage.store_telemetry"),
        return_value=None)
    _store_telemetry_spy = mocker.spy(
        TelemetryInMemoryStorage, 'store_telemetry')
    Telemetry(**DEFAULT_TELEMETRY_PARAMS).save_and_close()
    assert _store_telemetry_spy.called


def test_get_storage_class_returns_in_memory_storage_by_default():
    """
    check that _get_storage_class method returns TelemetryInMemoryStorage
    instance if no storage class is provided
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    assert isinstance(
        telemetry_inst._get_storage_class(None), TelemetryInMemoryStorage)


def test_get_storage_class_raises_exception_if_invalid_class_is_provided():
    """
    check that _get_storage_class raises exception if storage class is provided
    that is not a subclass of AbstractTelemetryStorage
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    with pytest.raises(exceptions.StorageClassOfIncorrectType):
        telemetry_inst._get_storage_class(str)


def test_get_storage_class_returns_instance_of_storage_class():
    """
    check that _get_storage_class method returns an instance of
    Storage class provided
    """
    # pylint: disable=too-few-public-methods
    class TestStorage(AbstractTelemetryStorage):
        """ test class """

        def store_telemetry(self, telemetry):
            """ test method """
            return None

    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    assert isinstance(
        telemetry_inst._get_storage_class(TestStorage), TestStorage)


def test_storage_class_close_method_closes_db():
    """
    check that _get_storage_class method returns an instance of
    Storage class provided
    """
    telemetry_inst = Telemetry(**DEFAULT_TELEMETRY_PARAMS)
    storage_instance = telemetry_inst._get_storage_class(None)
    storage_instance.close_db()
    assert storage_instance.db_in_memory is None
    assert storage_instance.db_cursor is None


def test_mongo_telemetry():
    """
    Test mongo_telemetry method returns a Telemetry object with a mongo storage
    class.
    """
    telemetry = mongo_telemetry(telemetry_rules={}, **DEFAULT_TELEMETRY_PARAMS)
    assert isinstance(telemetry, Telemetry)
    assert isinstance(telemetry._storage_class, TelemetryMongoStorage)
