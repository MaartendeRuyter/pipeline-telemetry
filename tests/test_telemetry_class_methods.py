"""
module to test the class methods fro Telemetry class of telemetry module

"""

import pytest

from pipeline_telemetry.main import Telemetry
from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.settings.data_class import ProcessType


def test_telemetry_class_method_add_process_type():
    """
    check that Telemetry class method add_process_type adds a process type
    """
    process_type = ProcessType(
        process_type="custom_process_type", subtypes=["custom_sub_process_type"]
    )
    Telemetry.add_process_type("TEST_TYPE", process_type)
    assert Telemetry("test", "test", "test", process_type)


def test_sub_process_types_also_added():
    """
    check that Telemetry class method add_process_type adds a process type
    including all sub_processes.
    """
    process_type = ProcessType(
        process_type="custom_process_type", subtypes=["custom_sub_process_type"]
    )
    Telemetry.add_process_type("TEST_TYPE", process_type)
    telemetry = Telemetry("category", "sub_category", "name", process_type)
    assert telemetry._process_type.sub_processes == ["custom_sub_process_type"]


def test_add_process_type_raises_exception():
    """
    test class method add_process_type raises an excpetion when an object
    other the a ProcessType is offered
    """
    with pytest.raises(exceptions.ProcessTypeMustBeOfClassProcessType):
        Telemetry.add_process_type("TYPE_NAME", "not a ProcessType")
