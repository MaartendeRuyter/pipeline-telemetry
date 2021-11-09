"""[summary]
"""
from enum import Enum

from pipeline_telemetry.settings.data_class import ProcessType

DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES = [
    "RETRIEVE_RAW_DATA",
    "DATA_CONVERSION",
    "DATA_STORAGE",
]

DEFAULT_UPLOAD_DATA_SUB_PROCESS_TYPES = [
    "DATA_SELECTION",
    "DATA_CONVERSION",
    "DATA_UPLOAD",
]


class BaseEnumerator(Enum):
    """
    Class to define base enumerator with a keys method.
    Only to be used for defining new enumerators.
    """

    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())


class DefaultProcessTypes(BaseEnumerator):
    """
    Class to define the defailt process types with their subtypes
    """

    CREATE_DATA_FROM_URL = ProcessType(
        process_type="create_data_from_url",
        subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES,
    )

    CREATE_DATA_FROM_API = ProcessType(
        process_type="create_data_from_api",
        subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES,
    )

    CREATE_DATA_FROM_FILE = ProcessType(
        process_type="create_data_from_file",
        subtypes=DEFAULT_CREATE_DATA_SUB_PROCESS_TYPES,
    )

    UPLOAD_DATA = ProcessType(
        process_type="upload_data", subtypes=DEFAULT_UPLOAD_DATA_SUB_PROCESS_TYPES
    )
