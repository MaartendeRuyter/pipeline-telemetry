"""Module to run integration test for telemetry module
"""
from test_data import DEFAULT_TELEMETRY_PARAMS
from test_integration_data import BASIC_RETRIEVE_DATA_TEST, \
    ITEMS_FIELD_HAS_DICT_TEST, MISSING_KEY_RETRIEVE_DATA_TEST, \
    MUST_HAVE_KEY_IN_ITEMS_TEST, NO_ITEMS_HAVE_MUST_HAVE_KEY_TEST, \
    validate_result_from_telemetry

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


def test_must_have_key_in_items_integration_test():
    """
    Test telemetry returns correct telemetry object when key is missing in one
    of the items.
    """
    telemetry_rules = MUST_HAVE_KEY_IN_ITEMS_TEST.validation_rules
    telemetry_params = DEFAULT_TELEMETRY_PARAMS | \
        {'telemetry_rules': telemetry_rules}
    telemetry = Telemetry(**telemetry_params)
    telemetry.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry.add('RETRIEVE_RAW_DATA',
                  MUST_HAVE_KEY_IN_ITEMS_TEST.data, None)
    telemetry.save_and_close()
    assert validate_result_from_telemetry(
        telemetry, MUST_HAVE_KEY_IN_ITEMS_TEST)


def test_no_items_have_must_have_key_in_items_integration_test():
    """
    Test telemetry returns correct telemetry object when no item has the
    correct key.
    """
    telemetry_rules = NO_ITEMS_HAVE_MUST_HAVE_KEY_TEST.validation_rules
    telemetry_params = DEFAULT_TELEMETRY_PARAMS | \
        {'telemetry_rules': telemetry_rules}
    telemetry = Telemetry(**telemetry_params)
    telemetry.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry.add('RETRIEVE_RAW_DATA',
                  NO_ITEMS_HAVE_MUST_HAVE_KEY_TEST.data, None)
    telemetry.save_and_close()
    assert validate_result_from_telemetry(
        telemetry, NO_ITEMS_HAVE_MUST_HAVE_KEY_TEST)


def test_items_has_dict_field_test():
    """
    Test telemetry returns correct telemetry object when items field contains
    a dict field.
    """
    telemetry_rules = ITEMS_FIELD_HAS_DICT_TEST.validation_rules
    telemetry_params = DEFAULT_TELEMETRY_PARAMS | \
        {'telemetry_rules': telemetry_rules}
    telemetry = Telemetry(**telemetry_params)
    telemetry.increase_sub_process_base_count('RETRIEVE_RAW_DATA')
    telemetry.add('RETRIEVE_RAW_DATA',
                  ITEMS_FIELD_HAS_DICT_TEST.data, None)
    telemetry.save_and_close()
    print(telemetry.telemetry)
    assert validate_result_from_telemetry(
        telemetry, ITEMS_FIELD_HAS_DICT_TEST)
