"""
This module provides test data for the telemetry tests
"""
from errors.base import ErrorCode


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
    'process_type': 'create_data_from_url'
}

# custom process type for testing extending the default process types
CUSTOM_PROCESS_TYPE = {
    'custom_process_type': ['CUSTOM_SUB_TYPE']}

TEST_ERROR_CODE = ErrorCode(
    code="TEST_CODE_0001",
    description='test error'
)
