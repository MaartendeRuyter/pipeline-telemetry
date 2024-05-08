"""Module to define validate entries validator class"""

from dataclasses import dataclass
from typing import Optional

import jmespath
from errors import ErrorCode, ListErrors, add_error_data

from ..settings import exceptions
from .abstract_validator_instruction import (
    AbstractValidatorInstruction,
    BaseValidatorInstructionRuleData,
)


@dataclass(frozen=True)
class ValidateEntriesRuleData(BaseValidatorInstructionRuleData):
    expected_count: int

    def __post_init__(self):
        if not isinstance(self.expected_count, int):
            raise TypeError("Field 'expected_count' must be of type 'int'.")

        if self.expected_count < 0:
            raise exceptions.ExpectedCountMustBePositiveInt

        super().__post_init__()


class ValidateEntries(AbstractValidatorInstruction):
    """
    class to define validate entries instruction.
    This instruction counts the entries in a list or a dict and reports an
    error when the number of items in the list or dict is different from the
    expected nr of items
    """

    RULE_DATA_CLASS = ValidateEntriesRuleData
    INSTRUCTION = "validate_entries"
    expected_count_field = "expected_count"

    @classmethod
    def _validate(
        cls, dict_to_validate: dict, rule_data: BaseValidatorInstructionRuleData
    ) -> list[ErrorCode]:
        """
        method to do the actual validation

        returns:
            - error in case
        """
        fieldname = cls._get_field_name(rule_data)

        field_to_validate = jmespath.search(fieldname, dict_to_validate)

        if not field_to_validate:
            return cls._validation_error(ListErrors.FIELD_NOT_FOUND, fieldname)

        if not isinstance(field_to_validate, (list, dict)):
            return cls._validation_error(ListErrors.WRONG_TYPE_IN_FIELD, fieldname)

        if len(field_to_validate) != cls._get_expected_count(rule_data):
            return cls._validation_error(ListErrors.UNEXPECTED_NR_OF_ITEMS, fieldname)

        return []

    @classmethod
    def _get_expected_count(
        cls, rule_data: BaseValidatorInstructionRuleData
    ) -> Optional[str]:
        """
        retrieves the expected_count in scope of the rule content
        """
        return getattr(rule_data, cls.expected_count_field)

    @staticmethod
    def _validation_error(error_code: ErrorCode, fieldname: str) -> list[ErrorCode]:
        """returns error code object in list with fieldname as error data"""
        return [add_error_data(error=error_code, error_data=fieldname)]
