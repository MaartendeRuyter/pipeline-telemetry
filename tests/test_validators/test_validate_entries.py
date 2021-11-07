"""
module to test has_key instruction class
"""
# pylint: disable=protected-access
import pytest
from test_data import TEST_ERROR_CODE

from pipeline_telemetry.settings.exceptions import \
    ExpectedCountMustBePositiveInt, FieldNameMandatory
from pipeline_telemetry.settings.telemetry_errors import ErrorCode
from pipeline_telemetry.validators.validate_entries import ValidateEntries


def test_validate_entries_class_exists():
    """ check that ValidateEntries class exists """
    assert ValidateEntries


def test_validate_entries_class_is_singleton_clss():
    """Check that ValidateEntries class is a singleton class."""
    assert ValidateEntries() is ValidateEntries()


def test_validate_rule_method_raises_exception():
    """
    check that _validate_rule method raises exception when field name
    not provided in rule
    """
    rule_content = {'not_field_name': 'test', 'expected_count': 1}
    with pytest.raises(FieldNameMandatory) as exception:
        ValidateEntries._validate_rule(rule_content)

    assert 'For `validate_entries` instruction' in str(exception)


def test_validate_rule_method_without_expected_count_raises_exception():
    """
    check that _validate_rule method raises exception when expected_count
    not provided in rule
    """
    rule_content = {'field_name': 'test'}
    with pytest.raises(ExpectedCountMustBePositiveInt) as exception:
        ValidateEntries._validate_rule(rule_content)

    assert 'Ruleset does not contain `expected_count`' in str(exception)


def test_validate_rule_method_with_neg_expected_count_raises_exception():
    """
    check that _validate_rule method raises exception when expected_count
    is a negative integer
    """
    rule_content = {'field_name': 'test', 'expected_count': -1}
    with pytest.raises(ExpectedCountMustBePositiveInt):
        ValidateEntries._validate_rule(rule_content)


def test_validate_rule_method_returns_none():
    """
    check that _validate_rule method returns none when field name and
    expected_count are provided in the rule
    """
    rule_content = {'field_name': 'test', 'expected_count': 1}
    assert ValidateEntries._validate_rule(rule_content) is None


def test_get_field_name_method():
    """
    check that _get_field_name method returns value of
    field_name that is in scope of validation
    """
    rule_content = {'field_name': 'test', 'expected_count': 1}
    assert ValidateEntries._get_field_name(rule_content) == 'test'


def test_get_expected_count():
    """
    check that _get_expected_count method returns value of
    expected_count
    """
    rule_content = {'field_name': 'test', 'expected_count': 1}
    assert ValidateEntries._get_expected_count(rule_content) == 1


def test_validation_error_method():
    """
    check that _validation_error method returns instance
    of ErrorCode with fieldname in error_data
    """
    validation_error_list = ValidateEntries._validation_error(
        TEST_ERROR_CODE, 'test_error_data')
    validation_error = validation_error_list[0]
    assert isinstance(validation_error_list, list)
    assert isinstance(validation_error, ErrorCode)
    assert validation_error.error_data == 'test_error_data'


def test_validate_valid_dict():
    """
    Test that a dict with a field with a list with the expected count (length)
    returns empty error list
    """
    valid_dict = {'correct_key': [1, 2, 3, 4]}
    rule_content = {'field_name': 'correct_key', 'expected_count': 4}
    validation_result = ValidateEntries.validate(
        dict_to_validate=valid_dict, rule_content=rule_content
    )
    assert validation_result == []


def test_validate_valid_dict_with_nested_key():
    """
    Test that a dict of the right length in nested key returns an empty error
    lits
    """
    valid_dict = {'key': {'nested_key': {'a': 1, 'b': 2}}}
    rule_content = {'field_name': 'key.nested_key', 'expected_count': 2}
    validation_result = ValidateEntries.validate(
        dict_to_validate=valid_dict, rule_content=rule_content
    )
    assert validation_result == []


def test_validate_invalid_dict():
    """
    Test that a dict without right key returns a list with error_code
    VALIDATE_ENTRIES_ERR_001 and the field_name in the error_data

    """
    invalid_dict = {'incorrect_key': 'value'}
    rule_content = {'field_name': 'correct_key', 'expected_count': 2}
    validation_result = ValidateEntries.validate(
        dict_to_validate=invalid_dict, rule_content=rule_content
    )
    assert len(validation_result) == 1
    assert validation_result[0].code == 'VALIDATE_ENTRIES_ERR_001'
    assert validation_result[0].error_data == 'correct_key'


def test_validate_dict_with_wrong_type_in_field():
    """
    Test that a dict without right key returns a list with error_code
    VALIDATE_ENTRIES_ERR_002 and the field_name in the error_data

    """
    invalid_dict = {'correct_key': 'value'}
    rule_content = {'field_name': 'correct_key', 'expected_count': 2}
    validation_result = ValidateEntries.validate(
        dict_to_validate=invalid_dict, rule_content=rule_content
    )
    assert len(validation_result) == 1
    assert validation_result[0].code == 'VALIDATE_ENTRIES_ERR_002'
    assert validation_result[0].error_data == 'correct_key'


def test_validate_dict_with_wrong_number_of_entries():
    """
    Test that a dict without right key returns a list with error_code
    VALIDATE_ENTRIES_ERR_003 and the field_name in the error_data

    """
    invalid_dict = {'correct_key': [1, 2, 3]}
    rule_content = {'field_name': 'correct_key', 'expected_count': 2}
    validation_result = ValidateEntries.validate(
        dict_to_validate=invalid_dict, rule_content=rule_content
    )
    assert len(validation_result) == 1
    assert validation_result[0].code == 'VALIDATE_ENTRIES_ERR_003'
    assert validation_result[0].error_data == 'correct_key'
