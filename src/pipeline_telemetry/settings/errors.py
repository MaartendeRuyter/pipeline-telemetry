"""Module to define errors
"""
from errors.base import ErrorCode, FunctionalErrorsBaseClass


class ValidationErrors(FunctionalErrorsBaseClass):
    """
    Class to define enumerator errors for Error module
    """
    KEY_NOT_FOUND = ErrorCode(
        code='HAS_KEY_ERR_0001',
        description='Key missing in provided dict')

    FIELD_NOT_FOUND = ErrorCode(
        code='VALIDATE_ENTRIES_ERR_001',
        description='Field that needs counting can not be found')

    WRONG_TYPE_IN_FIELD = ErrorCode(
        code='VALIDATE_ENTRIES_ERR_002',
        description='Field does not contain dict or list')

    UNEXPECTED_NR_OF_ITEMS = ErrorCode(
        code='VALIDATE_ENTRIES_ERR_003',
        description='Field contains unexpected nr of items')
