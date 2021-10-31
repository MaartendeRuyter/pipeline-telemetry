"""
This module provides test data for the telemetry tests
"""
from errors.base import ErrorCode

from pipeline_telemetry.settings.process_type import ProcessTypes
from pipeline_telemetry.settings.settings import \
    DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES, ProcessType


class InstructionTestClass():
    """Instruction class for test purposes."""
    # pylint: disable=too-few-public-methods
    instruction = 'test_instruction'
    fieldname = 'field_name'

    def __new__(cls):
        """ make this a singleton class """
        return cls


# default params for creating a test Telemetry object
DEFAULT_TELEMETRY_PARAMS = {
    'process_name': 'load_weather_data',
    'process_type': ProcessTypes.CREATE_DATA_FROM_URL
}

# custom process type for testing extending the default process types
CUSTOM_PROCESS_TYPE = {
    'custom_process_type': ['CUSTOM_SUB_TYPE']}

TEST_ERROR_CODE = ErrorCode(
    code="TEST_CODE_0001",
    description='test error'
)

TEST_TELEMETRY_RULES = {
    'RETRIEVE_RAW_DATA': {
        'has_key': {'field_name': 'items'}
    }
}

TEST_PROCESS_TYPE = ProcessType(
    process_type='test_process_type',
    subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES)
