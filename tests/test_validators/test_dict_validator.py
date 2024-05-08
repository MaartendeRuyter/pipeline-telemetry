"""
module to test validate module of data-validator
"""

import pytest
from test_data import InstructionTestClass

from pipeline_telemetry.settings import exceptions
from pipeline_telemetry.validators.dict_validator import DictValidator
from pipeline_telemetry.validators.has_key import HasKey

# pylint: disable=protected-access


def test_dict_validator_class_exists():
    """check that DictValidator class exists"""
    assert DictValidator


def test_dict_validator_has_instructions():
    """check that DictValidator class has instructions attribute"""
    assert DictValidator._instructions


def test_dict_validator_register_instruction():
    """
    check that register_instruction method registers an instruction
    """
    # ensure that test is not corrupted by previous registrations
    DictValidator._instructions = {}
    DictValidator.register_instruction(InstructionTestClass)
    assert InstructionTestClass.INSTRUCTION in list(DictValidator._instructions.keys())


def test_dict_validator_register_instruction_twice():
    """
    check that register_instruction method raises exception if you try to
    register an instruction twice
    """
    # ensure that test is not corrupted by previous registrations
    DictValidator._instructions = {}
    DictValidator.register_instruction(InstructionTestClass)
    with pytest.raises(exceptions.InstructionRegisteredTwice):
        DictValidator.register_instruction(InstructionTestClass)


def test_apply_rule_raises_exception_with_unregistered_instruction():
    """
    test that _apply_rule method returns an exception when a rule with an
    unregistered instruction is provided
    """
    with pytest.raises(exceptions.UnknownInstruction):
        DictValidator()._apply_rule({}, ("unkwown_rule", {"rule details": "details"}))


def test_apply_rule_calls_do_validate_method(mocker):
    """
    test that _apply_rule method calls the `validate` method on the instruction
    class and returns the value receive from the validate method
    """
    # as previous tests might have cleaned the instruction set it needs to be
    # reregistered
    DictValidator.register_instruction(HasKey)
    rule = ("has_key", {"has_key_details": "rule"})
    mocker.patch(
        "pipeline_telemetry.validators.has_key.HasKey.validate",
        return_value="return_value",
    )
    _do_validate_spy = mocker.spy(HasKey, "validate")
    return_value = DictValidator()._apply_rule({}, rule)
    assert return_value == "return_value"
    assert _do_validate_spy.called


def test_instruction_from_rule_succes():
    """test instruction returns instruction when given a valid rule"""
    valid_rule = ("instruction_in_valid_rule", {"rule_details": "test"})
    assert (
        DictValidator._instruction_from_rule(valid_rule) == "instruction_in_valid_rule"
    )


def test_instruction_from_rule_with_more_the_one_rule():
    """test instruction returns instruction when given a valid rule"""
    to_many_rules = {"rule_1": "test1", "rule_2": "test2"}
    with pytest.raises(exceptions.RuleCanHaveOnlyOneInstruction):
        DictValidator._instruction_from_rule(to_many_rules)
