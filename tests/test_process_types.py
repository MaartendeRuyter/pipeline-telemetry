"""Module to test processtype logic.
"""
from pipeline_telemetry.settings.process_type import ProcessTypes
from pipeline_telemetry.settings.settings import \
    DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES


def test_process_type_class_exists():
    """Test that process types class exists."""
    assert ProcessTypes


def test_process_type_class_can_call_a_process_type():
    """Test that a process type can be called upon the class exists."""
    assert ProcessTypes.CREATE_DATA_FROM_URL


def test_calling_process_key_property_on_a_process_type_returns_a_str():
    """
    Test that calling process_key property on a process type returns the
    process_type name.
    """
    assert ProcessTypes.CREATE_DATA_FROM_URL.process_key == \
        'create_data_from_url'


def test_calling_sub_processes_property_on_a_process_type_returns_a_list():
    """
    Test that calling sub_processes property on a process type returns the
    list of sub_processes.
    """
    assert ProcessTypes.CREATE_DATA_FROM_URL.sub_processes == \
        DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES
