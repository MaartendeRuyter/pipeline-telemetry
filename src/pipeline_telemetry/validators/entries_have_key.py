"""Module to define EntriesHaveKey class validator
"""
import jmespath
from errors import ErrorCode, ListErrors

from ..settings import exceptions
from ..validators.dict_validator import DictValidator


class EntriesHaveKey():
    """
    class to define HasFieldName instruction. Validator checks if all
    entries in a field contain a specific key.

    Validator can be invoked with command `entries_have_key`
    rule_content needs to contain:
        - field_name (str): field that holds the entries in a dict or a list
        - must_have_key (str): field that hold the key that is to be present
                               in all entries

    public method
        - validate
    """
    instruction = 'entries_have_key'
    fieldname = 'field_name'
    must_have_key = 'must_have_key'

    def __new__(cls):
        """ make this a singleton class """
        return cls

    @classmethod
    def validate(
            cls, dict_to_validate: dict, rule_content: dict) -> list[ErrorCode]:
        """
        Public method run the validation
        prior to validation the rule will be validated.

        Args:
            dict_to_validate (dict): Input dict that needs validation
            rule_content (dict): actual rule

        Returns:
            list[ErrorCode]: List with errors that were found. Empty list if no
                             errors were found

        Raise:
            FieldNameMandatory: when field name not defined in rule
            MustHaveKeyMandatory: when must have key is not defined in rule
        """
        cls._validate_rule(rule_content)
        return cls._validate(dict_to_validate, rule_content)

    @classmethod
    def _validate(
            cls, dict_to_validate: dict,
            rule_content: dict) -> list[ErrorCode]:
        """
        method to do the actual validation

        returns:
            - error in case
        """
        # if entries does not exist stop validation and return error
        if error := cls._validate_field_exists(dict_to_validate, rule_content):
            return error

        # if entries field is notlist or dict stop validation and return error
        if error := cls._validate_type_entries_field(
                dict_to_validate, rule_content):
            return error

        # return the errors per entry
        return cls._validate_entries_have_key(dict_to_validate, rule_content)

    @classmethod
    def _validate_entries_have_key(
            cls, dict_to_validate: dict,
            rule_content: dict) -> list[ErrorCode]:
        """
        method to check if the values in the entry have a specific key

        returns:
            - list{ErrorCode]: Empty list in case all entries have the key
        """
        errors = []
        fieldname = cls._get_field_name(rule_content)
        must_have_key = cls._get_must_have_key(rule_content)

        # prepare error messages
        entry_is_not_a_dict_error = cls._validation_error(
            ListErrors.ENTRY_IS_NOT_A_DICT, fieldname)
        missing_key_in_entry_error = cls._validation_error(
            ListErrors.KEY_NOT_FOUND_IN_ENTRY, fieldname + "_" + must_have_key)

        # for each entry do a has_key validation with the `must_have_key` field
        for entry in jmespath.search(fieldname, dict_to_validate):
            if not isinstance(entry, dict):
                errors.extend(entry_is_not_a_dict_error)
                continue

            if not jmespath.search(must_have_key, entry):
                errors.extend(missing_key_in_entry_error)

        return errors

    @classmethod
    def _validate_field_exists(
            cls, dict_to_validate: dict,
            rule_content: dict) -> list[ErrorCode]:
        """
        method to check if entries field exists in dict_to_validate

        returns:
            - list{ErrorCode]: Empty list in case the field does exist
        """
        fieldname = cls._get_field_name(rule_content)
        if not jmespath.search(fieldname, dict_to_validate):
            return cls._validation_error(
                ListErrors.ENTRIES_FIELD_NOT_FOUND, fieldname)

        return []

    @classmethod
    def _validate_type_entries_field(
            cls, dict_to_validate: dict,
            rule_content: dict) -> list[ErrorCode]:
        """
        method to check if entries field in dict_to_validate is a list

        returns:
            - list[ErrorCode]: Empty list in case the field holds a list
        """
        fieldname = cls._get_field_name(rule_content)
        entries = jmespath.search(fieldname, dict_to_validate)
        if not isinstance(entries, (list)):
            return cls._validation_error(
                ListErrors.ENTRIES_FIELD_OF_WRONG_TYPE, fieldname)

        return []

    @classmethod
    def _validate_rule(cls, rule_content: dict) -> None:
        """Method to raise exception when rule_content in invalid."""
        fieldname = cls._get_field_name(rule_content)
        if not isinstance(fieldname, str):
            raise exceptions.FieldNameMandatory(cls.instruction)

        must_have_key = cls._get_must_have_key(rule_content)
        if not isinstance(must_have_key, str):
            raise exceptions.MustHaveKeyMandatory(cls.instruction)

    @classmethod
    def _get_must_have_key(cls, rule_content: dict) -> str:
        """
        retrieves the must_have_key from the rule content
        """
        return rule_content.get(cls.must_have_key, None)

    @classmethod
    def _get_field_name(cls, rule_content: dict) -> str:
        """
        retrieves the field name in scope from the rule content
        """
        return rule_content.get(cls.fieldname, None)

    @staticmethod
    def _validation_error(
            error_code: ErrorCode, fieldname: str) -> list[ErrorCode]:
        """ returns error code object in list with fieldname as error data """
        key_specific_error = error_code.code + '@KEY_<' + fieldname + '>'
        return [ErrorCode(
            code=key_specific_error, description=error_code.description)]


DictValidator.register_instruction(EntriesHaveKey)
