"""Module to define validate entries validator class
"""
import jmespath
from errors import ErrorCode, ListErrors, add_error_data

from ..settings import exceptions
from ..validators.dict_validator import DictValidator


class ValidateEntries():
    """
    class to define validate entries instruction.
    This instruction counts the entries in a list or a dict and reports an
    error when the number of items in the list or dict is different from the
    expected nr of items
    """
    instruction = 'validate_entries'
    fieldname_field = 'field_name'
    expected_count_field = 'expected_count'

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
            list[ErrorCode]: List with errors that were found

        Raise:
            FieldNameMandatory: when field name not defined in rule
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
        fieldname = cls._get_field_name(rule_content)

        field_to_validate = jmespath.search(fieldname, dict_to_validate)

        if not field_to_validate:
            return cls._validation_error(
                ListErrors.FIELD_NOT_FOUND, fieldname)

        if not isinstance(field_to_validate, (list, dict)):
            return cls._validation_error(
                ListErrors.WRONG_TYPE_IN_FIELD, fieldname)

        if len(field_to_validate) != cls._get_expected_count(rule_content):
            return cls._validation_error(
                ListErrors.UNEXPECTED_NR_OF_ITEMS, fieldname)

        return []

    @classmethod
    def _validate_rule(cls, rule_content):
        fieldname = cls._get_field_name(rule_content)
        if not isinstance(fieldname, str):
            raise exceptions.FieldNameMandatory(cls.instruction)
        expected_count = cls._get_expected_count(rule_content)
        if not isinstance(expected_count, int) or expected_count < 0:
            raise exceptions.ExpectedCountMustBePositiveInt()

    @classmethod
    def _get_field_name(cls, rule_content):
        """
        retrieves the field name in scope from the rule content
        """
        return rule_content.get(cls.fieldname_field, None)

    @classmethod
    def _get_expected_count(cls, rule_content):
        """
        retrieves the expected_count in scope of the rule content
        """
        return rule_content.get(cls.expected_count_field, None)

    @staticmethod
    def _validation_error(
            error_code: ErrorCode, fieldname: str) -> list[ErrorCode]:
        """ returns error code object in list with fieldname as error data """
        return [add_error_data(error=error_code, error_data=fieldname)]


DictValidator.register_instruction(ValidateEntries)
