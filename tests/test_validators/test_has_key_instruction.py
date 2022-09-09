"""
module to test has_key instruction class
"""
from test_data import TEST_ERROR_CODE

from pipeline_telemetry.settings.telemetry_errors import ErrorCode
from pipeline_telemetry.validators.abstract_validator_instruction import \
    BaseValidatorInstructionRuleData
from pipeline_telemetry.validators.has_key import HasKey

# pylint: disable=protected-access


def test_has_key_class_exists():
    """ check that HasKey class exists """
    assert HasKey


def test_has_key_class_is_singelton():
    """ check that HasKey is a singleton class """
    instance_one = HasKey()
    instance_two = HasKey()
    assert instance_one is instance_two


def test_get_field_name_method():
    """
    check that _get_field_name method returns value of
    field_name that is in scope of validation
    """
    rule_data = BaseValidatorInstructionRuleData(**{'field_name': 'test'})
    assert HasKey._get_field_name(rule_data) == 'test'


def test_validation_error_method():
    """
    Check that _validation_error method returns a list with
    ErrorCode instance.
    """
    validation_error_list = HasKey._validation_error(
        TEST_ERROR_CODE, 'test_error_data')
    validation_error = validation_error_list[0]
    assert isinstance(validation_error_list, list)
    assert isinstance(validation_error, ErrorCode)


def test_validate_valid_dict():
    """Test that a dict with right key returns empty error list
    """
    valid_dict = {'correct_key': 'value'}
    rule_dict = {'field_name': 'correct_key'}
    validation_result = HasKey.validate(
        dict_to_validate=valid_dict, rule_dict=rule_dict
    )
    assert validation_result == []


def test_validate_valid_dict_with_nested_key():
    """
    Test that a dict with right key returns empty error list when the nested
    key in input dict is found
    """
    valid_dict = {'correct_key': {'nested_key': 'value'}}
    rule_dict = {'field_name': 'correct_key.nested_key'}
    validation_result = HasKey.validate(
        dict_to_validate=valid_dict, rule_dict=rule_dict
    )
    assert validation_result == []


def test_validate_invalid_dict():
    """
    Test that a dict without right key returns a list with error_code
    KEY_NOT_FOUND_001 and the field_name in the error_data

    """
    invalid_dict = {'incorrect_key': 'value'}
    rule_dict = {'field_name': 'correct_key'}
    validation_result = HasKey.validate(
        dict_to_validate=invalid_dict, rule_dict=rule_dict
    )
    assert len(validation_result) == 1
    assert validation_result[0].code == 'HAS_KEY_ERR_0001@KEY_<correct_key>'


def test_validate_invalid_nested_dict():
    """
    Test that a nested dict without right nested key returns a list with
    error_code KEY_NOT_FOUND_001 and the nested field_name in the error_data.
    """
    invalid_dict = {'incorrect_key': {'nested_key': 'value'}}
    rule_dict = {'field_name': 'correct_key.nested_key'}
    validation_result = HasKey.validate(
        dict_to_validate=invalid_dict, rule_dict=rule_dict
    )
    assert len(validation_result) == 1
    assert validation_result[0].code == \
        'HAS_KEY_ERR_0001@KEY_<correct_key.nested_key>'
