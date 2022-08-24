"""Module to define abstract validator class
"""
from abc import ABCMeta, abstractmethod
from typing import List, Dict

from errors import ErrorCode


class AbstractValidatorInstruction(metaclass=ABCMeta):
    """Abstract Validator Instruction class

    """
    instruction = 'instruction_name'
    fieldname = 'field_name_key'

    def __new__(cls):
        """ make this a singleton class """
        return cls

    @classmethod
    def validate(
            cls, dict_to_validate: dict, rule_content: dict) -> list[ErrorCode]:
        """
        Public method to run the validation
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

    @abstractmethod
    @classmethod
    def _validate(
            cls, dict_to_validate: dict,
            rule_content: dict) -> List[ErrorCode]:
        """
        method to do the actual validation

        returns:
            - list of errors
        """

    @abstractmethod
    @classmethod
    def _validate_rule(cls, rule_content: Dict) -> None:
        """Method to check the validity of the rule content."""

    @classmethod
    def _get_field_name(cls, rule_content):
        """
        retrieves the field name in scope from the rule content
        """
        return rule_content.get(cls.fieldname, None)

    @abstractmethod
    @staticmethod
    def _validation_error(
            error_code: ErrorCode, fieldname: str) -> list[ErrorCode]:
        """
        Customize the errors and their content for the specific validation rule.
        """
