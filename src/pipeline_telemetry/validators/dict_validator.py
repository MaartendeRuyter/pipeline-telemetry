"""
Module to define the DictValidator class

classes:
    - DictValidator
"""

from typing import Dict, List, Type

from errors import ErrorCode

from ..settings.exceptions import (
    InstructionRegisteredTwice,
    RuleCanHaveOnlyOneInstruction,
    UnknownInstruction,
)
from .abstract_validator_instruction import AbstractValidatorInstruction


class DictValidator:
    """Class to allow a dict validation according to a set of rules.

    class methods:
        - register_instruction():
            method to add instruction sets to the dictvalidator
    public methods:
        - validate():
            method to run the validate of a dict
    """

    _instructions: Dict[str, Type[AbstractValidatorInstruction]] = {}

    @classmethod
    def validate(
        cls, dict_to_validate: dict, validation_rules: dict
    ) -> List[ErrorCode]:
        """Public class method to run the validation.

        :param dict_to_validate: data dict to be validated
        :type dict_to_validate: dict
        :param validation_rules: validation rules for this data object
        :type validation_rules: dict

        :returns: List of ErrorCodes. List is empty if no Errors are found
        """
        errors = []
        for rule in validation_rules.items():
            errors.extend(cls._apply_rule(dict_to_validate, rule))
        return errors

    @classmethod
    def _apply_rule(cls, dict_to_validate: dict, rule: tuple) -> List[ErrorCode]:
        """[summary]

        Args:
            dict_to_validate (dict): data dict to be validated
            rule (tuple): The rule with the instruction on position 0 and
                          details for the instruction on position 1

        Raises:
            UnknownInstruction: [description]

        Returns:
            list: [description]
        """
        instruction = cls._instruction_from_rule(rule)
        if instruction not in cls._instructions:
            raise UnknownInstruction(instruction)
        validation_rule = cls._instructions.get(instruction)

        if validation_rule:
            return validation_rule.validate(
                dict_to_validate=dict_to_validate, rule_dict=rule[1]
            )

        return []

    @classmethod
    def register_instruction(
        cls, instruction_class: Type[AbstractValidatorInstruction]
    ) -> None:
        """Registration at class level of the instruction

        Args:
            instruction_class (type):

        Raises:
            InstructionRegisteredTwice: [description]
        """
        instruction = instruction_class.INSTRUCTION
        if instruction in cls._instructions:
            raise InstructionRegisteredTwice(instruction_class)
        cls._instructions.update({instruction_class.INSTRUCTION: instruction_class})

    @staticmethod
    def _instruction_from_rule(rule: tuple) -> str:
        """Returns the instruction string from rule dict

        Args:
            rule (tuple): The rule with the instruction on position 0 and
                          details for the instruction on position 1

        Raises:
            RuleCanHaveOnlyOneInstruction:
                if 0 or multiple instructions were given

        Returns:
            str: the instruction
        """
        if not (isinstance(rule, tuple) and len(rule) == 2):
            raise RuleCanHaveOnlyOneInstruction(rule)
        return rule[0]
