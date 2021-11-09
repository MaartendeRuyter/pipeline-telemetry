"""Module to define errors
"""
from errors import ErrorCode
from errors.base import FunctionalErrorsBaseClass


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

    ENTRIES_FIELD_NOT_FOUND = ErrorCode(
        code='ENTRIES_HAVE_KEY_ERR_001',
        description='Entries field does not exist')

    ENTRIES_FIELD_OF_WRONG_TYPE = ErrorCode(
        code='ENTRIES_HAVE_KEY_ERR_002',
        description='Entries field does not contain a list')

    KEY_NOT_FOUND_IN_ENTRY = ErrorCode(
        code='ENTRIES_HAVE_KEY_ERR_003',
        description='Key missing in entry')

    ENTRY_IS_NOT_A_DICT = ErrorCode(
        code='ENTRIES_HAVE_KEY_ERR_004',
        description='Entry that needs to have a key is not a dict')
