"""
Module to define customer excpetions for data_validator module

exceptions
- FieldNameMandatory
- UnknownInstruction
- InstructionRegisteredTwice
- RuleCanHaveOnlyOneInstruction
- InvalidProcessType
- BaseCountForSubProcessNotAdded
- TelemetryObjectAlreadyClosed
- StorageClassOfIncorrectType
"""


class FieldNameMandatory(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self, instruction):
        message = f'For `{instruction}` instruction'
        super().__init__(message)


class ExpectedCountMustBePositiveInt(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self):
        message = ''.join([
            'Ruleset does not contain `expected_count` or ',
            'expected count is negative'])
        super().__init__(message)


class UnknownInstruction(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self, instruction):
        super().__init__(f'{instruction} not registered')


class InstructionRegisteredTwice(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self, instruction_class):
        message = ''.join([
            f'{instruction_class.instruction} from class ',
            f'{instruction_class.__name__}.'
        ])
        super().__init__(message)


class RuleCanHaveOnlyOneInstruction(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self, rule):
        message = ''.join([
            'Rule contains multiple keys / instruction : ',
            ', '.join(rule.keys())
        ])
        super().__init__(message)


class InvalidProcessType(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self, process_type):
        message = ''.join([
            f'Invalid Process type {process_type} used with',
            ' Telemetry instanciation'])
        super().__init__(message)


class BaseCountForSubProcessNotAdded(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self, sub_process):
        message = ''.join([
            f'Sub process {sub_process} has not yet been initialized.',
            f' First call increase_sub_process_base_count({sub_process}) ',
            'on telemetry instance'])
        super().__init__(message)


class TelemetryObjectAlreadyClosed(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self):
        message = 'Telemetry object is already closed'
        super().__init__(message)


class StorageClassOfIncorrectType(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self, class_name):
        message = ''.join([
            f'StorageClass `{class_name}` not a child ',
            'class of AbstractTelemetryStorage'])
        super().__init__(message)


class ProcessTypeMustBeDict(Exception):
    """ custom exception for Telemetry Module """

    def __init__(self):
        message = 'Provided custom process_type is not of type dict'
        super().__init__(message)
