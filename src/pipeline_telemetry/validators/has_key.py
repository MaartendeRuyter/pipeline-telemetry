"""Module to define HasKey class validator
"""
import jmespath
from errors import ErrorCode, ListErrors

from ..settings import exceptions
from ..validators.dict_validator import DictValidator


class HasKey():
    """
    class to define HasFieldName instruction
    """
    instruction = 'has_key'
    fieldname = 'field_name'

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
        if not jmespath.search(fieldname, dict_to_validate):
            return cls._validation_error(
                ListErrors.KEY_NOT_FOUND, fieldname)

        return []

    @classmethod
    def _validate_rule(cls, rule_content):
        fieldname = cls._get_field_name(rule_content)
        if not isinstance(fieldname, str):
            raise exceptions.FieldNameMandatory(cls.instruction)

    @classmethod
    def _get_field_name(cls, rule_content):
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


DictValidator.register_instruction(HasKey)
