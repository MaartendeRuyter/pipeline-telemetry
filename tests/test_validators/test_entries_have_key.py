"""
module to test entries_have_key instruction class
"""

from pipeline_telemetry.validators.entries_have_key import (
    EntriesHaveKey,
    EntriesHaveKeyRuleData,
)

# pylint: disable=protected-access


def test_has_key_class_exists():
    """check that HasKey class exists"""
    assert EntriesHaveKey


def test_has_key_class_is_singelton():
    """check that HasKey is a singleton class"""
    instance_one = EntriesHaveKey()
    instance_two = EntriesHaveKey()
    assert instance_one is instance_two


def test_get_field_name_method():
    """
    check that _get_field_name method returns value of
    field_name that is in scope of validation
    """
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "test", "must_have_key": "test"}
    )
    assert EntriesHaveKey._get_field_name(rule_content) == "test"


def test_get_must_have_key_method():
    """
    check that _get_must_have_key method returns value of
    must_have_key that is in scope of validation
    """
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "fieldname", "must_have_key": "test"}
    )
    assert EntriesHaveKey._get_must_have_key(rule_content) == "test"


def test_validate_field_exists():
    """
    test that _validate_field_exists method returns empty list when
    entries field exists
    """
    dict_to_validate = {"items": [{"key": 1}, {"key": 2}]}
    rule_data = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key"}
    )

    assert EntriesHaveKey._validate_field_exists(dict_to_validate, rule_data) == []


def test_validate_field_exists_returns_error():
    """
    test that _validate_field_exists method returns empty list when
    entries field exists
    """
    dict_to_validate = {"not_items": [{"key": 1}, {"key": 2}]}
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key"}
    )
    errors = EntriesHaveKey._validate_field_exists(dict_to_validate, rule_content)

    assert len(errors) == 1
    assert "Entries field does not exist" in errors[0].description


def test_validate_entries_have_key():
    """
    test that _validate_entries_have_key method returns empty list when all
    entries have the right key
    """
    dict_to_validate = {"items": [{"key": 1}, {"key": 2}]}
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key"}
    )

    assert (
        EntriesHaveKey._validate_entries_have_key(dict_to_validate, rule_content) == []
    )


def test_validate_entries_have_nested_key():
    """
    test that _validate_entries_have_key method returns empty list when all
    entries have the right key
    """
    dict_to_validate = {"items": [{"key": {"nested_key": 2}}]}
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key.nested_key"}
    )

    assert (
        EntriesHaveKey._validate_entries_have_key(dict_to_validate, rule_content) == []
    )


def test_validate_entries_have_key_with_missing_key():
    """
    test that _validate_entries_have_key method returns list with has_key
    error when a key is missing
    """
    dict_to_validate = {"items": [{"not_key": 1}, {"key": 2}]}
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key"}
    )

    errors = EntriesHaveKey._validate_entries_have_key(dict_to_validate, rule_content)

    assert len(errors) == 1
    assert "Key missing in entry" in errors[0].description


def test_validate_entries_have_key_with_non_dict_items():
    """
    test that _validate_entries_have_key method returns list with
    entry_is_not_a_dict error when entry is not a dicy
    """
    dict_to_validate = {"items": ["not_a_dict", {"key": 2}]}
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key"}
    )

    errors = EntriesHaveKey._validate_entries_have_key(dict_to_validate, rule_content)

    assert len(errors) == 1
    assert "Entry that needs to have a key is not a dict" in errors[0].description


def test_validate_entries_have_keys_with_missing_key():
    """
    test that _validate_entries_have_key method returns list with has_key
    errors when a all keys are missing
    """
    dict_to_validate = {"items": [{"not_key": 1}, {"also_not_key": 2}]}
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key"}
    )

    errors = EntriesHaveKey._validate_entries_have_key(dict_to_validate, rule_content)

    assert len(errors) == 2


def test_validate_calls_validate_field_exists(mocker):
    """
    test that _validate method calls the _validate_field_exists method
    """
    dict_to_validate = {"not_items": [{"not_key": 1}, {"also_not_key": 2}]}
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key"}
    )

    _validate_field_exists_spy = mocker.spy(EntriesHaveKey, "_validate_field_exists")

    EntriesHaveKey._validate(dict_to_validate, rule_content)

    assert _validate_field_exists_spy.called


def test_validate_calls_validate_type_entries_field(mocker):
    """
    test that _validate method calls the _validate_type_entries_field method
    """
    dict_to_validate = {"items": "not a list or a dict"}
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key"}
    )

    _validate_type_entries_field_spy = mocker.spy(
        EntriesHaveKey, "_validate_type_entries_field"
    )

    EntriesHaveKey._validate(dict_to_validate, rule_content)

    assert _validate_type_entries_field_spy.called


def test_validate_calls_validate_entries_have_key(mocker):
    """
    test that _validate method calls the _validate_type_entries_field method
    """
    dict_to_validate = {"items": [{"a": 1}]}
    rule_content = EntriesHaveKeyRuleData(
        **{"field_name": "items", "must_have_key": "key"}
    )

    _validate_entries_have_key_spy = mocker.spy(
        EntriesHaveKey, "_validate_type_entries_field"
    )

    EntriesHaveKey._validate(dict_to_validate, rule_content)

    assert _validate_entries_have_key_spy.called


def test_validate_calls_validate(mocker):
    """
    test that public validate method calls the _validate method
    """
    dict_to_validate = {"items": [{"a": 1}]}
    rule_content = {"field_name": "items", "must_have_key": "key"}

    _validate_spy = mocker.spy(EntriesHaveKey, "_validate")
    EntriesHaveKey.validate(dict_to_validate, rule_content)

    assert _validate_spy.called
