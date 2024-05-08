"""
This module provides test data for the telemetry tests
"""

from errors import ErrorCode, ListErrors, ReturnValueWithStatus

from pipeline_telemetry import ProcessType, ProcessTypes, TelemetryCounter
from pipeline_telemetry.settings.settings import DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES
from pipeline_telemetry.validators.abstract_validator_instruction import (
    AbstractValidatorInstruction,
)


class InstructionTestClass(AbstractValidatorInstruction):
    """Instruction class for test purposes."""

    INSTRUCTION = "test_instruction"


# default params for creating a test Telemetry object
DEFAULT_TELEMETRY_PARAMS = {
    "category": "WEATHER",
    "sub_category": "DAILY_PREDICTIONS",
    "source_name": "load_weather_data",
    "process_type": ProcessTypes.CREATE_DATA_FROM_URL,
}

DEFAULT_TELEMETRY_MODEL_PARAMS = {
    "telemetry_type": "SINGLE TELEMETRY",
    "category": "WEATHER",
    "sub_category": "DAILY_PREDICTIONS",
    "source_name": "load_weather_data",
    "process_type": ProcessTypes.CREATE_DATA_FROM_URL.name,
}

# custom process type for testing extending the default process types
CUSTOM_PROCESS_TYPE = {"custom_process_type": ["CUSTOM_SUB_TYPE"]}

TEST_ERROR_CODE = ErrorCode(code="TEST_CODE_0001", description="test error")
TEST_ERROR_CODE_2 = ErrorCode(code="TEST_CODE_0002", description="test error")

TEST_TELEMETRY_RULES = {"RETRIEVE_RAW_DATA": {"has_key": {"field_name": "items"}}}

TEST_PROCESS_TYPE = ProcessType(
    process_type="test_process_type", subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES
)


TEST_PROCESS_TYPE_2 = ProcessType(
    process_type="test_process_type", subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES
)

TEST_PROCESS_TYPE_3 = ProcessType(
    process_type="test_process_type_3", subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES
)

TEST_TELEMETRY_COUNTER = TelemetryCounter(
    process_type=TEST_PROCESS_TYPE,
    sub_process="RETRIEVE_RAW_DATA",
    counter_name="test_counter",
)

TEST_TELEMETRY_COUNTER_2 = TelemetryCounter(
    process_type=TEST_PROCESS_TYPE,
    sub_process="RETRIEVE_RAW_DATA",
    counter_name="test_counter_2",
)

TEST_TELEMETRY_COUNTER_3 = TelemetryCounter(
    process_type=TEST_PROCESS_TYPE,
    sub_process="DATA_CONVERSION",
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

TEST_ERROR_TELEMETRY_COUNTER_2 = TelemetryCounter(
    process_type=TEST_PROCESS_TYPE,
    sub_process="RETRIEVE_RAW_DATA",
    increment=1,
    error=ListErrors.FIELD_NOT_FOUND,
)


TEST_ERROR_TC_PROCESS_TYPE_2 = TelemetryCounter(
    process_type=TEST_PROCESS_TYPE,
    sub_process="RETRIEVE_RAW_DATA",
    increment=1,
    error=ListErrors.KEY_NOT_FOUND,
)

TEST_TC_MULT_PROCESS_TYPES = TelemetryCounter(
    process_types=[TEST_PROCESS_TYPE, TEST_PROCESS_TYPE_2],
    sub_process="RETRIEVE_RAW_DATA",
    counter_name="test_counter",
)

TEST_TC_MULT_PROCESS_TYPES_2 = TelemetryCounter(
    process_types=[TEST_PROCESS_TYPE],
    sub_process="RETRIEVE_RAW_DATA",
    counter_name="test_counter",
)


TEST_RESULT = [1, TEST_TELEMETRY_COUNTER, 2, TEST_ERROR_TELEMETRY_COUNTER]

TEST_RETURN_VALUE = ReturnValueWithStatus(result=TEST_RESULT)
