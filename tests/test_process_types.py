"""Module to test processtype logic.
"""
import pytest
from test_data import TEST_PROCESS_TYPE

from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings.process_type import ProcessTypes
from pipeline_telemetry.settings.settings import \
    DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES


def test_process_type_class_exists():
    """Test that process types class exists."""
    assert ProcessTypes


def test_process_type_class_is_a_singleton_class():
    """Test that process types class exists."""
    assert ProcessTypes() is ProcessTypes()


def test_process_type_class_can_call_a_process_type():
    """Test that a process type can be called upon the class exists."""
    assert ProcessTypes.CREATE_DATA_FROM_URL


def test_calling_name_property_on_a_process_type_returns_a_str():
    """
    Test that calling name property on a process type returns the
    process_type name.
    """
    assert ProcessTypes.CREATE_DATA_FROM_URL.name == \
        'create_data_from_url'


def test_calling_sub_processes_property_on_a_process_type_returns_a_list():
    """
    Test that calling sub_processes property on a process type returns the
    list of sub_processes.
    """
    assert ProcessTypes.CREATE_DATA_FROM_URL.sub_processes == \
        DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES


def test_registering_process_type_success():
    """
    Test that a processtype can be registered
    """
    assert not ProcessTypes.is_registered(TEST_PROCESS_TYPE)
    ProcessTypes.register_process_type('TEST_PROCESS_TYPE', TEST_PROCESS_TYPE)
    assert ProcessTypes.is_registered(TEST_PROCESS_TYPE)


def test_registering_process_type_raises_exception():
    """
    Test that registering a processtype with a processtype of wrong class
    raises an exception.
    """
    with pytest.raises(exceptions.ProcessTypeMustBeOfClassProcessType):
        ProcessTypes.register_process_type('TEST_PROCESS_TYPE', 'process_type')


def test_registering_process_types_with_class_instance_raises_exception():
    """
    Test that registering a process types enumerator with a class instance    raises an exception.
    """
    with pytest.raises(exceptions.ProcessTypesMustBeOfClassBaseEnumertor):
        ProcessTypes.register_process_types('process_type')


def test_registering_process_types_with_wrong_class_raises_exception():
    """
    Test that registering a process types enumerator with a wrong class
    raises an exception.
    """
    with pytest.raises(exceptions.ProcessTypesMustBeOfClassBaseEnumertor):
        ProcessTypes.register_process_types(str)
