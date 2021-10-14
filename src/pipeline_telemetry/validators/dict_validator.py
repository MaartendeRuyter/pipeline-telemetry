"""
Module to define the DictValidator class
"""

from ..settings.exceptions import InstructionRegisteredTwice, \
    RuleCanHaveOnlyOneInstruction, UnknownInstruction


class DictValidator():
    """Class to allow a dict validation according to a set of rules.

    class methods:
        - register_instruction():
            method to add instruction sets to the dictvalidator
    public methods:
        - validate():
            method to run the validate of a dict
    """

    _instructions = {}

    @classmethod
    def validate(cls,
                 dict_to_validate: dict,
                 validation_rules: list) -> list:
        """ public method to run the validation """
        errors = []
        for rule in validation_rules.items():
            errors.extend(cls._apply_rule(dict_to_validate, rule))
        return errors

    @classmethod
    def _apply_rule(cls, dict_to_validate: dict, rule: dict) -> list:
        """[summary]

        Args:
            dict_to_validate (dict): [description]
            rule (dict): [description]

        Raises:
            UnknownInstruction: [description]

        Returns:
            list: [description]
        """
        instruction = cls._instruction_from_rule(rule)
        if instruction not in cls._instructions:
            raise UnknownInstruction(instruction)
        return cls._instructions.get(instruction).validate(
            dict_to_validate=dict_to_validate,
            rule_content=rule.get(instruction)
        )

    @classmethod
    def register_instruction(cls, instruction_class: type) -> None:
        """Registration at class level of the instruction

        Args:
            instruction_class (type):

        Raises:
            InstructionRegisteredTwice: [description]
        """
        instruction = instruction_class.instruction
        if instruction in cls._instructions:
            raise InstructionRegisteredTwice(instruction_class)
        cls._instructions.update({
            instruction_class.instruction: instruction_class})

    @staticmethod
    def _instruction_from_rule(rule: dict) -> str:
        """Returns the instuction string from rule dict

        Args:
            rule (dict): The rule

        Raises:
            RuleCanHaveOnlyOneInstruction:
                if 0 or multiple instructions were given

        Returns:
            str: the instruction
        """
        instruction = rule.keys()
        if not len(instruction) == 1:
            raise RuleCanHaveOnlyOneInstruction(rule)
        return list(instruction)[0]
