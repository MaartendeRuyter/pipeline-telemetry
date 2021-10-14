"""
module to test custom exceptions in pipeline telemetry module
"""
import pytest

from pipeline_telemetry.settings import exceptions


def raise_exception(exception, value):
    """ test helper method to raise exception """
    if value:
        raise exception(value)
    raise exception


def test_field_name_mandatory_exception():
    """ test FieldNameMandatory exception """
    with pytest.raises(exceptions.FieldNameMandatory) as exception:
        raise_exception(exceptions.FieldNameMandatory, 'test_field_name')

    assert 'For `test_field_name` instruction' in str(exception)


def test_unknown_instruction_exception():
    """ test UnknownInstruction exception """
    with pytest.raises(exceptions.UnknownInstruction) as exception:
        raise_exception(exceptions.UnknownInstruction, 'test_instruction')

    assert 'test_instruction not registered' in str(exception)


def test_instruction_registered_twice_exception():
    """ test InstructionRegisteredTwice exception """
    class TestInstructrion():
        """ test class """
        instruction = 'test_instruction'

    with pytest.raises(exceptions.InstructionRegisteredTwice) as exception:
        raise_exception(
            exceptions.InstructionRegisteredTwice, TestInstructrion)

    assert 'test_instruction from class TestInstructrion.' in str(exception)


def test_rule_can_only_have_one_instruction_exception():
    """ test RuleCanHaveOnlyOneInstruction exception """
    with pytest.raises(exceptions.RuleCanHaveOnlyOneInstruction) as exception:
        raise_exception(
            exceptions.RuleCanHaveOnlyOneInstruction, {'key1': 1, 'key2': 2})

    assert 'Rule contains multiple keys' in str(exception)
    assert 'key1, key2' in str(exception)


def test_invalid_process_type_exception():
    """ test InvalidProcessType exception """
    with pytest.raises(exceptions.InvalidProcessType) as exception:
        raise_exception(exceptions.InvalidProcessType, 'test_process_type')

    assert 'Invalid Process type test_process_type' in str(exception)


def test_base_count_for_sub_process_not_added_exception():
    """ test BaseCountForSubProcessNotAdded exception """
    with pytest.raises(exceptions.BaseCountForSubProcessNotAdded) as exception:
        raise_exception(
            exceptions.BaseCountForSubProcessNotAdded, 'sub_process')

    assert 'Sub process sub_process has not yet been initialized' in \
        str(exception)


def test_telemetry_object_already_closed_exception():
    """ test TelemetryObjectAlreadyClosed exception """
    with pytest.raises(exceptions.TelemetryObjectAlreadyClosed) as exception:
        raise_exception(exceptions.TelemetryObjectAlreadyClosed, None)

    assert 'Telemetry object is already closed' in str(exception)


def test_storage_class_of_incorrect_type_exception():
    """ test StorageClassOfIncorrectType exception """
    with pytest.raises(exceptions.StorageClassOfIncorrectType) as exception:
        raise_exception(
            exceptions.StorageClassOfIncorrectType, 'Incorrect_class')

    assert 'StorageClass `Incorrect_class` not a child class' in str(exception)


def test_process_type_must_be_dict_exception():
    """ test ProcessTypeMustBeDict exception """
    with pytest.raises(exceptions.ProcessTypeMustBeDict) as exception:
        raise exceptions.ProcessTypeMustBeDict

    assert 'Provided custom process_type is not of type dict' in str(exception)


def test_expected_count_must_be_positive_int_exception():
    """ test ExpectedCountMustBePositiveInt exception """
    with pytest.raises(exceptions.ExpectedCountMustBePositiveInt) as exception:
        raise exceptions.ExpectedCountMustBePositiveInt

    assert 'Ruleset does not contain `expected_count` or' in str(exception)
