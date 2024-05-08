"""Module to define abstract validator class"""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Type

from errors import ErrorCode


@dataclass(frozen=True)
class BaseValidatorInstructionRuleData:
    field_name: str

    def __post_init__(self):
        if not isinstance(self.field_name, str):
            raise TypeError("Field 'field_name' must be of type 'str'.")


class AbstractValidatorInstruction(metaclass=ABCMeta):
    """Abstract Validator Instruction class"""

    RULE_DATA_CLASS: Type[BaseValidatorInstructionRuleData] = (
        BaseValidatorInstructionRuleData
    )
    INSTRUCTION = "instruction_name"
    FIELDNAME = "field_name"

    def __new__(cls):
        """make this a singleton class"""
        return cls

    @classmethod
    def validate(cls, dict_to_validate: dict, rule_dict: dict) -> list[ErrorCode]:
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
        rule_data = cls.RULE_DATA_CLASS(**rule_dict)
        return cls._validate(dict_to_validate, rule_data)

    @classmethod
    @abstractmethod
    def _validate(
        cls, dict_to_validate: dict, rule_data: BaseValidatorInstructionRuleData
    ) -> List[ErrorCode]:
        """
        method to do the actual validation

        returns:
            - list of errorcodes
        """

    @classmethod
    def _get_field_name(cls, rule_data: BaseValidatorInstructionRuleData) -> str:
        """
        Retrieves the field name in scope from the rule content.
        """
        return getattr(rule_data, cls.FIELDNAME)

    @staticmethod
    @abstractmethod
    def _validation_error(error_code: ErrorCode, fieldname: str) -> list[ErrorCode]:
        """
        Customize the errors and their content for the specific validation rule.
        """
