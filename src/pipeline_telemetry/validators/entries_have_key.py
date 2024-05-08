"""Module to define EntriesHaveKey class validator"""

from dataclasses import dataclass

import jmespath
from errors import ErrorCode, ListErrors

from .abstract_validator_instruction import (
    AbstractValidatorInstruction,
    BaseValidatorInstructionRuleData,
)


@dataclass(frozen=True)
class EntriesHaveKeyRuleData(BaseValidatorInstructionRuleData):
    must_have_key: str


class EntriesHaveKey(AbstractValidatorInstruction):
    """
    class to define EntriesHaveKey instruction. Validator checks if all
    entries in a list are of type dict and contain a specific key/field.

    Validator can be invoked with command `entries_have_key`
    rule_data needs to contain:
        - field_name (str): field that holds list of entries to be
                            validated
        - must_have_key (str): field that hold the key that is to be present
                               in all entries

    public method
        - validate
    """

    RULE_DATA_CLASS = EntriesHaveKeyRuleData
    INSTRUCTION = "entries_have_key"
    must_have_key = "must_have_key"

    @classmethod
    def _validate(
        cls, dict_to_validate: dict, rule_data: BaseValidatorInstructionRuleData
    ) -> list[ErrorCode]:
        """
        method to do the actual validation

        returns:
            - list of errorcodes
        """
        # if entries does not exist stop validation
        if error := cls._validate_field_exists(dict_to_validate, rule_data):
            return error

        # if entries field is not a list stop validation
        if error := cls._validate_type_entries_field(dict_to_validate, rule_data):
            return error

        # return the errors per entry
        return cls._validate_entries_have_key(dict_to_validate, rule_data)

    @classmethod
    def _validate_entries_have_key(
        cls, dict_to_validate: dict, rule_data: BaseValidatorInstructionRuleData
    ) -> list[ErrorCode]:
        """
        method to check if the values in the entry have a specific key

        returns:
            - list{ErrorCode]: Empty list in case all entries have the key
        """
        errors = []
        fieldname = cls._get_field_name(rule_data)
        must_have_key = cls._get_must_have_key(rule_data)

        # prepare error messages
        entry_is_not_a_dict_error = cls._validation_error(
            ListErrors.ENTRY_IS_NOT_A_DICT, fieldname
        )
        missing_key_in_entry_error = cls._validation_error(
            ListErrors.KEY_NOT_FOUND_IN_ENTRY, fieldname + "__" + must_have_key
        )

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
        cls, dict_to_validate: dict, rule_data: BaseValidatorInstructionRuleData
    ) -> list[ErrorCode]:
        """
        method to check if entries field exists in dict_to_validate

        returns:
            - list{ErrorCode]: Empty list in case the field does exist
        """
        fieldname = cls._get_field_name(rule_data)

        if not jmespath.search(fieldname, dict_to_validate):
            return cls._validation_error(ListErrors.ENTRIES_FIELD_NOT_FOUND, fieldname)

        return []

    @classmethod
    def _validate_type_entries_field(
        cls, dict_to_validate: dict, rule_data: BaseValidatorInstructionRuleData
    ) -> list[ErrorCode]:
        """
        method to check if entries field in dict_to_validate is a list

        returns:
            - list[ErrorCode]: Empty list in case the field holds a list
        """
        fieldname = cls._get_field_name(rule_data)
        entries = jmespath.search(fieldname, dict_to_validate)
        if not isinstance(entries, (list)):
            return cls._validation_error(
                ListErrors.ENTRIES_FIELD_OF_WRONG_TYPE, fieldname
            )

        return []

    @classmethod
    def _get_must_have_key(cls, rule_data: BaseValidatorInstructionRuleData) -> str:
        """
        retrieves the must_have_key from the rule content
        """
        return getattr(rule_data, cls.must_have_key)

    @staticmethod
    def _validation_error(error_code: ErrorCode, fieldname: str) -> list[ErrorCode]:
        """returns error code object in list with fieldname as error data"""
        key_specific_error = error_code.code + "@KEY_<" + fieldname + ">"
        return [ErrorCode(code=key_specific_error, description=error_code.description)]
