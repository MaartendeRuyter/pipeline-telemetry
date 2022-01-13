"""
This module provides test data for the telemetry tests
"""
from errors import ErrorCode, ListErrors

from pipeline_telemetry.settings.data_class import ProcessType, \
    TelemetryCounter
from pipeline_telemetry.settings.process_type import ProcessTypes
from pipeline_telemetry.settings.settings import \
    DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES


class InstructionTestClass:
    """Instruction class for test purposes."""

    # pylint: disable=too-few-public-methods
    instruction = "test_instruction"
    fieldname = "field_name"

    def __new__(cls):
        """make this a singleton class"""
        return cls


# default params for creating a test Telemetry object
DEFAULT_TELEMETRY_PARAMS = {
    "category": "WEATHER",
    "sub_category": "DAILY_PREDICTIONS",
    "source_name": "load_weather_data",
    "process_type": ProcessTypes.CREATE_DATA_FROM_URL,
}

# custom process type for testing extending the default process types
CUSTOM_PROCESS_TYPE = {"custom_process_type": ["CUSTOM_SUB_TYPE"]}

TEST_ERROR_CODE = ErrorCode(code="TEST_CODE_0001", description="test error")

TEST_TELEMETRY_RULES = {"RETRIEVE_RAW_DATA": {"has_key": {"field_name": "items"}}}

TEST_PROCESS_TYPE = ProcessType(
    process_type="test_process_type", subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES
)

TEST_TELEMETRY_COUNTER = TelemetryCounter(
    process_type=TEST_PROCESS_TYPE,
    sub_process="RETRIEVE_RAW_DATA",
    counter_name="test_counter",
)

TEST_TELEMETRY_COUNTER_INC_2 = TelemetryCounter(
    process_type=TEST_PROCESS_TYPE,
    sub_process="RETRIEVE_RAW_DATA",
    counter_name="test_counter",
    increment=2,
)

TEST_INV_TELEMETRY_COUNTER = TelemetryCounter(
    process_type=TEST_PROCESS_TYPE,
    sub_process="invalid_sub_process",
    counter_name="test_counter",
    increment=2,
)

TEST_ERROR_TELEMETRY_COUNTER = TelemetryCounter(
    process_type=TEST_PROCESS_TYPE,
    sub_process="RETRIEVE_RAW_DATA",
    increment=1,
    error=ListErrors.KEY_NOT_FOUND,
)
