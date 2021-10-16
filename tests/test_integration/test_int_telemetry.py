"""Module to run integration test for telemetry module
"""
from test_data import DEFAULT_TELEMETRY_PARAMS
from test_integration_data import BASIC_RETRIEVE_DATA_TEST, \
    MISSING_KEY_RETRIEVE_DATA_TEST, validate_result_from_telemetry

from pipeline_telemetry.main import Telemetry


def test_basic_test_data():
    """Test data basic data test returns correct telemetry."""
    telemetry_rules = BASIC_RETRIEVE_DATA_TEST.validation_rules
    telemetry_params = DEFAULT_TELEMETRY_PARAMS | \
        {'telemetry_rules': telemetry_rules}
    telemetry = Telemetry(**telemetry_params)
    telemetry.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry.add('RETRIEVE_RAW_DATA', BASIC_RETRIEVE_DATA_TEST.data, None)
    telemetry.save_and_close()
    assert validate_result_from_telemetry(telemetry, BASIC_RETRIEVE_DATA_TEST)


def test_missing_key_integration_test():
    """Test telemetry returns correct telemetry object when key is missing."""
    telemetry_rules = MISSING_KEY_RETRIEVE_DATA_TEST.validation_rules
    telemetry_params = DEFAULT_TELEMETRY_PARAMS | \
        {'telemetry_rules': telemetry_rules}
    telemetry = Telemetry(**telemetry_params)
    telemetry.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry.add('RETRIEVE_RAW_DATA',
                  MISSING_KEY_RETRIEVE_DATA_TEST.data, None)
    telemetry.save_and_close()
    assert validate_result_from_telemetry(
        telemetry, MISSING_KEY_RETRIEVE_DATA_TEST)
