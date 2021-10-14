"""
module to test the class methods fro Telemetry class of telemetry module

"""
import pytest

from pipeline_telemetry.main import BASE_COUNT_KEY, Telemetry
from pipeline_telemetry.settings import exceptions


def test_telemetry_class_method_add_process_type():
    """
    check that Telemetry class method add_process_type adds a process type
    """
    process_type = 'custom_process_type'
    sub_process = 'custom_sub_process_type'
    Telemetry.add_process_type({process_type: [sub_process]})
    assert Telemetry('test', process_type)


def test_sub_process_types_also_added():
    """
    check that Telemetry class method add_process_type adds a process type
    including all sub_processes.
    """
    process_type = 'custom_process_type'
    sub_process = 'custom_sub_process_type'
    Telemetry.add_process_type({process_type: [sub_process]})
    telemetry = Telemetry('test', process_type)
    telemetry.increase_sub_process_base_count(sub_process=sub_process)
    assert telemetry.telemetry[sub_process][BASE_COUNT_KEY] == 1


def test_add_process_type_raises_exception():
    """
    test tha class method add_process_type raises an excpetion when an object
    other the a dict is offered
    """
    with pytest.raises(exceptions.ProcessTypeMustBeDict):
        Telemetry.add_process_type('not a dict')
