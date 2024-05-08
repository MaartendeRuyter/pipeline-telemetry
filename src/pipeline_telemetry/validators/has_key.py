"""Module to define HasKey class validator"""

import jmespath
from errors import ErrorCode, ListErrors

from .abstract_validator_instruction import (
    AbstractValidatorInstruction,
    BaseValidatorInstructionRuleData,
)


class HasKey(AbstractValidatorInstruction):
    """
    class to define HasFieldName validation instruction.
    """

    INSTRUCTION = "has_key"
    FIELDNAME = "field_name"

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
        if not jmespath.search(fieldname, dict_to_validate):
            return cls._validation_error(ListErrors.KEY_NOT_FOUND, fieldname)

        return []

    @staticmethod
    def _validation_error(error_code: ErrorCode, fieldname: str) -> list[ErrorCode]:
        """returns error code object in list with fieldname as error data"""
        key_specific_error = error_code.code + "@KEY_<" + fieldname + ">"
        return [ErrorCode(code=key_specific_error, description=error_code.description)]
